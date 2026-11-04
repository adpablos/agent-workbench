# Hosts

Where agent hosts differ in ways that change what you do. Everything else in this repository is
host-neutral. Read this when setting up a workbench, when a probe fails, or the first time you
delegate on a host.

Each section says what was observed and where, or that it comes from documentation. None of it is a
guarantee: the probes in [VALIDATION.md](VALIDATION.md) decide what is true in your environment.

One workbench can serve several hosts: they share `AGENTS.md`, and each ignores the other's
settings. Alternating hosts on the same work is a change of Director, so use the ownership
transfer in [OPERATING.md](../OPERATING.md).

## Instruction loading

Observed on macOS from the command line, without the interactive interface, at default settings.

| Situation | Claude Code 2.1.305 | Codex 0.160.0 |
|---|---|---|
| Root `AGENTS.md` | Loaded, unless hidden. Its documentation says some sessions miss it before 2.1.281 | Loaded |
| Hidden by | A `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in that folder, or a `CLAUDE.md` in a folder above it. `~/.claude/CLAUDE.md` did not hide it | Not observed |
| Folder that is not a Git repository | Works | Asks to trust the folder; `codex exec` needs `--skip-git-repo-check` |
| Session started in a repository | Loads that repository's file and the workbench `AGENTS.md`, unless the repository has a `CLAUDE.md`, which hides both `AGENTS.md` files | Loads only that repository's file |
| Session started in a subfolder without `.git` | Loads the workbench `AGENTS.md` | Loads nothing |
| Agent reads a file in a subfolder | Loads that subfolder's instructions on demand, also in subagents | Loads nothing |
| Names to probe | `CLAUDE.md`, `CLAUDE.local.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, `AGENTS.md` | `AGENTS.override.md`, `AGENTS.md`, any `project_doc_fallback_filenames` |

Skills and agents can also come from subfolders, and the subfolder probe covers them. Claude Code
documents `.claude/skills/`, `.claude/agents/`, and `.claude/commands/`, and Codex
`.agents/skills/`; Copilot is covered in its own section. Probe every folder the installed version
documents, since the lists grow. Observed with Claude Code 2.1.316 and Codex 0.166.0, after the
agent read a file in `repos/probe/` or `tools/probe/`:

- Claude Code loaded the skills in that folder's `.claude/skills/` on demand, even with the
  `claudeMdExcludes` setting below. The transcript showed a `commands_changed` entry, and the agent
  listed them. It loaded no agent or command from there.
- Codex loaded nothing.

Setting `instructionFiles` to `claude-md-and-agents-md` in user settings makes Claude Code load
both `CLAUDE.md` and `AGENTS.md`. Do not rely on it: it belongs to one person, so two people would
load different instructions. Keep one instruction file per folder instead.

To confirm a load on Claude Code, search the session transcript for the probe word, not for one
kind of entry. On 2.1.305, `CLAUDE.md` forms appeared as `nested_memory` entries and `AGENTS.md`
as `hook_additional_context`. On 2.1.316, `AGENTS.md` appeared as an `instructions` attachment.

### Claude Code: references inside the workbench

Because Claude Code loads subfolder instructions on demand, a reference repository's instructions
reach the Director as soon as it reads one of that repository's files. Without further settings
the subfolder probe fails. Excluding `repos/` and `tools/` in `.claude/settings.json` at the
workbench root stops their instruction files, but on 2.1.316 not their skills, so the probe still
fails: keep both folders outside the workbench root. Keep the setting anyway, as a guard for any
reference that ends up inside. Use the workbench's real absolute path:

```json
{
  "claudeMdExcludes": ["/path/to/wb/repos/**", "/path/to/wb/tools/**"]
}
```

If that file already exists, add the key and keep the rest. If it does not, this creates it on
macOS or Linux, from the workbench folder:

