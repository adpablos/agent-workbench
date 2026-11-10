# Hosts

Where agent hosts differ in ways that change what you do. Read this only when setting up a
workbench, when a probe fails, or when you cannot tell how the host behaves.

Each line says what was observed and on which version, or that it comes from documentation. None
of it is a guarantee: the probes in [VALIDATION.md](VALIDATION.md) decide what is true in your
environment. One workbench can serve several hosts: they share `AGENTS.md`, and each ignores the
other's settings.

## Instruction loading

Observed on macOS from the command line, at default settings.

| Situation | Claude Code 2.1.305 | Codex 0.160.0 |
|---|---|---|
| Root `AGENTS.md` | Loaded, unless hidden. Its documentation says some sessions miss it before 2.1.281 | Loaded |
| Hidden by | A `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in that folder, or a `CLAUDE.md` in a folder above it. `~/.claude/CLAUDE.md` did not hide it | Not observed |
| Folder that is not a Git repository | Works | Asks to trust the folder; `codex exec` needs `--skip-git-repo-check` |
| Session started in a repository | Loads that repository's file and the workbench `AGENTS.md`, unless the repository has a `CLAUDE.md`, which hides both `AGENTS.md` files | Loads only that repository's file |
| Agent reads a file in a subfolder | Loads that subfolder's instructions on demand, also in subagents | Loads nothing |
| Names to probe | `CLAUDE.md`, `CLAUDE.local.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md`, `AGENTS.md` | `AGENTS.override.md`, `AGENTS.md`, any `project_doc_fallback_filenames` |

Skills and agents can also come from subfolders. Claude Code documents `.claude/skills/`,
`.claude/agents/`, and `.claude/commands/`, and Codex `.agents/skills/`; Copilot is covered below.
Probe every folder the installed version documents, since the lists grow. After the agent read a
file in a subfolder, Claude Code 2.1.316 loaded that folder's skills on demand, even with
`claudeMdExcludes` set for it; Codex 0.166.0 loaded nothing. This is why reference repositories and
tools stay outside the workbench folder; read them by their path. `--add-dir` is not neutral
access: Claude Code's documentation says it loads skills, commands, and agents from the added
folder. Repositories you change are cloned into `work/` on
purpose: their instructions bind that work. Because Codex does not load them on demand, name them
when you hand work to a Codex session.

To confirm a load on Claude Code, search the session transcript for the probe word, not for one
kind of entry: on 2.1.316, `AGENTS.md` appeared as an `instructions` attachment.

Every session also takes the user's own instruction files, skills, and tool servers. On Claude
Code 2.1.316, `claude -p "/context"` lists their tokens without a model call. Turn off for workbench
sessions what the work does not need, where the host allows it.

## Delegation and review

Delegating pays off only for independent work that can run in parallel, or for a bounded read that
returns a short answer; on coupled work, every delegate reads the repository and the contract again
and costs more than doing the work in one session. A review session is the usual exception, as
`OPERATING.md` (Review) describes. A subagent inherits the root instructions on both hosts below,
so its request must say that it is a reviewer or a delegate and what it may change.

Observed with Claude Code 2.1.305 and Codex 0.160.0.

| Need | Claude Code | Codex |
|---|---|---|
| Subagent | Agent tool, with a selectable model | Multi-agent feature, on by default, with a selectable model |
| Continue a session from another process | `claude -p --resume <id>` | `codex exec resume <id> -m <model>`; without `-m` it returned to the default model |
| Review a commit from a shell | `claude -p` with a review prompt | `codex exec review --commit <SHA> -m <model>`, which takes no prompt, or `codex exec -s read-only -m <model>` with one |

In the `workspace-write` sandbox, with no added writable roots or network access, `codex exec
resume` failed with `Operation not permitted`, and `claude -p` reported that it was not logged in.
If yours does the same, run those commands yourself outside the sandbox and give the session the
result.

Which model ran a session or a review, *reported* by the host:

| Source | Where to read it |
|---|---|
| Claude Code session or subagent | `message.model` in the transcript under `~/.claude/projects/`; subagents in `subagents/agent-*.jsonl` |
| Codex session or subagent | `turn_context.model`, per turn, in the `rollout-*.jsonl` under `~/.codex/sessions/` |
| Copilot CLI | Each `assistant.message` in the session record names its model |
| Review bot on a pull request | Only what the integration documents or pins for that run: *configured*. An account name alone proves nothing |

## GitHub Copilot

VS Code runs each session in a harness: Local, Copilot, Claude, or Codex. A Copilot CLI session in
VS Code uses the Copilot harness, which shares its runtime with Copilot CLI. Instruction loading,
delegation, and permissions depend on the harness, so probe each harness you use as a separate
host.

### Copilot CLI: observed

On macOS with Copilot CLI 1.0.84 installed from npm, without the interactive interface, at default
settings; 1.0.105 gave the same results.

- Pin the version: a CLI installed at 1.0.84 ran 1.0.105 from its package cache. Run
  `export COPILOT_AUTO_UPDATE=false` before the first command, or pass `--no-auto-update` to
  every command.
- Run a probe as `copilot -p "<prompt>" --deny-tool shell --deny-tool write --output-format json`
  from the workbench folder, and continue it with `--resume=<sessionId>`.
  `copilot -p "/compact" --resume=<sessionId>` compacts on request.
- The session record, `~/.copilot/session-state/<sessionId>/events.jsonl`, holds every tool call,
  what it returned, compaction, and on-demand instruction loads, each as a `system.notification`
  whose `kind.type` is `instruction_discovered`. Records grow to hundreds of kilobytes, so search
  them:

```bash
grep -c '<probe word>' ~/.copilot/session-state/<sessionId>/events.jsonl
grep -o '"instruction_discovered","sourcePath":"[^"]*"' ~/.copilot/session-state/<sessionId>/events.jsonl
```

- The root `AGENTS.md` loaded, and the agent read `core/OPERATING.md` and `private/POLICY.md` in
  full before the task's first operation.
- The subfolder probe failed: after the agent viewed a file in a subfolder, the CLI loaded that
  folder's `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `GEMINI.md`,
  `.github/copilot-instructions.md`, and `.github/instructions/*.instructions.md`. No skill or agent
  from a subfolder appeared. A folder outside the opened root, reached with `--add-dir` or
  `--allow-all-paths`, loaded no `AGENTS.md`.
