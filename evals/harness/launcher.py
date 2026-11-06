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
         "--mcp-config", "--add-dir", "--dangerously-skip-permissions",
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


def git_refusal(run, cwd, argv):
    """Why a forwarded git call is refused, or None when it stays inside the run."""
    inside = lambda p: str((cwd / p).resolve()).startswith(str(run) + "/")  # noqa: E731
    for i, a in enumerate(argv):
        prev = argv[i - 1] if i else ""
        if prev in ("-c", "--config") or a.startswith("--config="):
            key = (a.split("=", 1)[1] if a.startswith("--config=") else a).split("=", 1)[0]
            if UNSAFE_KEY.match(key):
                return f"configuration key {key}"
        if "://" in a and not (a.startswith("file://") and inside(a[7:])):
            return f"URL {a}"
        if a.startswith("--template"):
            value = a.split("=", 1)[1] if "=" in a else argv[i + 1] if i + 1 < len(argv) else ""
            if value and not inside(value):
                return f"template outside the run: {value}"
        if re.match(r"^[\w.-]+@[\w.-]+:", a) or a.startswith(("--upload-pack",
                                                              "--receive-pack", "--exec")):
            return f"argument {a}"
        if a.startswith("/") and not inside(a):
            return f"path outside the run: {a}"
    sub = [a for a in argv if not a.startswith("-")]
    if sub[:1] == ["config"] or sub[:2] == ["config", "set"]:
        keys = [a for a in sub[1:] if "." in a and not a.startswith(("/", "."))]
        if keys and UNSAFE_KEY.match(keys[0]):
            return f"configuration key {keys[0]}"
    if sub[:1] in (["clone"], ["worktree"], ["submodule"]):
        for a in sub[1:]:
            if not a.startswith("-") and ("/" in a or a.endswith(".git")) and not inside(a):
                return f"path outside the run: {a}"
    return None


class Launcher:
    def __init__(self, real, run, env, model, effort, real_git="/usr/bin/git"):
        self.real, self.run, self.env, self.model, self.effort = real, run, env, model, effort
        self.real_git = real_git
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
        if not str(cwd).startswith(str(self.run) + "/"):
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
        cmd = ([self.real_git, *req["argv"]] if tool == "git"
               else command(self.real, self.run, self.model, self.effort, req["argv"]))
        proc = subprocess.Popen(cmd, cwd=cwd, env=self.env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        def pump(stream, kind):
            for chunk in iter(lambda: stream.read1(65536), b""):
                send(kind, chunk)

        threads = [threading.Thread(target=pump, args=(proc.stdout, 1)),
                   threading.Thread(target=pump, args=(proc.stderr, 2))]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        try:
            send(3, str(proc.wait()).encode())
        except (BrokenPipeError, ConnectionResetError, socket.error):
            pass

    def write(self, entry):
        with open(self.log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def close(self):
        self.server.shutdown()
