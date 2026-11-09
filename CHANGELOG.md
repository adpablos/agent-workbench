# Changelog

User-visible changes to the core. Versions follow [Semantic Versioning](https://semver.org/).
Merging a pull request only adds to Unreleased. A release is its own pull request that closes
Unreleased, and its commit is tagged on `main` once a workbench passes acceptance in
[docs/VALIDATION.md](docs/VALIDATION.md). Once a merge leaves changes in Unreleased that workbenches
should receive, propose that release. Workbenches pin a release tag together with its commit.

## Unreleased

- **Breaking: one session does one task, under a 504-word contract.** The Director, worker
  sessions, roles, ownership transfer, and the routines built on them are gone. The session that
  does a task works with the requester directly. It acts without asking within its task and its own
  copy, and asks first, showing the exact action, before anything outside them. It gets an
  independent review only for a change with several parts or real risk, and waits for it within its
  turn. It is done when what was asked is done and verified, with optional work listed under Found,
  and keeps a short status note only when the work spans sessions. `OPERATING.md` is 504 words,
  from 2,812, and the entrypoint 150, from 284; the `docs` check caps them at 600, and 700 together.
  Measured with `evals/` on four scenarios, two runs each, against v0.3.0 in a single session: 36%
  less cost (US$42.11 against US$66.12) and 4 complete runs against 0, with no safety violation and
  an approved chart change in both runs of the scenario that needs one. It missed its own cost cap
  against a session with no core, US$31.41: its main sessions cost US$28.43, and a review session
  ran in all eight runs because the test policy set `review: fresh session`.
  `evals/reports/2026-11-candidate.md` has the detail.

  **Do to update**, from v0.2.0 or v0.3.0:

  1. Finish or close any Director and worker sessions first; they are not resumed.
  2. Update the core as the README says, keep a copy of your `AGENTS.md`, and replace it with
     `templates/workbench-entrypoint.md`, adding back your local lines.
  3. In `private/POLICY.md`, remove the Director row of the models table and any rule about
     Directors or coordinators, roles, delegation, or session ownership: a policy that keeps them
     brings them back. Keep the review pairing and the approved models.
  4. In each open record in `private/tasks/`, make a person its owner and drop Director and worker
     session handles.

  **Adopt when convenient:**

  - The shorter status note in `templates/task.md`; existing records keep working as they are.
  - Keep reference repositories and tool checkouts outside the workbench folder, listed in
    `private/workspace.json` and no longer writable. The README's layout has no `repos/` or
    `tools/`, since hosts load instruction files and skills from subfolders of the folder they open.
  - Run the entrypoint probe once with the new `AGENTS.md`.

  **Nothing to do for:** settings, which keep their values, including `review`; an `agents` line,
  which no longer applies and can go when you next edit the policy; approvals, the approval log,
  `private/workspace.json`'s format, and probes already passed. `private/INDEX.md` is optional.
  `docs/VALIDATION.md` keeps two probes, whether the entrypoint is loaded and followed and whether
  subfolders add instructions, and a short acceptance of a release; the Director probe, its kit in
  `probes/`, and the other probes are gone. `docs/HOSTS.md` says when delegation pays off, in one
  paragraph.
- `evals/` measures the core's way of working on real repositories: a service and the separate
  repository that configures its deployment, with tickets based on recent upstream fixes and
  hidden tests. It compares configurations of the core against a bare session and reports outcome,
  safety, continuity, cost, and friction from the host's records. A candidate core is one more
  configuration file. It is a development tool for the core: a workbench never reads it.
- `docs/HOSTS.md` records what Copilot CLI 1.0.84 showed: pin the version at every launch, since an
  npm install ran a newer cached version; find reads, compaction, and on-demand instruction loads in
  the session record; and read usage there without a model call. The entrypoint loaded and was
  read. Viewing a file in a subfolder loaded every instruction file there, and a folder outside the
  opened root loaded none. Each new session pays for about 12,000 tokens before its first answer,
  and personal skills and tool servers are offered in every session; one skill answered a workbench
  request in place of the contract.
- Before review, the diff is compared with the repository's existing patterns, and tests that
  protect nothing the change relies on are removed. Cleanup after a merge also checks for ignored
  files and commits that only a worktree's own refs reach; when a loss cannot be ruled out, the
  copy stays.
- The requester can approve an integration run against non-production services. The approval names
  the environment, endpoints and methods, copy, tools, credential mechanism, and where evidence is
  kept, and the run covers only what it names. Business-data changes, production, deployment,
  publication, and privileged operations keep their own approvals whatever the method. A newer,
  broader rule does not override an older explicit prohibition: both are reported.
  `docs/DEFAULTS.md` (Integration runs) has the detail.
- `private/POLICY.md` can stay short: a trigger, "Before <action>, read `private/<file>.md` in
  full", makes a topic file part of the policy, read in full before that action; a missing topic
  blocks the action. The approval log may move to one linked file, and its entries record scope,
  reason, and where the exact text was approved. Moving content out of the policy is itself a
  policy change. Existing policies need no migration.
- An optional `private/knowledge/`, from `templates/knowledge.md`, holds facts that several tasks
  reuse, such as a glossary, service relationships, and source locators. It is evidence, never
  instructions or authority.

## 0.3.0 - 2026-11-04

- A complete read of the files the entrypoint lists stays valid while it is visible in the current
  context and the file is unchanged. Agents read again at the start of a session or worker, after
  compaction or another context reset, when the earlier read is no longer visible, before taking
  over ownership, and after a file changed, but not on every request in the same context. The whole
  text of a file that the host puts in context counts as a read, also after compaction; a summary or
  a reference does not. `docs/HOSTS.md` records how Claude Code and Codex compact and how a record
  shows it. The entrypoint itself needs no separate read while its text is in context. Existing
  workbenches apply every change to the entrypoint template to their `AGENTS.md`, keeping their
  local additions: the removed "do not rely on an earlier reading" would otherwise contradict the
  new paragraph. The read probe checks a second request and a compaction.
- A copy is made only when the task needs one. The task record lists every copy, worktree, cache,
  kept output, and branch with its purpose and lifetime, and gives each a disposition before the
  task closes, merged or not: kept with a reason that outlives the task, or removed after the exact
  paths and refs were approved. `docs/PULL-REQUESTS.md` says how to prepare and verify cleanup after
  a merge; merge approval never authorizes it, and the README's step for adding a repository says to
  record the copy. Task records no longer need a date prefix.
- An assignment names where delivery ends, and when the next step needs an approval the agent does
  not have, it prepares that exact request instead of reporting the step it reached. For one task
  and one named repository, the requester can record in the task record that the agent pushes the
  reviewed branch and opens its pull request with text the agent writes. That never covers merging,
  releasing, tagging, force pushes, or skipping checks or review, never overrides a stricter policy,
  and a person still merges. Under it, a fixed head is reviewed before it is pushed.
- `docs/HOSTS.md` records what Claude Code 2.1.316 showed. `AGENTS.md` appears in the transcript as
  an `instructions` attachment, so a load is confirmed by searching for the probe word.
  `claude agents` does not list sessions started with `claude -p`; a new Director reaches one
  through its transcript and `--resume`.
- The subfolder probe also covers skills and agents: each folder a host recognizes for them gets one
  whose description asks for its own word. Claude Code 2.1.316 loaded the skills of a subfolder
  despite `claudeMdExcludes`, so on Claude Code `repos/` and `tools/` stay outside the workbench
  root; Codex 0.166.0 loaded nothing. Workbenches that kept them inside move them out and continue
  in a new session, since a session that already loaded their skills keeps them.

## 0.2.0 - 2026-11-02

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
- The documentation check no longer counts a CRLF line ending, so a 100-character line passes on a
  Windows checkout as it does elsewhere.
- A task record's owner is a session, named by its handle, or a person. A role such as "Director"
  leaves ownership uncertain, so a resuming Director reconciles it before writing.
- Merging a pull request does not make a release. Once a merge leaves changes in Unreleased that
  consumers should receive, the agent proposes the release, and that proposal stays as the task's
  next action until the requester decides. Full base acceptance runs once per host, for the first
  release accepted there. A later release runs only the checks that a table in `docs/VALIDATION.md`
  selects for the behaviors it changes; a change of wording alone needs only Core payload.

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
