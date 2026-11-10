# Agent Workbench

A small, Markdown-first foundation for working with coding agents across repositories and
information sources: one session per task that works with you directly, independent review of
changes that carry risk, and a short status note when work spans sessions.

It adds no runtime, scheduler, background service, database, dashboard, or installer. It relies
on the agent host you already have, such as Claude Code, Codex, or GitHub Copilot in VS Code, and
on existing approved tools.

## Contents

| File | Purpose |
|---|---|
| [OPERATING.md](OPERATING.md) | Operating contract that every agent reads |
| [docs/DEFAULTS.md](docs/DEFAULTS.md) | Configurable defaults and the safety floor |
| [docs/HOSTS.md](docs/HOSTS.md) | Where agent hosts differ, read only when needed |
| [docs/PULL-REQUESTS.md](docs/PULL-REQUESTS.md) | What a pull request contains and how its review ends |
| [docs/VALIDATION.md](docs/VALIDATION.md) | Probes and how a release is accepted |
| [templates/](templates/) | Starting points for the workbench's `AGENTS.md` and private files |
| [evals/](evals/) | Development tool for the core: measures a candidate on real repositories. A workbench never reads it |

## Set up a workbench

You need Git, a login that can clone the repositories you will work on, and an agent host. Claude
Code must be 2.1.281 or later.

1. Create a folder with a short path, for example `~/wb` or `C:/wb`, outside any Git repository and
   below no folder with its own agent instructions.
2. Place this repository at `core/` at a pinned revision. With Git, from the workbench folder:
   `git clone --branch v0.4.0 https://github.com/adpablos/agent-workbench.git core`, note the
   revision that `git -C core rev-parse HEAD` prints, and disable pushing from the workbench:
   `git -C core remote set-url --push origin DISABLED`. If your organization restricts imports, use
   its approved route.
3. Open the workbench folder in your agent host, accept its prompt to trust the folder if it shows
   one, and ask the agent: "Set up this workbench by following `core/README.md`." It performs the
   remaining steps with you; you can also perform them by hand.
4. Copy `core/templates/workbench-entrypoint.md` to `AGENTS.md` at the workbench root. The host
   loads it, and it points every agent to the rules. Add no other instruction file at the root.
   Create `private/` with `POLICY.md`, `workspace.json`, and `INDEX.md` from `core/templates/`, and
   create `private/tasks/` and `work/`. Create only what is missing; never overwrite a file.
5. Complete `private/POLICY.md` (review pairing, approved models, preferences) and
   `private/workspace.json` (approved sources, writable paths, pins). Read what the environment
   shows without changing it, such as tool versions. Ask the requester only for the rest, in one
   short list that includes the name or role to record as approver.
6. Show the exact content of `POLICY.md` and `workspace.json`. They take effect only after the
   requester approves that content; then record the approval date and approver in each.
7. In a new chat, run the probe in [docs/VALIDATION.md](docs/VALIDATION.md) that shows whether the
   entrypoint is loaded and followed.

```text
wb/                      # not a Git repository
  AGENTS.md              # entrypoint, from core/templates/workbench-entrypoint.md
  core/                  # this repository, pinned
  private/
    POLICY.md            # approved rules and preferences
    workspace.json       # approved sources, writable paths, and pins
    tasks/               # status notes for work that spans sessions
    INDEX.md             # priorities and links, read when resuming
    <topic>.md           # optional, policy topics that POLICY.md triggers
    knowledge/           # optional, facts several tasks reuse, from core/templates/knowledge.md
  work/                  # your writable copies, one folder per task
```

Reference repositories and tool checkouts stay outside the workbench folder, wherever they already
are, and `private/workspace.json` lists them. Hosts load instruction files and skills from
subfolders of the folder they open, so a reference inside it would add its instructions to every
session that reads one of its files; the subfolder probe in
[docs/VALIDATION.md](docs/VALIDATION.md) shows it. Keep `private/` and `work/` out of this
repository; a `.gitignore` is not a substitute for that separation.

### Add a repository

