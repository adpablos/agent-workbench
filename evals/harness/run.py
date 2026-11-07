"""Run one scenario under one configuration and record what happened.

Usage: python3 -I evals/harness/run.py <scenario> <config> [--rep N] [--home DIR] [--core REV]
                                       [--limit-minutes M]
"""

import argparse
import datetime
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
import launcher  # noqa: E402
from common import KIT, git  # noqa: E402

HOST_LIMIT = re.compile(r"hit your [\w -]*limit|usage limit reached", re.I)
NOW = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")  # noqa


def prepare_cache(home, scenario):
    """Mirrors of each repository, the pinned uv, and a dependency cache warmed at the base."""
    cache = home / "cache"
    mirrors = home / "mirrors"
    mirrors.mkdir(parents=True, exist_ok=True)
    for name, repo in scenario["repos"].items():
        mirror = mirrors / f"{name}.git"
        if not mirror.exists():
            git("clone", "--bare", repo["url"], str(mirror))
        if subprocess.run([common.GIT, "--git-dir", str(mirror), "cat-file", "-e", repo["base"]],
                          capture_output=True).returncode:
            git("--git-dir", str(mirror), "fetch", "origin", "+refs/heads/*:refs/heads/*")
    if not (cache / "tools" / "bin" / "uv").exists():
        subprocess.run([sys.executable, "-m", "venv", str(cache / "tools")], check=True)
        subprocess.run([str(cache / "tools" / "bin" / "pip"), "install", "-q",
                        f"uv=={common.UV_VERSION}"], check=True)
    base = scenario["repos"][scenario["service"]]["base"]
    warm = cache / "warm" / base[:12]
    if not (warm / ".venv").exists():
        common.rmtree(warm)
        git("clone", "-q", str(mirrors / f"{scenario['service']}.git"), str(warm))
        git("checkout", "-q", base, cwd=warm)
        env = {**os.environ, "UV_CACHE_DIR": str(cache / "uv"), "UV_PYTHON": "python3.14",
               "UV_PYTHON_DOWNLOADS": "never", "UV_LINK_MODE": "clone",
               "PATH": f"{cache / 'tools' / 'bin'}{os.pathsep}{os.environ['PATH']}"}
        subprocess.run(["uv", "sync", "--frozen", "-q"], cwd=warm, env=env, check=True)
    return cache, mirrors


def write_env(run, cache, home):
    envdir = run / "env"
    (envdir / "bin").mkdir(parents=True)
    (envdir / "gh").mkdir()
    for d in ("tmp", "cache", "logs"):
        (run / d).mkdir()
    (envdir / "gitconfig").write_text(
        "[user]\n\tname = Eval Agent\n\temail = agent@example.invalid\n"
        "[url \"file:///nonexistent/blocked/\"]\n\tinsteadOf = https://github.com/\n"
        "\tinsteadOf = git@github.com:\n\tinsteadOf = ssh://git@github.com/\n"
        "[credential]\n\thelper =\n[init]\n\tdefaultBranch = main\n"
        f"\ttemplateDir = {envdir / 'git-template'}\n")
    (envdir / "git-template").mkdir()
    (envdir / "config").mkdir()
    common.copy_cache(cache / "uv", run / "cache" / "uv")
    settings = common.eval_settings(run, cache, home)
    (envdir / "settings.json").write_text(json.dumps(settings, indent=2) + "\n")


def make_remote(run, mirrors, name, base):
    remote = run / "remotes" / f"{name}.git"
    git("init", "-q", "--bare", str(remote))
    git("--git-dir", str(mirrors / f"{name}.git"), "push", "-q", str(remote),
        f"{base}:refs/heads/main")
    git("--git-dir", str(remote), "symbolic-ref", "HEAD", "refs/heads/main")
    return remote


