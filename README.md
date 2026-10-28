# Agent Workbench

A small, Markdown-first foundation for coordinating coding agents across repositories and
information sources: one Director that delegates bounded work, independent cross-family review of
code changes, and private records that let work resume from another session.

It adds no runtime, scheduler, background service, database, dashboard, or installer. It relies
on the agent host you already have (first target: VS Code with GitHub Copilot on native Windows)
and on existing approved tools.

## Contents

| File | Purpose |
|---|---|
| [OPERATING.md](OPERATING.md) | Operating contract that every agent reads |
| [docs/VALIDATION.md](docs/VALIDATION.md) | Capability probes and acceptance procedure |
| [templates/](templates/) | Starting points for the workbench entrypoint and private files |

## Set up a workbench

1. Create a folder with a short path outside any Git repository, for example `C:/wb`. Short paths
   keep deep build trees within Windows path limits.
2. Place this repository at `core/` at a pinned revision, through the import route your
   organization approves.
3. Copy `core/templates/workbench-entrypoint.md` to `AGENTS.md` at the workbench root.
4. Create `private/` and copy `POLICY.md`, `workspace.json`, and `INDEX.md` into it. Create
   `private/tasks/` and `work/`.
5. Fill in `private/workspace.json` (approved sources, writable paths, pins) and
   `private/POLICY.md`. Both take effect only after the requester approves their exact content.
6. Open the workbench folder in VS Code and run the preflight probes in
   [docs/VALIDATION.md](docs/VALIDATION.md) that decide your next step.

```text
wb/                      # not a Git repository
  AGENTS.md              # entrypoint
  core/                  # this repository, pinned
  private/
    POLICY.md            # approved rules and preferences
    workspace.json       # approved scope and pins
    INDEX.md             # links to priorities, tasks, decisions, and sources
    tasks/               # one record per recoverable task
    dossiers/            # optional, from an adopted mapping tool
  work/                  # isolated writable copies, per task
```

Reference repositories stay where they are. Keep `private/` and `work/` out of this repository;
a `.gitignore` is not a substitute for that separation.

## Where information lives

| Information | Owner |
|---|---|
| Common behavior and role contracts | `core/OPERATING.md` |
| Approved personal or team rules and preferences | `private/POLICY.md` |
| Permitted scope, entrypoints, and pins | `private/workspace.json` |
| Priorities and links to tasks, decisions, and sources | `private/INDEX.md` |
| Coordination decisions, authorization, results, and next action | One record per task in `private/tasks/` |
| Capability observations and acceptance evidence | Task records for the validation runs |
| Detailed service maps from an adopted mapping tool | Its dossiers, referenced rather than copied |
| Product conventions and business state | Existing repositories and official systems |
| Whether an agent is running now | Current host evidence; a saved status is a dated observation |

## Optional integrations

[Toil](https://github.com/imagile-dev/toil) can provide service maps (dossiers), work-item
normalization, and briefings through its CLI. If you adopt it, keep its checkout outside the
workbench root, pin a revision, check its runtime requirement and your software approval first,
and declare its local side effects. Its UI is not required.

## Contributing to the core

- Keep everything generic and in English, with synthetic examples only: no organization names,
  internal addresses or paths, account identifiers, conversations, or operational records.
- Keep `OPERATING.md` short, about 2,500 words at most; move detail into documents read on demand.
- This repository has no `AGENTS.md` on purpose: inside a workbench, a nested `AGENTS.md` could be
  discovered as runtime instructions. For the same reason, the entrypoint template is named
  `workbench-entrypoint.md`. Contributor guidance lives here.
- Changes follow the Review section of `OPERATING.md`: a local commit, cross-family review of that
  exact SHA, and at most two correction rounds.
- Add an executable only for a demonstrated, repeated need, using built-in modules, portable
  paths, and tests of real failure modes on native Windows.

## Acknowledgements

The separation of coordination, execution, and review draws on concepts from
[Director Pattern](https://github.com/bladnman/director_pattern). No code is copied.

## License

Not chosen yet; to be decided before publication.
