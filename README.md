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
| [skills/](skills/) | Optional task stages as agent skills, from an idea to a merged change |

## Set up a workbench

You need Git, a login that can clone the repositories you will work on, and an agent host. Claude
Code must be 2.1.281 or later.

1. Create a folder with a short path, for example `~/wb` or `C:/wb`, outside any Git repository and
   below no folder with its own agent instructions.
2. Place this repository at `core/` at a pinned revision. With Git, from the workbench folder:
   `git clone --branch v0.7.0 https://github.com/adpablos/agent-workbench.git core`, note the
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
wb/                      # not a Git repository, or a local one of its own (see below)
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

### Where a rule of your own goes

- A rule a command can check goes in a script, with one line in `private/POLICY.md` that says
  when to run it. The agent runs it and fixes what it lists.
- A rule that needs reading goes where every session reads: `private/POLICY.md`, or the
  project's agent instructions when the rule belongs to that project.
- A skill is for a procedure the agent is sent to. A rule written only in a skill is read only
  when the agent opens the skill, and an economical model often does not.

### Keep a history of the workbench

Optional. To see what changed in your rules, agents, and notes, make the workbench folder a
local Git repository of its own: `git init` there, with a `.gitignore` that leaves out `core/`,
`work/`, any clone or tool kept inside the folder, and any folder of local settings with secret
values. `private/` is never shared: give the folder no remote, or only a private repository of
your own. Ask the agent to commit there after it changes the policy, an agent, or a skill.

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

Write `<workbench>` out as the folder's full path: a host may refuse a command whose path it
cannot read in advance, such as one built from a shell variable. A worktree shares the clone's
history, so it takes seconds and little space, and
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

## Task stages

Optional. `skills/` holds eight agent skills that take a development task through short stages.
Each stage is small enough to run in its own session, on the model that suits it:

| Skill | What the stage does | Suits |
|---|---|---|
| `shape` | Turns an idea into tasks the size of one ticket, by asking the requester | A strong model |
| `investigate` | Reproduces a reported failure, or answers a question by running the code, before any fix is planned | A strong model |
| `think` | Reads the ticket and the code, and writes a plan of closed steps in the task's note | A strong model |
| `do` | Carries out the plan, one commit per step, and stops only for what the requester must decide | A strong model; an economical one only once you have seen its changes pass `review` in your repositories |
| `review` | Reviews the change once, comparing each addition with its nearest neighbour; its findings become new steps of the plan | A strong model of another family |
| `ship` | Writes the pull request text, pushes once the requester approves it, and leaves the build to be checked | A model that writes well |
| `close` | After the merge, removes the copy and branch, follows the build, and archives the note | An economical model |
| `retro` | Every few tasks, reads what went wrong and what went well, and proposes improvements | A strong model |

The note in `private/tasks/` carries the state from one stage to the next. The stages are not
the cheaper way: measured on tickets that touch many files, with every stage on a strong
model, a ticket cost about four times what one session of that model cost (about $3 against
$0.90 at list prices, and 30 minutes against 10), and two blind reviewers, one of each model
family, each preferred the change of one session working from the contract alone in six
tickets of eight. What the stages add is the question before the code. On tickets with a
decision left out, they asked the requester in half of the runs and one session in none;
where only the requester had the answer, they asked every time, and one session chose by
itself and said so afterwards. With `do` on an economical model, one build in four was left
unfinished and one change in four passed a strong model's review.

Use the stages when the ticket leaves open a decision that neither the code nor a document
settles, when someone must see the plan before any code is written, or when the work passes
between sessions or people. For the rest, ask for the ticket directly and have `review` read
the change when it carries risk.

To install them, ask the agent: "Install the task stages by following `core/README.md`." It:

1. Copies the folders under `core/skills/` into the folder your host reads skills from:
   `.github/skills/` for GitHub Copilot, `.claude/skills/` for Claude Code, `.agents/skills/` for
   Codex. It copies them again after each update of the core, and changes none of them in place.
2. Defines one agent per model, in the host's own format, from `core/templates/agent.md`: GitHub
   Copilot reads `.github/agents/<name>.agent.md` and Claude Code `.claude/agents/<name>.md`.
   Without agents, every stage runs on the session's model.
3. Adds the Task stages section of `core/templates/POLICY.md` to `private/POLICY.md`, with your
   agents, shows you the exact text, and waits for your approval.
4. Runs the task stages probe in [docs/VALIDATION.md](docs/VALIDATION.md).

Then ask in ordinary words, such as "start this ticket", "go on", or "it is merged", or name a
stage, such as `/think ABC-123`. A session that is not the stage's agent starts that agent, or
tells you which one to select when the host cannot do that. A reply that ends with `Next:` and
a stage passes the turn to that stage, so one "go on" can take a planned task through `do`,
`review`, and the pull request text. The session always stops with the plan, at a question, at
a step it could not do, at review findings, and before a push. A reported failure starts with
"investigate this": the stage reproduces it before naming a cause, and `think` plans the fix
from its finding. When the policy says how to read a build's result, the next message after a
push checks the build, and `close` keeps the task open until the build of the merge has
finished. Shape an idea in a session of the planning agent itself: it is a conversation.
`retro` appends what the core could do better to `private/core-feedback.md`, without private
names; bring those lines to an issue here.

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
   previous revision as the rollback point, applies the steps the changelog lists, and copies
   `core/skills/` again where the workbench installed the task stages.
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
- Keep each skill to 600 words at most, with no model, host, or language of its own: those belong
  to the workbench's policy and agents. Quote its description; the `docs` check enforces both.
- Keep [docs/HOSTS.md](docs/HOSTS.md) to differences that change what a user does, each with the
  host version where it was observed.

## Acknowledgements

Earlier versions separated coordination, execution, and review following concepts from
[Director Pattern](https://github.com/bladnman/director_pattern). No code is copied.

## License

[MIT](LICENSE).
