"""Run, for agents whose shell is sandboxed, the commands that the sandbox cannot run.

A sandboxed shell has no network, so `claude` cannot run there, and it may not write any
`.git/config`, so `git clone` and `git remote set-url` fail. The run's `claude` and `git` commands
are clients that send their arguments over localhost to this launcher, which runs in the harness.
For `claude`, the launcher fixes the model, effort, permissions, and settings; that session's own
shell is sandboxed again. For `git`, only subcommands that write repository configuration come
here, and only when every path stays inside the run, no URL names a network host, and no
configuration key could run a program. Everything else runs in the sandbox as usual.
"""

import json
import re
import socket
import socketserver
import struct
import subprocess
import threading
import time
from pathlib import Path

FIXED = {"--model", "--effort", "--permission-mode", "--setting-sources", "--settings",
         "--mcp-config", "--add-dir", "--plugin-dir", "--dangerously-skip-permissions",
         "--allow-dangerously-skip-permissions"}
TAKES_VALUE = FIXED - {"--dangerously-skip-permissions", "--allow-dangerously-skip-permissions"}

GIT_FORWARD = {"clone", "init", "remote", "config", "worktree", "submodule", "branch",
               "checkout", "switch"}
GIT_OPTIONS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
UNSAFE_KEY = re.compile(r"^(core\.(hookspath|fsmonitor|sshcommand|gitproxy|pager|editor|askpass)"
                        r"|.*\.insteadof|credential\..*|alias\..*|include(if)?\..*|filter\..*"
                        r"|diff\..*\.(command|textconv)|merge\..*\.driver|uploadpack\..*"
                        r"|protocol\..*|https?\..*|url\..*|sequence\.editor|gpg\..*|ssh\..*"
                        r"|remote\..*\.(uploadpack|receivepack|proxy|vcs))$", re.I)

CLIENT = '''#!/usr/bin/env python3
# Sends this call to the run's launcher and relays its output and exit status.
import json, os, socket, struct, sys
TOOL = @TOOL@
if TOOL == "git":
    args, i = sys.argv[1:], 0
    while i < len(args) and args[i].startswith("-"):
        i += 2 if args[i] in @GIT_OPTS@ else 1
    if i >= len(args) or args[i] not in @GIT_FORWARD@:
        os.execv(@REAL_GIT@, ["git"] + args)
sock = socket.create_connection(("127.0.0.1", int(open(@PORT@).read())))
sock.sendall((json.dumps({"tool": TOOL, "argv": sys.argv[1:], "cwd": os.getcwd()}) + "\\n").encode())
f = sock.makefile("rb")
while True:
    head = f.read(5)
    if len(head) < 5:
        sys.exit(1)
    kind, size = struct.unpack(">BI", head)
    data = f.read(size)
    if kind == 3:
        sys.exit(int(data))
    out = sys.stdout if kind == 1 else sys.stderr
    out.buffer.write(data)
    out.flush()
'''


def claude_refusal(run, argv):
    """A session may resume only a conversation that started in this run."""
    for i, a in enumerate(argv):
        name, eq, value = a.partition("=")
        if name in ("--resume", "-r"):
            sid = value if eq else (argv[i + 1] if i + 1 < len(argv) else "")
            prefix = re.sub(r"[^A-Za-z0-9]", "-", str(run))
            projects = Path.home() / ".claude" / "projects"
            if not any(p.name == prefix or p.name.startswith(prefix + "-")
                       for p in projects.glob(f"*/{sid}.jsonl") for p in [p.parent]):
                return f"resume of a session outside this run: {sid}"
    return None


def command(real, run, model, effort, argv):
    """The real call: the caller's arguments without the ones the run fixes, plus the fixed."""
    kept, skip = [], False
    for a in argv:
        if skip:
            skip = False
            continue
        name = a.split("=", 1)[0]
        if name in FIXED:
            skip = name in TAKES_VALUE and "=" not in a
            continue
        kept.append(a)
    return [real, "--model", model, "--effort", effort, "--permission-mode", "dontAsk",
            "--setting-sources", "project,local", "--settings", str(run / "env" / "settings.json"),
            "--strict-mcp-config", *kept]


GIT_GLOBAL_FLAGS = {"--no-pager", "-P", "--no-optional-locks", "--literal-pathspecs",
                    "--no-replace-objects"}
GIT_SAFETY = ["-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false"]