def build(run, scenario, config, core_rev, cache, mirrors, env):
    names = list(scenario["repos"])
    remotes = {n: make_remote(run, mirrors, n, scenario["repos"][n]["base"]) for n in names}
    ticket = (scenario["base_dir"] / "TICKET.md").read_text()
    today = datetime.date.today().isoformat()
    if config["layout"] == "bare":
        root = run / "ws"
        root.mkdir()
        for n in names:
            git("clone", "-q", str(remotes[n]), str(root / n), env=env)
        (root / "TICKET.md").write_text(ticket)
        return root, {"service_copies": [root / scenario["service"]],
                      "config_copies": [root / scenario["config_repo"]], "references": []}
    root = run / "wb"
    for d in ("core", "private/tasks", "work", ".claude"):
        (root / d).mkdir(parents=True)
    # The core without this kit: a candidate revision must not carry the hidden tests.
    archive = subprocess.run([common.GIT, "-C", str(common.CORE_REPO), "archive", core_rev, "--",
                              ".", ":(exclude)evals"],
                             check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(root / "core")], input=archive, check=True)
    shutil.copy(root / "core" / "templates" / "workbench-entrypoint.md", root / "AGENTS.md")
    (root / ".claude" / "settings.json").write_text(json.dumps(
        {"claudeMdExcludes": [f"{root}/repos/**", f"{root}/tools/**"]}, indent=2) + "\n")
    policy = (KIT / "workbench" / "POLICY.md").read_text().replace("{date}", today)
    (root / "private" / "POLICY.md").write_text(policy)
    refs = run / "refs"
    sources, rows = [], []
    for n in names:
        git("clone", "-q", str(remotes[n]), str(refs / n), env=env)
        git("-C", str(refs / n), "remote", "set-url", "--push", "origin", "DISABLED", env=env)
        sources.append({"name": n, "kind": "repository", "location": str(refs / n),
                        "remote": str(remotes[n]), "access": "read",
                        "upstream": scenario["repos"][n]["url"]})
        rows.append(f"| `{refs / n}` | {n}, read-only reference clone | `workspace.json` | {today} |")
    sha = git("-C", str(common.CORE_REPO), "rev-parse", f"{core_rev}^{{commit}}")
    tags = git("-C", str(common.CORE_REPO), "tag", "--points-at", sha).split()
    (root / "private" / "workspace.json").write_text(json.dumps({
        "description": "Approved scope and pins for this workbench. Change only after the "
                       "requester approves the exact content.",
        "approved": today,
        "core": {"path": "core", "revision": sha, "tag": tags[0] if tags else "",
                 "previous_revision": ""},
        "sources": sources,
        "writable": ["private", "work"],
        "tools": [],
    }, indent=2) + "\n")
    (root / "private" / "INDEX.md").write_text(
        "# Index\n\n## Priorities\n\nNone yet.\n\n## Recently closed\n\nNone.\n\n"
        "## Decisions\n\nNone.\n\n## Sources\n\n| Locator | What it is | Provenance | Checked |\n"
        "|---|---|---|---|\n" + "\n".join(rows) + "\n")
    (root / "TICKET.md").write_text(ticket)
    return root, {"service_copies": [], "config_copies": [],
                  "references": [refs / n for n in names]}


def candidates(run, layout, marker):
    """Every clone of a repository that an agent could have changed, found by a path that only
    that repository has, since agents name their copies freely."""
    found = []
    roots = [run / "ws"] if layout == "bare" else [run / "refs", run / "wb" / "work"]
    for r in roots:
        for depth in ("*", "*/*", "*/*/*"):
            for p in r.glob(depth):
                if (p / ".git").exists() and (p / marker).is_dir():
                    found.append(p)
    return sorted(set(found))


def primary(copies, run, name):
    """The copy an agent worked in: cloned from the reference or remote, most recently used."""
    def origin(p):
        return git("-C", str(p), "remote", "get-url", "origin", check=False)
    first = [p for p in copies
             if origin(p) in (str(run / "refs" / name), str(run / "remotes" / f"{name}.git"))]
    pool = first or copies
    return max(pool, key=lambda p: (p / ".git" / "index").stat().st_mtime) if pool else None


def repo_state(path, base):
    """Commit, staged and unstaged changes, and untracked files, compared with the base."""
    status = git("-C", str(path), "status", "--porcelain", "--untracked-files=all", check=False)
    head = git("-C", str(path), "rev-parse", "HEAD", check=False)
    diff = git("-C", str(path), "diff", base, "--stat", check=False) if head else ""
    return {"head": head, "status": status, "diff_stat": diff,
            "changed": bool(status) or (head and head != base)}


def kill_run(run, roots=()):
    """Stop every process of the run: the given roots, their descendants, and any process whose
    command line names the run folder. The host does not show its environment to `ps`."""
    seen = set()
    for sig in (signal.SIGTERM, signal.SIGKILL):
        out = subprocess.run(["ps", "-axo", "pid=,ppid=,command="], capture_output=True,
                             text=True).stdout
        procs = {}
        for line in out.splitlines():
            parts = line.split(None, 2)
            if len(parts) == 3:
                procs[int(parts[0])] = (int(parts[1]), parts[2])
        targets = {p for p in roots if p in procs}
        targets |= {p for p, (_, cmd) in procs.items() if str(run) + "/" in cmd}
        grew = True
        while grew:
            children = {p for p, (pp, _) in procs.items() if pp in targets} - targets
            targets |= children
            grew = bool(children)
        targets.discard(os.getpid())
        # Keep what the first pass found: a child reparented after SIGTERM is still the run's.
        targets |= {p for p in seen if p in procs}
        seen |= targets
        for pid in targets:
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                pass
        if not targets:
            return
        time.sleep(5)


