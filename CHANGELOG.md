# Changelog

User-visible changes to the core. Versions follow [Semantic Versioning](https://semver.org/).
Merging a pull request only adds to Unreleased. A release is its own pull request that closes
Unreleased, and its commit is tagged on `main` once a workbench passes acceptance in
[docs/VALIDATION.md](docs/VALIDATION.md). Once a merge leaves changes in Unreleased that workbenches
should receive, propose that release. Workbenches pin a release tag together with its commit.

## Unreleased

- Updating the core moves it back only when the core itself breaks. When a probe fails because of
  the host, the workbench keeps the update and stops relying on what that probe established. In a
  repository that another team maintains, its conventions apply, and the practices that traits turn
  on only if that team adopts them. `templates/workspace.json` has a field for the core's release
  tag.
- An assignment's return route says where the worker leaves its result. The Director does not
  assume it is notified when a session finishes or waits. It tells the requester once what a
  waiting worker needs, continues other authorized work, and, once none remains, ends its turn
  instead of polling.
- Only people with the applicable authority approve. A message from another agent or session is
  not approval, whatever it claims, and a declared sender does not prove who wrote it.
- To get fewer confirmations, the agent proposes the narrowest rule the host supports as a
  permissions change and never grants one itself.
- A worker delegates only when its assignment allows it, and the agents it starts count toward the
  limit. A continuation reuses the same worker only where the host allows it.
- The entrypoint template says that a refused, truncated, or partial read is not a full read.
  Existing workbenches copy that sentence into their `AGENTS.md`.
- `docs/HOSTS.md` has a GitHub Copilot section, from its documentation and not yet exercised. It
  covers harnesses, instruction loading, delegation, confirmations, model evidence, and redacted
  secrets. Among other things, Copilot harness sessions in a separate worktree show no confirmation
  prompts, and a hook that times out does not stop a tool call.
- Merging a pull request does not make a release. Once a merge leaves changes in Unreleased that
  consumers should receive, the agent proposes the release. Full base acceptance runs once per
  host, for the first release accepted there. A later release runs only the checks that a table in
  `docs/VALIDATION.md` selects for what it changes; a change of wording alone needs only Core
  payload.

## 0.1.0 - 2026-10-30

- `docs/PULL-REQUESTS.md` defines what a pull request contains, the review request, what counts as
  a material finding and a verdict, how to answer findings, what later rounds cover, and what
  happens when the base moves.
- `docs/DEFAULTS.md` lists what the core does by default, with one-line settings in
  `private/POLICY.md` or a project's agent instructions, and a five-rule safety floor that takes a
  recorded waiver to change. Project practices such as the changelog and versioning apply according
  to what a project is, or is meant to be.
- Independent review is the floor; a different model family is the default way to get it. Rounds
  after the first review cover the earlier findings and the new diff, unless a project sets
  `re-review: full`. The report labels follow the conversation's language and can be turned off.
- Updating the core takes a project's `core-version`, then the latest tag, then the tip of `main`.
- The README explains how anyone can contribute, how to work with others, and that `main` stays
  usable.
- The core no longer assumes one host or operating system. `docs/HOSTS.md` records where Claude
  Code, Codex, and other hosts differ in instruction loading, delegation, and model evidence.
- A Claude Code workbench excludes `repos/` and `tools/` in `.claude/settings.json`, so that the
  instructions of reference repositories do not reach the Director. The subfolder probe now targets
  those folders, and it no longer accepts a clean reply as proof: an agent may ignore a file the
  host loaded.
- Assignments name the instruction files of each repository, and model evidence comes from the
  turn that did the work.
- The agent updates the core on request: it validates the candidate commit apart from the active
  core, activates exactly that commit after approval, and records the new and previous revisions
  in `workspace.json`.
- Reference clones and tool checkouts can live inside the workbench, in `repos/<project>/<repo>`
  and `tools/`, once a preflight probe shows that the host does not load instruction files from
  subfolders; until then they stay outside the opened root.
- Changes reach `main` only through reviewed pull requests that pass a documentation check of
  line width and relative links.
- First Markdown core: the operating contract, the validation procedure, templates for the
  entrypoint and private files, an agent-guided setup, and the MIT license.