Clone the repository once, outside the workbench folder, and list that clone in
`private/workspace.json` with the requester's approval and `"access": "read, task worktrees"`. Its
files stay read-only and on its default branch; that access lets a session fetch there and add or
remove a task's worktree and branch, which writes only to the clone's Git metadata. A task works in
a worktree of it, on its own branch:

```bash
git -C <clone> fetch origin
git -C <clone> worktree add <workbench>/work/<task>/<repo> -b <branch> origin/<default branch>
```

A worktree shares the clone's history, so it takes seconds and little space, and
`git -C <clone> worktree list` shows every open copy. The clone's own default branch may fall
behind; that is harmless, since copies start from `origin/<default branch>`.
[templates/POLICY.md](templates/POLICY.md) carries these rules as preferences. The requester
saying that a task's change is merged or dropped approves removing that task's copy and branch,
after the After merge checks in [docs/PULL-REQUESTS.md](docs/PULL-REQUESTS.md), so `work/`
holds only open tasks. A dropped change has no merge to verify, and anything the checks would lose,
such as commits on no other branch, keeps the copy until the requester decides; nothing is forced.

Without a listed clone, `git clone <repository URL> work/<task>/<repo>` still gives a task its copy,
and copies already made that way keep working. A workbench whose host cannot write to a folder
outside it lists no clone and leaves those preferences out of its policy.

To review what is open, ask the agent: it lists each clone's worktrees and the folders under
`work/` with the state of each branch, proposes the exact removals, and removes nothing before
you approve them.

## Update the core

Ask the agent: "Update the core by following `core/README.md`." From the workbench folder, it:

1. Runs `git -C core fetch --tags` and takes, by its full SHA, the revision in the project's
   `core-version` setting, otherwise the latest release tag, otherwise the tip of the remote default
   branch, as the candidate. `main` means `origin/main`, never a local branch.
2. Shows you the SHA and the changelog entries since the revision pinned in
   `private/workspace.json`, including any step the entrypoint or the private files need, and
   waits.
3. After your approval, runs `git -C core checkout --detach <SHA>` and confirms that
   `git -C core rev-parse HEAD` prints that SHA; `git pull` could add commits you did not see. It
   records the SHA, and its release tag if it has one, in `private/workspace.json`, with the
   previous revision as the rollback point, and applies the steps the changelog lists.
4. If a path that the entrypoint or the private files rely on is gone, it moves the core back to
   the previous revision and restores the pin.

A release tag in `core-version` keeps everyone on a project on the same commit.

## Work with others

Each person keeps their own workbench; `private/` is never shared. Shared rules live in the
project's repository, as settings in its agent instructions, and shared work lives in that
repository and its pull requests. The repository must make sense without a workbench.

## Contributing to the core

Anyone can contribute, and you need neither a workbench nor a particular agent. Open an issue to
discuss a larger change, or fork the repository and open a pull request against `main`. The
`docs` check must pass; the maintainer arranges the independent review of your final commit, and
you answer any findings.

- Keep everything generic and in English, with synthetic examples only: no organization names,
  internal addresses or paths, account identifiers, conversations, or operational records. The
  core is installed where nothing else is: no rule or example may rely on its author's setup.
- Keep `OPERATING.md` to 600 words at most, and it and the entrypoint together to 700; the `docs`
  check enforces both. Move detail into documents read on demand.
- This repository has no `AGENTS.md` or `CLAUDE.md` on purpose: inside a workbench, a nested
  instruction file could be discovered as runtime instructions. For the same reason, the
  entrypoint template is named `workbench-entrypoint.md`. Contributor guidance lives here.
- Changes reach `main` only through pull requests, and each one leaves `main` usable. A reviewer
  from another model family reviews the exact head, with at most two correction rounds.
- Note each user-visible change under Unreleased in [CHANGELOG.md](CHANGELOG.md).
- Add an executable only for a demonstrated, repeated need, using built-in modules, portable
  paths, and tests of real failure modes on each platform it supports.
- Keep [docs/HOSTS.md](docs/HOSTS.md) to differences that change what a user does, each with the
  host version where it was observed.

## Acknowledgements

Earlier versions separated coordination, execution, and review following concepts from
[Director Pattern](https://github.com/bladnman/director_pattern). No code is copied.

## License

[MIT](LICENSE).