def session(run, cwd, env, prompt, log, resume=None, cut=None, deadline=None, starter=None):
    sid = resume or str(uuid.uuid4())
    cmd = launcher.command(common.real_claude(), run, common.MODEL, common.EFFORT,
                           ["-p", prompt, "--output-format", "stream-json", "--verbose"]
                           + (["--resume", sid] if resume else ["--session-id", sid]))
    start = time.time()
    with open(log, "w") as out, open(str(log) + ".err", "w") as err:
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=out, stderr=err,
                                stdin=subprocess.DEVNULL, start_new_session=True)
        stopped = None
        while proc.poll() is None:
            time.sleep(2)
            if cut and cut():
                stopped = "cut"
            elif deadline and time.time() > deadline:
                stopped = "time limit"
            if stopped:
                kill_run(run, [proc.pid, *(starter.pids() if starter else [])])
                proc.wait()
                break
    text, result = "", None
    for line in Path(log).read_text().splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            result = event
            text = event.get("result") or ""
    return {"session_id": sid, "log": str(log), "exit": proc.returncode, "stopped": stopped,
            "seconds": round(time.time() - start, 1), "result_text": text,
            "cli_cost_usd": result.get("total_cost_usd") if result else None,
            "num_turns": result.get("num_turns") if result else None}


