# Agent Workbench

A small, Markdown-first foundation for coordinating coding agents across repositories and
information sources: one Director that delegates bounded work, independent cross-family review of
code changes, and private records that let work resume from another session.

It adds no runtime, scheduler, background service, database, dashboard, or installer. It relies
on the agent host you already have, such as Claude Code, Codex, or GitHub Copilot in VS Code, and
on existing approved tools.

## Contents

| File | Purpose |
|---|---|
| [OPERATING.md](OPERATING.md) | Operating contract that every agent reads |
| [docs/VALIDATION.md](docs/VALIDATION.md) | Capability probes and acceptance procedure |
| [docs/DEFAULTS.md](docs/DEFAULTS.md) | Configurable defaults and the safety floor |
| [docs/HOSTS.md](docs/HOSTS.md) | Where agent hosts differ in setup, delegation, and evidence |
| [templates/](templates/) | Starting points for the workbench's `AGENTS.md` and private files |

## Set up a workbench

You need Git, a login that can clone the repositories you will work on, and an agent host. Claude
Code must be 2.1.281 or later.

1. Create a folder with a short path, for example `~/wb` or `C:/wb`, outside any Git repository and
   below no folder with its own agent instructions. On Windows, a short path also keeps deep build
   trees within path limits.
2. Place this repository at `core/` at a pinned revision. With Git, from the workbench folder:
   `git clone https://github.com/adpablos/agent-workbench.git core` (without `core`, the folder
   takes the repository's name), note the revision that `git -C core rev-parse HEAD` prints, and
   disable pushing from the workbench: `git -C core remote set-url --push origin DISABLED`. If your
   organization restricts imports, use its approved route.
3. Open the workbench folder in your agent host, accept its prompt to trust the folder if it shows
   one, and ask the agent: "Set up this workbench by following `core/README.md`." It reads
   `core/OPERATING.md` and performs the remaining steps with you; you can also perform them by
   hand.
4. Copy `core/templates/workbench-entrypoint.md` to `AGENTS.md` at the workbench root. This is the
   workbench's entrypoint: the host loads it, and it points every agent to the rules. Add no other
   instruction file at the root. Create `private/`, copy `POLICY.md`, `workspace.json`, and
   `INDEX.md` into it, and create `private/tasks/` and `work/`. If you may use Claude Code here,
   also create `.claude/settings.json` as
   [docs/HOSTS.md](docs/HOSTS.md#claude-code-references-inside-the-workbench) describes. Create
   only what is missing; never overwrite an existing file.
5. Complete `private/POLICY.md` (review pairing, approved models, local preferences),
   `private/workspace.json` (approved sources, writable paths, pins), and one task record per
   initial priority, linked from `private/INDEX.md`. Read what the environment shows without
   changing it, such as tool versions. Ask the requester only for the rest, in one short list that
   includes the name or role to record as approver, and use any answers they have already
   prepared. Do not ask again for what `OPERATING.md` covers.
6. Show the exact content of `POLICY.md` and `workspace.json`. They take effect only after the
   requester approves that content; then record the approval date and approver in each.
7. Run the preflight probes in [docs/VALIDATION.md](docs/VALIDATION.md) that decide your next step,
   on each host you use. The first one, in a new chat, shows whether `AGENTS.md` is loaded.

```text
wb/                      # not a Git repository
  AGENTS.md              # entrypoint, from core/templates/workbench-entrypoint.md
  .claude/settings.json  # Claude Code only, see docs/HOSTS.md
  core/                  # this repository, pinned
  private/
    POLICY.md            # approved rules and preferences
    workspace.json       # approved scope and pins
    INDEX.md             # links to priorities, tasks, decisions, and sources
    tasks/               # one record per recoverable task
    dossiers/            # optional, from an adopted mapping tool
  repos/                 # read-only reference clones, as <project>/<repo>
  tools/                 # pinned checkouts of tools you run
  work/                  # isolated writable copies, per task
```

Existing reference repositories may stay where they are. Clone new ones into `repos/` only when a
task needs them, mirroring the remote: a service map, not the folder layout, records how they
relate. If a tool writes to the repositories it finds, point it at `work/<task>/`, never at a
reference. Use `repos/` and `tools/` only once the subfolder probe in
[docs/VALIDATION.md](docs/VALIDATION.md) passes; until then, keep both folders outside the
workbench root. Keep `private/` and `work/` out of this repository; a `.gitignore` is not a
substitute for that separation.

### Add a repository

From the workbench folder, clone a read-only reference into `repos/`, and add it to the sources in
`private/workspace.json` with the requester's approval:

```bash
git clone <repository URL> repos/<project>/<repo>
git -C repos/<project>/<repo> remote set-url --push origin DISABLED
```

For each task that changes it, clone a writable copy from the same URL into `work/`. Its `origin`
stays the remote, so it can publish a branch once that is authorized:

```bash
git clone <repository URL> work/<task>/<repo>
```

## Update the core

Ask the agent: "Update the core by following `core/README.md`." From the workbench folder, it:

1. Runs `git -C core fetch --tags` and takes, by its full SHA, the revision in the project's
   `core-version` setting, otherwise the latest release tag, otherwise the tip of the remote default
   branch, as the candidate. `main` means `origin/main`, never a local branch. If two projects
   require different versions, it reports the conflict: each workbench has one core, so use one
   workbench per version.
2. Checks the candidate out apart from the active core:
   `git -C core worktree add --detach ../work/core-update <SHA>`.
3. Validates it there: changelog entries and changed files since the revision pinned in
   `private/workspace.json`, the core paths that the entrypoint and private files rely on, and new
   template fields or probes. It shows you the SHA, the changes, and the result, and waits.
4. After your approval, activates exactly that commit with `git -C core checkout --detach <SHA>`,
   which also works for a tag older than the active core, and confirms that
   `git -C core rev-parse HEAD` prints that SHA; `git pull` could add commits you did not see. It
   records the SHA, and its release tag if it has one, in `private/workspace.json` with the previous
   revision as the rollback point, and removes the candidate with
   `git -C core worktree remove ../work/core-update`.
5. Reruns the preflight probes that the changes affect. If one fails, it moves the core back to
   the previous revision, restores that revision as the pin in `private/workspace.json`, and
   reports.

A different candidate needs its own validation and approval. Prefer this procedure to editing the
pin by hand.

`main` stays usable, so a project can follow it before a release exists. People on the same project
may then sit on different commits; a release tag in `core-version` keeps them identical.

## Change the defaults

The core ships with defaults you can change with one line: report format, changelog, versioning,
review, and more. [docs/DEFAULTS.md](docs/DEFAULTS.md) lists them, says when each applies, and
describes the small safety floor that takes a recorded decision to change. Ask the agent to "show
the settings" to see what applies now.

## Work with others

Each person keeps their own workbench; `private/` is never shared. Shared rules live in the
project's repository, as settings in its agent instructions, and shared work lives in that
repository and its pull requests. The repository must make sense without a workbench.

## Where information lives

| Information | Owner |
|---|---|
| Common behavior and role contracts | `core/OPERATING.md` |
| Defaults, settings, and the safety floor | `core/docs/DEFAULTS.md` |
| Settings that change what a project delivers | That project's agent instructions |
| Approved personal rules and preferences | `private/POLICY.md` |
| Permitted scope, entrypoints, and pins | `private/workspace.json` |
| Priorities and links to tasks, decisions, and sources | `private/INDEX.md` |
| Coordination decisions, authorization, results, and next action | One record per task in `private/tasks/` |
| Capability observations and acceptance evidence | Task records for the validation runs |
| Detailed service maps from an adopted mapping tool | Its dossiers, referenced rather than copied |
| Product conventions and business state | Existing repositories and official systems |
| Whether an agent is running now | Current host evidence; a saved status is a dated observation |

## Optional integrations

[Toil](https://github.com/imagile-dev/toil) can provide service maps (dossiers), work-item
normalization, and briefings through its CLI. If you adopt it, keep a pinned checkout in `tools/`,
check its runtime requirement and your software approval first, and declare its local side
effects. Its UI is not required.

## Contributing to the core

Anyone can contribute, and you need neither a workbench nor a particular agent. Open an issue to
discuss a larger change, or fork the repository and open a pull request against `main`. The
`docs` check must pass; the maintainer arranges the independent review of your final commit, and
you answer any findings.

- Keep everything generic and in English, with synthetic examples only: no organization names,
  internal addresses or paths, account identifiers, conversations, or operational records.
- Keep `OPERATING.md` short, about 2,500 words at most; move detail into documents read on demand.
- This repository has no `AGENTS.md` or `CLAUDE.md` on purpose: inside a workbench, a nested
  instruction file could be discovered as runtime instructions. For the same reason, the
  entrypoint template is named `workbench-entrypoint.md`. Contributor guidance lives here.
- Changes reach `main` only through pull requests, and each one leaves `main` usable. A reviewer
  from another model family reviews the exact head, as in the Review section of `OPERATING.md`,
  with at most two correction rounds.
- Note each user-visible change under Unreleased in [CHANGELOG.md](CHANGELOG.md).
- Add an executable only for a demonstrated, repeated need, using built-in modules, portable
  paths, and tests of real failure modes on each platform it supports.
- Keep [docs/HOSTS.md](docs/HOSTS.md) to differences that change what a user does, each with the
  host version where it was observed.

## Acknowledgements

The separation of coordination, execution, and review draws on concepts from
[Director Pattern](https://github.com/bladnman/director_pattern). No code is copied.

## License

[MIT](LICENSE).
