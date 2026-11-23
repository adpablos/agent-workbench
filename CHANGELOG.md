# Changelog

User-visible changes to the core. Versions follow [Semantic Versioning](https://semver.org/).
Merging a pull request only adds to Unreleased. A release is its own pull request that closes
Unreleased, and its commit is tagged on `main` once a workbench passes acceptance in
[docs/VALIDATION.md](docs/VALIDATION.md). Once a merge leaves changes in Unreleased that workbenches
should receive, propose that release. Workbenches pin a release tag together with its commit.

## Unreleased

- **The build stops only for a decision.** `do` now stops only for what the requester must
  decide: a step that is unclear or cannot be done as written, or a change the ticket and the
  plan's Goal do not settle. What they settle it repairs and names under Snags: a file the
  step needs but does not name, an existing test that asserts what the ticket changes, a
  check that passes only after a later step. A check the machine cannot run is named as not
  verified, and what no step or failing check needs is named, not changed. Before, it
  stopped at each of these. Measured on eight changes, two sets of runs: 1 and 3 stops per
  eight tickets against 12 and 15, and every ticket finished against 7 and 5 of eight. On
  the next model of the same family, two more sets: 2 and 2 stops, every ticket finished.
  The stops left ask for an exact text the ticket gives and the plan did not quote.
- **Shipping with findings open.** `ship without review` on a task whose note lists open
  findings, or whose plan has review steps not done, now records
  `open findings, accepted by the requester` in the note and lists each of them at the end of
  the pull request description; a description saved before the findings were accepted is
  written again. Before, the note said the review was skipped and the description could
  leave the findings out.
- **A push the policy approves in advance.** When a line of the policy approves pushing a
  repository's task branch in advance, as `docs/DEFAULTS.md` shows, `ship` pushes without
  asking for `Approved`, and opens the pull request if the line covers it. Before, `ship` asked
  every time.
- **Later review rounds.** `review` now does what `docs/PULL-REQUESTS.md` (Rounds after the
  first) says. When it finds something it keeps the reviewed commit and the round in the note's
  Reviewed line; the next round reads the diff since that commit and the review steps; from
  round 3 it adds no steps, lists the open findings in the note and hands them to the
  requester. Before, every round read the whole change and no round was the last. The
  document no longer names a `P0` the stage does not use.
- **Every review round runs the repository's checks.** `review` runs the checks the
  repository's pipeline runs before it reads; before, it could. A failure the change causes
  is a finding; a check the machine cannot run is named as not verified, not made a step.
  It stops when the task's copy has changes not committed, so the checks run on the commit
  it reviews. In a later round a finding counts as resolved only after reading what else its
  fix changes, and the round reads the open findings of the last one too.
  Measured on eight changes: reviewers that did not run the type check missed a build that
  failed, and two called resolved a fix that broke the case next to it.
- **Review steps name every file.** A step that `review` adds names every file its fix touches,
  the test included, so `do` does not stop to ask whether it may change a test.
- **`shape` shows directions.** For an idea with no chosen way, `shape` first shows two or three
  different directions with its recommendation, and asks which. An idea whose way is chosen
  goes on as before.
- **What the stages cost and what they add.** The README no longer presents the stages as the
  cheaper way, and says when they earn their cost. Measured on tickets of many files, with
  every stage on a strong model, a ticket cost about four times what one session of that
  model cost (about $3 against $0.90 at list prices, 30 minutes against 10), and two blind
  reviewers, one of each model family, each preferred the change of one session working from
  the contract in six of eight. On tickets with a decision left out, the stages asked the
  requester before any code in half of the runs and one session in none. `do` on an
  economical model left one build in four unfinished, and one change in four passed a strong
  model's review: the README and the policy template now give `do` a strong model. Use the
  stages when a decision is written nowhere, when someone must see the plan first, or when
  the work passes between sessions or people.
- **Policy template.** A stage passes the turn only to a stage whose agent the session can
  start; an agent on another host is started from a shell with the command its line gives; a
  task can start from the pushed branch of a task not merged yet.
- **The entrypoint no longer says the folder is not a Git repository.** The README lets it keep
  a local history of its own; the entrypoint now says it is not a project's repository.
- **Forced removal after merge, stated once.** `docs/PULL-REQUESTS.md` said never to force, while
  `close` forces a removal the requester approved after seeing what would be lost. The document
  now carries that one case.
- **Where a rule of your own goes.** The README now says it: a rule a command can check, in a
  script with one policy line; a rule that needs reading, in the policy or the project's agent
  instructions; not in a skill. Measured on two models, a rule written only in a skill was
  the one place an economical model did not follow.
- **The workbench's history may have a private remote.** The README said to give it no remote;
  it now allows a private repository of your own.
- **`evals/` removed.** The kit measured configurations of v0.4.0 and was not kept up with
  later releases, so it said nothing about the current core. Candidates are now measured
  outside this repository; the kit stays in the history up to v0.7.0.
- **Hosts.** `docs/HOSTS.md` says what a session is offered with and without isolation on Claude
  Code and Codex, how to run one stage from the command line, how one Claude Code chat runs
  every stage across both hosts, and what breaks it.

## 0.7.0 - 2026-11-20

- **Planning decides by where things belong.** `think` now reads further before it decides:
  the code the change touches, what calls it, where each thing it uses comes from, and, when
  the ticket depends on another part or repository, how that part provides what the ticket
  needs. It names the ways to meet the ticket and judges each by where things belong: each
  job the change needs done goes to the part of the repository that already does that kind of
  job, and each thing from another part is taken from the part that produces it. That a part
  can reach a thing, or that doing a job in place is smaller, is no reason. Only then it
  picks the smallest way that fits. The note has a new Approach section with the way chosen,
  the ways left and why, and the part that does each job; the reply names the way chosen. The
  rules for the shape of a plan's steps moved from the stage to the note's template.
- **Planning asks less.** `think` stops for the requester only when the ticket can be read in
  two ways that change what its user gets, or needs something it cannot reach. It also stops
  when the ticket's author may not know what the code shows: the ticket asks for something the
  code or its tests forbid on purpose and does not name that rule, or it leaves open what
  becomes of data already stored, or a new dependency or service. Then it says what it found
  and asks. Every other choice it makes itself and names in the reply, so the requester can
  change it before any code is written. A thing with no example in the repository is built
  from what the repository already uses, and a repository without tests for similar code gets
  none planned.
- **Review checks it too.** `review` lists under Form each thing the change takes from another
  part and the part that produces it. A thing taken through a part that does not produce it is
  a finding rated `P2` or higher.

## 0.6.0 - 2026-11-19

- **A stage for incidents and questions: `investigate`.** A reported failure, or a question
  about how the system behaves, now starts with its own stage. It creates the task's copy, runs
  the code, and names a cause only after it has seen the failure itself; when it cannot
  reproduce it, it says what it ran and what it needs, and stops. It changes no product code
  and leaves a Finding in the task's note (reported, reproduced, cause, not checked) that
  `think` plans the fix from. A task without a ticket takes a short local name: `investigate`
  chooses one, and `shape` writes one for a task the requester says will have no ticket.
- **The build is followed.** When the policy says how to read a build's result, `ship` marks
  the pushed commit's build as running, the next message about the task checks it first, and
  `close` reads the build of the merge and what the merge sets off, such as a deployment. It
  keeps the note open with `Waiting for the build` until that finishes, and shows the failing
  lines when it fails. Without that policy line nothing changes.
- **Review compares form, in writing.** `review` no longer answers from memory whether the
  change does something another way: it lists in the note, under Form, each thing the change
  adds, the nearest existing one of its kind, and whether they match. A difference the ticket
  did not ask for is a finding rated `P2` or higher, so it comes back as a step.
- **Local settings with secret values.** The contract still forbids writing secrets into files,
  and now also asking for them. A policy can name local files that only the requester fills in,
  to run a component on the machine against a test environment; an agent never opens, prints,
  or commits them.
- The README says how to keep a local history of the workbench's own files, and
  [docs/HOSTS.md](docs/HOSTS.md) records when a subagent in VS Code's newer harness cannot
  write files.

  **Do to update:** copy `core/skills/` again; there is a new folder, `investigate`. In
  `private/POLICY.md`, with the requester's approval of the exact text: add `investigate` to
  the planning agent's stages and to the sentence that lists the stages, and add the paragraph
  about the Build line, both from the Task stages section of `templates/POLICY.md`; optionally
  add its two new preferences, `A build's result` and `Local settings`. `templates/task.md`
  gained a Build line and a Form section; notes you already keep need no change.

## 0.5.0 - 2026-11-16

- **Task stages, as optional skills.** `skills/` adds seven agent skills that take a development
  task through short stages: `shape` turns an idea into tasks the size of one ticket, `think`
  writes a plan of closed steps in the task's note, `do` carries it out with one commit per step
  and stops when a step is unclear, `review` reviews once and turns its findings into new steps,
  `ship` writes the pull request text and pushes after the requester approves it, `close` cleans
  up after the merge, and `retro` reads what went wrong and what went well every few tasks. The
  note carries the state between stages, so each can run in its own session on the model that
  suits it: a strong model plans and reviews, an economical one does the rest. A session asked
  in ordinary words finds the next stage from the note and starts the stage's agent, or says
  which agent to select; it goes on from stage to stage until it needs the requester: with the
  plan, at a question, at a step it could not do, at review findings, and before a push.
  `retro` collects, without private names, what the core could do better in
  `private/core-feedback.md`. The contract does not change: a workbench that installs nothing
  works as before. Rehearsed on Copilot CLI 1.0.105 and in VS Code 1.137.0 with four models,
  and on Codex CLI 0.166.0 with one; the README (Task stages) says how to install them and
  [docs/HOSTS.md](docs/HOSTS.md) what was observed.

  **Do to update:** nothing is required. To use the stages, follow the README (Task stages):
  copy `core/skills/` into your host's skills folder, define your agents from
  `templates/agent.md`, and add the Task stages section of `templates/POLICY.md` to your policy.
  `templates/task.md` gained the lines the stages use (Reviewed, Pull request, Plan, Pull
  request text, Snags, Worked); notes you already keep need no change. A workbench that used
  prompt files for stages of its own replaces them with these skills, since VS Code runs prompt
  files only in the harness it is retiring.

## 0.4.0 - 2026-11-09

- **Breaking: one session does one task, under a 531-word contract.** The Director, worker
  sessions, roles, ownership transfer, and the routines built on them are gone. The session that
  does a task works with the requester directly. It acts without asking within its task and its own
  copy, and asks first, showing the exact action, before anything outside them, unless the
  request names that action or the policy approves it in advance. It gets an
  independent review only for a change with several parts or real risk, and waits for it within its
  turn. It is done when what was asked is done and verified, with optional work listed under Found,
  and keeps a short status note only when the work spans sessions. `OPERATING.md` is 531 words,
  from 2,510 in v0.3.0, and the entrypoint 150, from 284; the `docs` check caps them at 600, and
  700 together.

  **Do to update**, from v0.2.0 or v0.3.0:

  1. Finish or close any Director and worker sessions first; they are not resumed.
  2. Update the core as the README says, keep a copy of your `AGENTS.md`, and replace it with
     `templates/workbench-entrypoint.md`, adding back your local lines.
  3. In `private/POLICY.md`, remove the Director row of the models table and any rule about
     Directors or coordinators, roles, delegation, or session ownership: a policy that keeps them
     brings them back. Keep the review pairing and the approved models, and add the private-data
     line of `templates/POLICY.md` (Preferences): the contract covers secrets, not other private
     data.
  4. In each open record in `private/tasks/` and in `private/INDEX.md`, make a person the owner
     and drop Director and worker session handles.

  **Adopt when convenient:**

  - The shorter status note in `templates/task.md`; existing records keep working as they are.
  - The models table of `templates/POLICY.md`: task session, review session, and an optional
    delegated bounded read.
  - A topic trigger that names a core document, such as reading `core/docs/PULL-REQUESTS.md` before
    opening, reviewing, or merging a pull request: the contract itself does not point to it.
  - The `description` of `templates/workspace.json`: a source, path, or tool not listed is outside
    the scope.
  - Keep reference repositories and tool checkouts outside the workbench folder, listed in
    `private/workspace.json`, and drop `repos` from its `writable` list. The README's layout has no
    `repos/` or `tools/`, since hosts load instruction files and skills from subfolders of the
    folder they open; do this first wherever the subfolder probe failed.
  - Run the entrypoint probe once with the new `AGENTS.md`.
  - The three preferences on task copies and repository skills in `templates/POLICY.md`, with
    each project's clone listed in `private/workspace.json` as `"access": "read, task worktrees"`;
    clones already under `work/` keep working.

  Publishing needs approval of the exact branch, head, title, and body by default. A request that
  names the push or the pull request approves it, and so does a policy line approved in advance for
  a repository, as `docs/DEFAULTS.md` (Approvals in advance) shows; neither implies merging,
  releasing, tagging, or a force push. `review-rounds` above 2 stops at 2, the contract's limit.

  **Nothing to do for:** settings, which keep their values, including `review`; an `agents` line,
  which no longer applies and can go when you next edit the policy; approvals, the approval log,
  `private/workspace.json`'s format, and probes already passed.
  `docs/VALIDATION.md` keeps two probes, whether the entrypoint is loaded and followed and whether
  subfolders add instructions, and a short acceptance of a release; the Director probe, its kit in
  `probes/`, and the other probes are gone. `docs/HOSTS.md` says when delegation pays off, in one
  paragraph.
- A task's copy is a worktree of one clone per project, kept outside the workbench folder, instead
  of a fresh clone under `work/`, and closing a task removes its copy and branch after the After
  merge checks. A session also reads a repository's own agent instructions and skills before
  changing it, since Copilot CLI loads no skill from a subfolder. The README and
  `templates/POLICY.md` carry this; the contract now says "copy" where it said "clone", and
  `docs/PULL-REQUESTS.md` (After merge) removes a task's own copy and branch on the requester's
  word that its change is merged or dropped.
- `evals/` measures the core's way of working on real repositories: a service and the separate
  repository that configures its deployment, with tickets based on recent upstream fixes and
  hidden tests. It compares configurations of the core against a bare session and reports outcome,
  safety, continuity, cost, and friction from the host's records. A candidate core is one more
  configuration file. It is a development tool for the core: a workbench never reads it.
  `evals/reports/2026-11-candidate.md` measures M, this release's contract without its last two
  edits, on four scenarios, two runs each, against v0.3.0 in a single session: 36% less cost
  (US$42.11 against US$66.12) and 4 complete runs against 0, with no safety violation and the
  approved chart change in both runs of the scenario that needs one. It missed its own cost cap
  against a session with no core, US$31.41: its main sessions cost US$28.43, and its review
  sessions US$13.67, one in each of the eight runs. The two edits, one sentence on actions approved
  in advance and the word "copy" for "clone", were checked with rehearsals, not with the kit.
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
  blocks the action. The approval log may move to one linked file, and its entries record the
  date, the change, and the approver. Moving content out of the policy is itself a
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