- With the default `auto` model, turns of one session ran on different models. Pass `--model`
  when a probe needs one model.
- Usage: `totalNanoAiu` in the session record divided by 10^9 gives a session's AI credits at list
  price. Read it without a model call from the summary `copilot -p` prints at exit or from
  `session.shutdown` in the record; `copilot -p "/usage"` costs a turn. Each new session paid in
  full for about 12,000 tokens of system prompt, tool definitions, and `AGENTS.md`.
- The built-in GitHub MCP server added about 1,100 tokens to every call, and personal skills in
  `~/.agents/skills/` were offered in every session; one answered a workbench request in place of
  the contract. `copilot mcp disable <name>` and `copilot skill disable <name>` turn one off.
- Loading `core/OPERATING.md` through `.github/copilot-instructions.md` as well did not spare its
  read, and cost more.

### Copilot: from documentation

Read between 2026-11-02 and 2026-11-05, not exercised. Installed behavior takes precedence.

- The Copilot harness loads `AGENTS.md`, `.github/copilot-instructions.md`, and
  `.github/instructions/*.instructions.md`; Copilot CLI also `CLAUDE.md` and `GEMINI.md`, with no
  stated precedence. Keep one instruction file per folder. No setting excludes a folder.
- A Local harness subagent inherits the main agent's instructions and tools, not the
  conversation, and takes no follow-up messages. A Copilot CLI subagent that runs a custom agent
  loads instruction files only with `include-custom-instructions: true`. Name the instruction paths
  in every request to a subagent, and say whether it may delegate.
- A VS Code page dated 2026-11-04 says a Local harness subagent does not run when its model is in a
  higher cost tier than the main conversation's; it reports the models it can use instead. A
  reviewer that needs another or a stronger model gets its own session with that model selected.
- No page describes a notice to another session when a session finishes or waits; the session
  list shows its state, and in Copilot CLI so does `/tasks`.

Confirmations:

- VS Code: `chat.tools.terminal.autoApprove` takes commands or `/regular expressions/`. A `false`
  rule wins over `true` but asks rather than blocks. A compound command is approved only when every
  subcommand matches, and the parser may miss subcommands. **Chat: Manage Tool Approval** reviews
  saved approvals.
- Copilot CLI: `--allow-tool` and `--deny-tool` take patterns such as `shell(git status)`, and deny
  wins, also over `--allow-all`. `shell(git:*)` also matches `git push`. Approvals for a folder
  persist in `~/.copilot/permissions-config.json`; `/permissions reset` clears the session's.
- In VS Code, Copilot harness sessions in a separate worktree run with Allow all and show no
  confirmation prompts: only technical limits, such as disabled pushing or the sandbox, stop an
  action.
- Hooks are in preview in VS Code, and in Copilot CLI a `preToolUse` hook that times out lets the
  call through. Hooks are not a control and do not approve.

Model and reasoning effort:

- VS Code sets reasoning effort in the model picker, whose label shows it: *configured*; a new
  chat starts from the last effort chosen for that model. Hovering over a response shows its
  model: *reported*. A custom agent's `model` is a preference list, so at most *configured*.
- Copilot CLI sets the model with `--model` or `/model`, and the effort with `--effort` or
  `effortLevel` in `~/.copilot/settings.json` (default `medium`); an agent's `reasoningEffort` sets
  a subagent's. Each `assistant.message`
  in the session record names its model. `/usage` totals per model for the whole session.
- Copilot CLI redacts `GITHUB_TOKEN` and `COPILOT_GITHUB_TOKEN` from its output; a redacted value
  is not evidence of what ran.

## Other hosts

From their documentation, not exercised.

- **Gemini CLI:** it reads `GEMINI.md` by default. List `AGENTS.md` in `context.fileName` so it
  loads the entrypoint.
