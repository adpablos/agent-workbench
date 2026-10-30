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

Setting `instructionFiles` to `claude-md-and-agents-md` in user settings makes Claude Code load
both `CLAUDE.md` and `AGENTS.md`. Do not rely on it: it belongs to one person, so two people would
load different instructions. Keep one instruction file per folder instead.

To confirm a load on Claude Code, search the session transcript for the probe word. `CLAUDE.md`
forms appear as `nested_memory` entries and `AGENTS.md` as `hook_additional_context`.

### Claude Code: references inside the workbench

Because Claude Code loads subfolder instructions on demand, a reference repository's instructions
reach the Director as soon as it reads one of that repository's files. Without further settings
the subfolder probe fails. To keep `repos/` and `tools/` in the workbench, exclude them in
`.claude/settings.json` at the workbench root, with the workbench's real absolute path:

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

Then run the probe again. Claude Code asks before an agent writes into `.claude/`: approve that
step or run the commands yourself.

Keep the path absolute. A relative pattern such as `**/repos/**` also matches the root `AGENTS.md`
when the workbench path contains a `repos` folder, and the entrypoint disappears without warning.
Use only letters, digits, `-`, `_`, `.`, and `/` in the workbench path, plus a drive prefix on
Windows, as in `C:/wb/repos/**`: other characters can break the JSON or the pattern.

`work/` stays out of this setting on purpose: the instructions of a repository you are changing
bind that work. Because Codex does not load them on demand, name them in every assignment.

The alternative is to keep `repos/` and `tools/` outside the workbench and grant access with
`--add-dir`. Claude Code then loads no instructions from them, unless
`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` is set.

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

## Other hosts

From their documentation, not exercised.

- **GitHub Copilot in VS Code:** the root `AGENTS.md` is on by default. Discovery in subfolders
  depends on the session type and on the experimental `chat.useNestedAgentsMdFiles` setting.
- **Gemini CLI:** it reads `GEMINI.md` by default. List `AGENTS.md` in `context.fileName` so it
  loads the entrypoint.