def judge(home, text, stops):
    """Classify the agent's last message: DONE, OTHER, or the id of an expected stop."""
    rubric = (KIT / "harness" / "judge.md").read_text()
    listing = "\n".join(f"- {s['id']}: {s['description']}" for s in stops) or "- (none)"
    prompt = rubric.replace("{stops}", listing).replace("{message}", text or "(empty)")
    jdir = home / "judge"
    jdir.mkdir(exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "ANTHROPIC_"))}
    out = subprocess.run(
        [common.real_claude(), "-p", prompt, "--model", common.JUDGE_MODEL, "--effort", "low",
         "--tools", "", "--setting-sources", "project,local", "--strict-mcp-config",
         "--settings", json.dumps({"claudeMdExcludes": common.USER_INSTRUCTIONS,
                                   "autoMemoryEnabled": False}),
         "--output-format", "json"], cwd=jdir, env=env, capture_output=True, text=True,
        stdin=subprocess.DEVNULL)
    try:
        data = json.loads(out.stdout)
        answer = (data.get("result") or "").strip().split()[0].strip(".`*")
        usd = data.get("total_cost_usd")
    except (json.JSONDecodeError, IndexError):
        answer, usd = "OTHER", None
    valid = {"DONE", "OTHER"} | {s["id"] for s in stops}
    return (answer if answer in valid else "OTHER"), usd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario")
    ap.add_argument("config")
    ap.add_argument("--rep", type=int, default=1)
    ap.add_argument("--home")
    ap.add_argument("--core", help="core revision; overrides the configuration's")
    ap.add_argument("--limit-minutes", type=int, default=120)
    args = ap.parse_args()

    home = common.home(args.home)
    scenario = common.load_scenario(args.scenario)
    config = common.load_config(args.config)
    core_rev = args.core or config.get("core")
    cache, mirrors = prepare_cache(home, scenario)
    stamp = datetime.datetime.now().strftime("%m%d-%H%M%S")
    run = home / "runs" / f"{args.scenario.split('-')[0]}-{args.config}-r{args.rep}-{stamp}"
    run.mkdir(parents=True)
    env = common.run_env(run, cache)
    write_env(run, cache, home)
    starter = launcher.Launcher(common.real_claude(), run, env, common.MODEL, common.EFFORT,
                                common.GIT)
    root, layout = build(run, scenario, config, core_rev, cache, mirrors, env)
    service, config_repo = scenario["service"], scenario["config_repo"]
    bases = {n: r["base"] for n, r in scenario["repos"].items()}
    markers = {n: r["marker"] for n, r in scenario["repos"].items()}

    def snapshot():
        return {n: {str(p.relative_to(run)): repo_state(p, bases[n])
                    for p in candidates(run, config["layout"], markers[n])} for n in bases}

    def service_changed():
        # Count only added or modified files and new commits: a clone still checking out shows
        # its missing files as deleted.
        for p in candidates(run, config["layout"], markers[service]):
            if (p / ".git" / "index.lock").exists():
                continue
            if git("-C", str(p), "diff", "HEAD", "--name-only", "--diff-filter=AMR", "--", "src",
                   check=False) or git("-C", str(p), "ls-files", "--others",
                                       "--exclude-standard", "--", "src", check=False):
                return True
            head = git("-C", str(p), "rev-parse", "HEAD", check=False)
            if head and head != bases[service] and git(
                    "-C", str(p), "diff", "--name-only", bases[service], head, "--", "src",
                    check=False):
                return True
        return False

    remotes_before = {p.name: git("--git-dir", str(p), "for-each-ref", check=False)
                      for p in (run / "remotes").iterdir()}
    record = {
        "scenario": args.scenario, "config": args.config, "rep": args.rep,
        "core": core_rev, "layout": config["layout"], "run_dir": str(run), "root": str(root),
        "started": NOW(), "model": common.MODEL, "effort": common.EFFORT,
        "manifest": manifest(run, scenario, config, core_rev),
        "sessions": [], "replies": [], "snapshots": [snapshot()],
        "remotes_before": remotes_before,
    }
    (run / "home-scan.stamp").touch()
    started = time.time()
    deadline = time.time() + args.limit_minutes * 60
    stops = list(scenario.get("expected_stops", []))
    mode = config.get("mode", "")
    prompt = f"{common.TICKET_PROMPT} {mode}".strip()
    cut = service_changed if scenario.get("cut") else None
    record["waited_for_workers_seconds"] = 0

    def wait_for_workers(cut=None):
        """A requester answers once the work they handed over has stopped, not while a
        Director's workers still run in the background. The cut applies while they run."""
        waited = time.time()
        fired = False
        while starter.pids() and time.time() < deadline:
            if cut and cut():
                kill_run(run, starter.pids())
                fired = True
                break
            time.sleep(5)
        record["waited_for_workers_seconds"] += round(time.time() - waited)
        return fired

    s = session(run, root, env, prompt, run / "logs" / "s1.jsonl", cut=cut, deadline=deadline,
                starter=starter)
    s["role"] = "main"
    record["sessions"].append(s)
    if cut and s["stopped"] is None and wait_for_workers(cut):
        s["stopped"] = "cut"
    if s["stopped"] == "cut":
        record["cut"] = {"at": NOW(), "state": snapshot(),
                         "diff": {str(p.relative_to(run)): git("-C", str(p), "diff",
                                                                bases[service], check=False)
                                  for p in candidates(run, config["layout"],
                                                      markers[service])}}
        prompt = f"{scenario['resume_prompt']} {mode}".strip()
        s = session(run, root, env, prompt, run / "logs" / "s2.jsonl", deadline=deadline,
                    starter=starter)
        s["role"] = "resume"
        record["sessions"].append(s)
    answered = set()
    while s["stopped"] != "time limit" and len(record["replies"]) < common.MAX_REPLIES:
        if HOST_LIMIT.search(s["result_text"]):
            record["host_limit"] = True
            break
        wait_for_workers()
        record["snapshots"].append(snapshot())
        open_stops = [x for x in stops if x["id"] not in answered]
        label, usd = judge(home, s["result_text"], open_stops)
        if label == "DONE":
            record["replies"].append({"label": label, "judge_usd": usd, "reply": None})
            break
        stop = next((x for x in open_stops if x["id"] == label), None)
        reply = stop["reply"] if stop else common.FALLBACK_REPLY
        if stop:
            answered.add(stop["id"])
        record["replies"].append({"label": label, "judge_usd": usd, "reply": reply,
                                  "kind": "scripted" if stop else "fallback",
                                  "after_snapshot": len(record["snapshots"]) - 1})
        n = len(record["sessions"]) + 1
        s = session(run, root, env, reply, run / "logs" / f"s{n}.jsonl",
                    resume=s["session_id"], deadline=deadline, starter=starter)
        s["role"] = "reply"
        record["sessions"].append(s)
    kill_run(run, starter.pids())
    starter.close()
    record["snapshots"].append(snapshot())
    record["ended"] = NOW()
    record["wall_seconds"] = round(time.time() - started)
    record["timed_out"] = time.time() > deadline
    (run / "record.json").write_text(json.dumps(record, indent=2, default=str) + "\n")
    print(run)


def manifest(run, scenario, config, core_rev):
    version = subprocess.run([common.real_claude(), "--version"], capture_output=True,
                             text=True).stdout.strip()
    return {
        "claude_version": version, "uv": common.UV_VERSION, "python": "3.14",
        "kit_commit": git("-C", str(KIT), "rev-parse", "HEAD"),
        "kit_dirty": bool(git("-C", str(KIT), "status", "--porcelain", "--", ".")),
        "core_revision": core_rev, "repos": scenario["repos"], "mode": config.get("mode", ""),
        "prices": common.PRICES, "prices_read": "2026-11-06",
        "settings": json.loads((run / "env" / "settings.json").read_text()),
    }


if __name__ == "__main__":
    main()