```bash
mkdir -p .claude
[ -e .claude/settings.json ] || printf '{\n  "claudeMdExcludes": ["%s/repos/**", "%s/tools/**"]\n}\n' "$(pwd -P)" "$(pwd -P)" > .claude/settings.json
```

Then run the probe again on each new version. Claude Code asks before an agent writes
into `.claude/`: approve that step or run the commands yourself.

Keep the path absolute. A relative pattern such as `**/repos/**` also matches the root `AGENTS.md`
when the workbench path contains a `repos` folder, and the entrypoint disappears without warning.
Use only letters, digits, `-`, `_`, `.`, and `/` in the workbench path, plus a drive prefix on
Windows, as in `C:/wb/repos/**`: other characters can break the JSON or the pattern.

`work/` stays out of this setting on purpose: the instructions of a repository you are changing
bind that work. Because Codex does not load them on demand, name them in every assignment.

The alternative is to keep `repos/` and `tools/` outside the workbench and grant access with
`--add-dir`. Claude Code then loads no `CLAUDE.md` files from them, unless
`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` is set. Its documentation says that `--add-dir`
still loads skills, commands, and agents from an added folder, as in Copilot CLI, so this is not
neutral access either. Prefer reading a reference outside the root by its path, and probe whichever
access you use before relying on it.

## Delegation

Observed with the same versions and settings.

| Need | Claude Code 2.1.305 | Codex 0.160.0 |
|---|---|---|
| Subagent | Agent tool, with a selectable model | Multi-agent feature, on by default, with a selectable model |
| Inherited instructions | The root instructions | The root instructions, when it runs in the root |
| Continue a session from another process | `claude -p --resume <id>` | `codex exec resume <id> -m <model>` |
| List sessions | `claude agents` | `codex agents` |
| Review a commit from a shell | `claude -p` with a review prompt | `codex exec review --commit <SHA> -m <model>`, which takes no prompt, or `codex exec -s read-only -m <model>` with one |

Without `-m`, `codex exec resume` returned to the configured default model. Claude Code kept the
session's model.

On Claude Code 2.1.316, neither `claude agents` nor the host's agent listing showed sessions
started with `claude -p` between their turns. A new Director still reached such a session: it found
the transcript under `~/.claude/projects/`, read it, and sent one message with
`claude -p --resume <id>`.

In the `workspace-write` sandbox, with no added writable roots or network access, `codex exec
resume` failed with `Operation not permitted`, and `claude -p` reported that it was not logged in.
If your probe shows the same, run those commands yourself outside the sandbox and give the Director
the result.

A subagent's inherited instructions include the Director's. It stays a delegate only because its
assignment says so, as [OPERATING.md](../OPERATING.md) requires.

## Model evidence

Observed with the same versions.

| Source | Where to read it | Label |
|---|---|---|
| Claude Code session | `message.model` on the turn's messages, in the transcript under `~/.claude/projects/` | *reported* |
| Claude Code subagent | `subagents/agent-*.jsonl` in the session's folder | *reported* |
| Codex session | `turn_context.model`, per turn, in the `rollout-*.jsonl` under `~/.codex/sessions/` | *reported* |
| Codex subagent | Its own rollout, with `parent_thread_id` | *reported* |
| Review bot on a pull request | What the integration documents or pins for that run. An account name alone proves nothing | *configured*, otherwise pending |

## GitHub Copilot

From documentation read on 2026-11-02, not exercised: the VS Code pages are dated 2026-10-28, and
GitHub's Copilot CLI pages carry no date. They are newer than VS Code 1.137.0, so older versions may
lack some settings, harnesses, or commands. Installed behavior takes precedence: run the probes
before relying on a line, then replace it with what you observed and the version.

VS Code runs each session in a harness: Local, Copilot, Claude, or Codex. A Copilot CLI session in
VS Code uses the Copilot harness, which shares its runtime with Copilot CLI. Instruction loading,
delegation, and permissions depend on the harness, so probe each harness you use as Director as a
separate host.

