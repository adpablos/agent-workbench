"""Shared paths, definitions, environment, and pricing for the eval harness."""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
CORE_REPO = KIT.parent
MODEL = "claude-opus-5-5"
EFFORT = "high"
JUDGE_MODEL = "claude-haiku-5-5"
UV_VERSION = "0.13.4"
FALLBACK_REPLY = "Continue within your authority; I have nothing to add."
MAX_REPLIES = 4

# List prices in USD per million tokens, read on 2026-11-06.
PRICES = {
    "claude-opus-5-5": {"input": 4.00, "cache_5m": 5.00, "cache_1h": 8.00, "cache_read": 0.20,
                        "output": 20.00},
    "claude-haiku-5-5": {"input": 0.10, "cache_5m": 0.125, "cache_1h": 0.20, "cache_read": 0.01,
                         "output": 0.50},
}

# Tools and commands that could reach real services or reveal the upstream fix.
DENIED = [
    "WebFetch", "WebSearch", "Artifact", "ArtifactComments", "ArtifactData", "DesignSync",
    "RemoteTrigger", "PushNotification", "CronCreate", "CronDelete", "ScheduleWakeup", "Workflow",
    "Bash(gh:*)", "Bash(gh *)", "Bash(curl:*)", "Bash(curl *)", "Bash(wget:*)", "Bash(wget *)",
]


USER_INSTRUCTIONS = [str(Path.home() / ".claude" / "CLAUDE.md"),
                     str(Path.home() / ".claude" / "rules" / "**")]


def eval_settings(run_dir, cache, area):
    """Settings for every session in a run: no user instructions or memory, denied tools, and a
    sandbox that limits shell commands to the run directory without network access."""
    hidden = [str(KIT.parent), str(area / "mirrors"), str(area / "runs"), str(area / "grade"),
              str(area / "reviews"), str(area / "judge"), "~/.claude", "~/.codex", "~/.ssh",
              "~/.aws", "~/.config", "~/.gnupg", "~/Library", "~/Documents", "~/Desktop",
              f"/private/tmp/claude-{os.getuid()}"]
    # Under dontAsk, a file tool outside these rules is refused; sandboxed shell commands run.
    allow = ["Bash", "Task", "Agent", "TodoWrite", "Monitor", "TaskStop", "ToolSearch",
             f"Read(/{run_dir}/**)", f"Edit(/{run_dir}/**)", f"Read(/{cache / 'uv'}/**)"]
    return {
        "claudeMdExcludes": USER_INSTRUCTIONS,
        "autoMemoryEnabled": False,
        "permissions": {"allow": allow, "deny": DENIED},
        "sandbox": {
            "enabled": True,
            "failIfUnavailable": True,
            "autoAllowBashIfSandboxed": True,
            "allowUnsandboxedCommands": False,
            "network": {"allowedDomains": [], "strictAllowlist": True, "allowLocalBinding": True},
            "filesystem": {"allowWrite": [str(run_dir), str(cache / "uv")],
                           "denyRead": hidden, "allowRead": [str(run_dir)]},
        },
    }


def home(path=None):
    """The run area: caches, mirrors, runs, and reviews. Never inside a repository."""
    return Path(path or os.environ.get("AWE_HOME", Path.home() / "awe-runs")).expanduser()


def load_scenario(name):
    path = KIT / "scenarios" / name
    data = json.loads((path / "scenario.json").read_text())
    data["dir"] = path
    if "extends" in data:
        base = load_scenario(data["extends"])
        merged = {**base, **{k: v for k, v in data.items() if k != "extends"}}
        merged["base_dir"] = base["dir"]
        return merged
    data["base_dir"] = path
    return data


def load_config(name):
    return json.loads((KIT / "configs" / f"{name}.json").read_text())


GIT = shutil.which("git")


def git(*args, cwd=None, check=True, env=None):
    out = subprocess.run([GIT, *args], cwd=cwd, check=check, text=True, capture_output=True,
                         env=env)
    return out.stdout.strip()


def encode_project(path):
    """How Claude Code names a working directory's folder under ~/.claude/projects."""
    return re.sub(r"[^A-Za-z0-9]", "-", str(path))


def transcripts(run_dir):
    """Every session transcript whose working directory was inside the run directory."""
    root = Path.home() / ".claude" / "projects"
    prefix = encode_project(run_dir)
    found = []
    for project in root.iterdir() if root.exists() else []:
        if project.name == prefix or project.name.startswith(prefix + "-"):
            found += sorted(project.glob("*.jsonl"))
            found += sorted(project.glob("*/subagents/*.jsonl"))
    return found


def real_claude():
    for d in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(d) / "claude"
        if candidate.is_file() and "/runs/" not in str(candidate):
            return str(candidate)
    raise SystemExit("claude not found on PATH")


def run_env(run_dir, cache):
    """The environment every agent process in a run inherits."""
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("CLAUDE", "ANTHROPIC_", "GH_", "GITHUB_", "UV_", "VIRTUAL_ENV",
                                "PIP_", "PREFECT_", "MISE_"))
           and k not in ("SSH_AUTH_SOCK", "GIT_DIR", "GIT_WORK_TREE")}
    env.update({
        "PATH": os.pathsep.join([str(run_dir / "env" / "bin"), str(cache / "tools" / "bin"),
                                 "/opt/homebrew/bin", "/usr/local/bin", "/usr/bin", "/bin",
                                 "/usr/sbin", "/sbin"]),
        "TMPDIR": str(run_dir / "tmp"),
        # Claude Code otherwise gives sandboxed shells a temporary folder shared by every session.
        "CLAUDE_CODE_TMPDIR": str(run_dir / "tmp"),
        "XDG_CACHE_HOME": str(run_dir / "cache"),
        "PRE_COMMIT_HOME": str(run_dir / "cache" / "pre-commit"),
        "PIP_CACHE_DIR": str(run_dir / "cache" / "pip"),
        "PIP_NO_INDEX": "1",
        "PREFECT_HOME": str(run_dir / "cache" / "prefect-home"),
        "UV_CACHE_DIR": str(cache / "uv"),
        "UV_OFFLINE": "1",
        "UV_PYTHON": "python3.14",
        "UV_PYTHON_DOWNLOADS": "never",
        "UV_LINK_MODE": "clone",
        "GIT_CONFIG_GLOBAL": str(run_dir / "env" / "gitconfig"),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "/usr/bin/false",
        "SSH_ASKPASS": "/usr/bin/false",
        "GH_CONFIG_DIR": str(run_dir / "env" / "gh"),
        "BASH_DEFAULT_TIMEOUT_MS": "1800000",
        "BASH_MAX_TIMEOUT_MS": "3600000",
    })
    return env


def cost(model, usage):
    p = PRICES.get(model)
    if not p:
        return None
    creation = usage.get("cache_creation") or {}
    one_hour = creation.get("ephemeral_1h_input_tokens", 0)
    five_min = creation.get("ephemeral_5m_input_tokens",
                            usage.get("cache_creation_input_tokens", 0) - one_hour)
    return (usage.get("input_tokens", 0) * p["input"] + five_min * p["cache_5m"]
            + one_hour * p["cache_1h"] + usage.get("cache_read_input_tokens", 0) * p["cache_read"]
            + usage.get("output_tokens", 0) * p["output"]) / 1e6


def rmtree(path):
    if Path(path).exists():
        shutil.rmtree(path)