def git_refusal(run, cwd, argv):
    """Why a forwarded git call is refused, or None when it stays inside the run.

    Forwarded commands run outside the sandbox, so every path must resolve inside the run, no
    URL may name a network host, and no configuration key may run a program."""
    def inside(path, base):
        target = (base / path).resolve()
        return target == run or str(target).startswith(str(run) + "/")

    def unsafe_key(arg):
        return UNSAFE_KEY.match(arg.split("=", 1)[0])

    base, i = cwd, 0
    while i < len(argv) and argv[i].startswith("-"):
        a = argv[i]
        name, _, value = a.partition("=")
        if name in ("-C", "--git-dir", "--work-tree", "--namespace") or a == "-c":
            value = value or (argv[i + 1] if i + 1 < len(argv) else "")
            i += 1 if "=" in a else 2
        else:
            i += 1
        if a == "-c" or name == "--config-env":
            if unsafe_key(value):
                return f"configuration key {value.split('=', 1)[0]}"
        elif name in ("-C", "--git-dir", "--work-tree"):
            if not inside(value, base):
                return f"path outside the run: {value}"
            if name == "-C":
                base = (base / value).resolve()
        elif name not in GIT_GLOBAL_FLAGS and name != "--namespace":
            return f"global option {name}"
    if i >= len(argv) or argv[i] not in GIT_FORWARD:
        return f"subcommand {argv[i] if i < len(argv) else '(none)'}"
    sub, rest = argv[i], argv[i + 1:]
    for j, a in enumerate(rest):
        name, eq, value = a.partition("=")
        if a.startswith(("--upload-pack", "--receive-pack", "--exec", "--config")) or (
                sub == "clone" and a in ("-u", "-c")):
            return f"argument {a}"
        candidate = value if a.startswith("-") and eq else a
        if a.startswith("-") and not eq:
            continue
        if "://" in candidate and not (candidate.startswith("file://")
                                       and inside(candidate[7:], base)):
            return f"URL {candidate}"
        if re.match(r"^[\w.-]+@[\w.-]+:", candidate):
            return f"argument {candidate}"
        if candidate and "://" not in candidate and not inside(candidate, base):
            return f"path outside the run: {candidate}"
    if sub == "config":
        keys = [a for a in rest if not a.startswith("-") and a not in
                ("set", "get", "unset", "list", "edit", "rename-section", "remove-section")]
        if keys and unsafe_key(keys[0]):
            return f"configuration key {keys[0]}"
    return None


class Launcher:
    def __init__(self, real, run, env, model, effort, real_git="/usr/bin/git"):
        self.real, self.run, self.env, self.model, self.effort = real, run, env, model, effort
        self.real_git = real_git
        self.procs = set()
        self.log = run / "logs" / "claude-calls.jsonl"
        launcher = self

        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                launcher.serve(self.rfile, self.wfile)

        self.server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        (run / "env" / "launcher.port").write_text(str(self.server.server_address[1]))
        for tool in ("claude", "git"):
            client = run / "env" / "bin" / tool
            client.write_text(CLIENT.replace("@PORT@", repr(str(run / "env" / "launcher.port")))
                              .replace("@TOOL@", repr(tool)).replace("@REAL_GIT@", repr(real_git))
                              .replace("@GIT_OPTS@", repr(GIT_OPTIONS_WITH_VALUE))
                              .replace("@GIT_FORWARD@", repr(GIT_FORWARD)))
            client.chmod(0o755)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def serve(self, rfile, wfile):
        lock = threading.Lock()

        def send(kind, data):
            with lock:
                wfile.write(struct.pack(">BI", kind, len(data)) + data)
                wfile.flush()

        req = json.loads(rfile.readline())
        cwd = Path(req["cwd"]).resolve()
        tool = req.get("tool", "claude")
        entry = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tool": tool,
                 "cwd": str(cwd), "argv": req["argv"]}
        refusal = None
        if cwd != self.run and not str(cwd).startswith(str(self.run) + "/"):
            refusal = "folder outside the run"
        elif tool == "git":
            refusal = git_refusal(self.run, cwd, req["argv"])
        if refusal:
            entry["refused"] = refusal
            self.write(entry)
            send(2, f"{tool}: refused by the eval harness: {refusal}\n".encode())
            send(3, b"1")
            return
        self.write(entry)
        if tool == "claude":
            refusal = claude_refusal(self.run, req["argv"])
            if refusal:
                entry["refused"] = refusal
                self.write(entry)
                send(2, f"claude: refused by the eval harness: {refusal}\n".encode())
                send(3, b"1")
                return
        cmd = ([self.real_git, *GIT_SAFETY, *req["argv"]] if tool == "git"
               else command(self.real, self.run, self.model, self.effort, req["argv"]))
        proc = subprocess.Popen(cmd, cwd=cwd, env=self.env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.procs.add(proc.pid)

        def pump(stream, kind):
            for chunk in iter(lambda: stream.read1(65536), b""):
                try:
                    send(kind, chunk)
                except OSError:
                    proc.terminate()
                    return

        def hangup():
            # The caller sends nothing after its request, so end of input means it was stopped:
            # stop what it started, as a shell would stop its own child.
            rfile.read()
            if proc.poll() is None:
                proc.terminate()

        threads = [threading.Thread(target=pump, args=(proc.stdout, 1)),
                   threading.Thread(target=pump, args=(proc.stderr, 2))]
        for t in threads:
            t.start()
        threading.Thread(target=hangup, daemon=True).start()
        for t in threads:
            t.join()
        code = proc.wait()
        self.procs.discard(proc.pid)
        try:
            send(3, str(code).encode())
        except (BrokenPipeError, ConnectionResetError, socket.error):
            pass

    def pids(self):
        return list(self.procs)

    def write(self, entry):
        with open(self.log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def close(self):
        self.server.shutdown()