### Copilot: instruction loading

- The Copilot harness loads `AGENTS.md`, `.github/copilot-instructions.md`, and
  `.github/instructions/*.instructions.md`. Copilot CLI also loads `CLAUDE.md` and `GEMINI.md`, and
  combines all of them with no stated precedence. Keep one instruction file per folder.
- Both discover `AGENTS.md` in the folders from the repository root to the working directory, and
  Copilot CLI also in the folders on the path of the file it works on. No documented setting
  excludes a folder as `claudeMdExcludes` does: in Copilot CLI, `/instructions` turns single files
  off and `--no-custom-instructions` turns all of them off. Keep `repos/` and `tools/` outside the
  opened root until the subfolder probe passes.
- `chat.useNestedAgentsMdFiles` does not control the Copilot harness.
- In Copilot CLI, `--add-dir` also loads that folder's `.github/skills` and `.github/agents` as
  trusted configuration, so it does not give neutral access to a reference. That says nothing about
  what loads from a subfolder of the opened root: probe `.github/skills/` and `.github/agents/`
  there too.
- Evidence of a load: in VS Code, the system prompt in the Chat Debug view or the discovery events
  in Agent Debug Logs; the customizations editor shows only what was discovered. In Copilot CLI,
  `/env` and `/instructions`.

### Copilot: delegation and sessions

- A Local subagent inherits the main agent's instructions and tools, unless it runs a custom agent,
  but not the conversation, and it takes no follow-up messages. It cannot start subagents unless
  `chat.subagents.allowInvocationsFromSubagents` is on.
- A Copilot CLI subagent that runs a custom agent loads `AGENTS.md` and other instruction files
  only with `include-custom-instructions: true`; the default is `false`. Copilot CLI allows nested
  subagents. Name the instruction paths in every assignment, and say whether the worker may
  delegate.
- No page describes a notice to another session when a session finishes or waits for a
  confirmation. The session list shows its state; in Copilot CLI, so does `/tasks`.
- In VS Code, Copilot harness sessions in a separate worktree run with Allow all and show no
  confirmation prompts. There, only technical limits, such as disabled pushing or the sandbox, stop
  an action.

### Copilot: confirmations

- VS Code: `chat.tools.terminal.autoApprove` takes commands or `/regular expressions/`. A `false`
  rule wins over `true`, but it asks for approval rather than blocking. A compound command is
  approved only when every subcommand matches, and the parser may miss subcommands. Which settings
  scope wins is not documented. **Chat: Manage Tool Approval** reviews saved approvals and **Chat:
  Reset Tool Confirmations** clears them.
- Copilot CLI: `--allow-tool` and `--deny-tool` take patterns such as `shell(git status)`, and deny
  wins, also over `--allow-all`. `shell(git:*)` also matches `git push`. Approvals for a repository
  or folder persist in `~/.copilot/permissions-config.json`. `/permissions reset` clears the
  session's approvals, and `/reset-allowed-tools` also clears those saved for the current location.
- Hooks are in preview in VS Code. In Copilot CLI, a `preToolUse` hook that times out lets the call
  through, and the documentation says hooks do not replace permissions or sandboxing: do not use
  them as a control or to approve.

### Copilot: model and secrets

- VS Code shows the model of a response when you hover over it: *reported*. A custom agent's
  `model` is a preference list, so it is at most *configured*. Copilot CLI `/usage` gives per-model
  totals for the whole session, which attribute a turn only when one model ran the session.
- Copilot CLI redacts `GITHUB_TOKEN` and `COPILOT_GITHUB_TOKEN` from its output, and
  `--secret-env-vars` names more variables to redact. A redacted value in a trace is not evidence
  of what ran; do not reveal it to check.

## Other hosts

From their documentation, not exercised.

- **Gemini CLI:** it reads `GEMINI.md` by default. List `AGENTS.md` in `context.fileName` so it
  loads the entrypoint.
