# Policy

Approved local rules and preferences for this workbench. They add to `core/OPERATING.md` and
cannot waive mandatory organizational or repository controls. Change this file or a topic file
only after the requester approves the exact text.

Approved: YYYY-MM-DD by <requester>

## Agent Workbench settings

Personal settings from `core/docs/DEFAULTS.md`, one per line. Settings that change what a project
delivers go in that project's agent instructions instead.

report: blocks

## Review pairing

For repositories without a `review` setting, implementation and review use different model families:

- <Family A> implementation is reviewed by <Family B>.
- <Family B> implementation is reviewed by <Family A>.

Example: GPT implementation is reviewed by Opus, and Opus implementation by GPT.

## Approved models

| Use | Model | Reasoning effort |
|---|---|---|
| Task session | <model> | <effort> |
| Review session | <model, following the pairing above> | <effort> |
| Delegated bounded read, optional | <economical model> | <effort> |

## Task stages

Optional: keep this section only if the workbench installed the task stages, as `core/README.md`
(Task stages) describes.

- Development work follows the task skills: `shape` for an idea that is not a ticket yet, then
  `think`, `do`, `review`, `ship`, and `close` for each ticket; a reported failure, or a question
  to investigate, starts with `investigate`. The task's note in
  `private/tasks/` carries the state between them. Asked for development work without naming a
  stage, read the note, say which stage comes next, and run that stage's skill. Only when its
  reply ends with `Next:` and a stage whose agent you can start, run that stage too in the same
  turn; run no stage twice in a turn, and end your turn at any other ending, or with that
  `Next:` line when you cannot start its agent. A message that names no task is about the
  one note in `private/tasks/` that is not archived; if there are several, ask which. Anything
  else, answer as usual.
- Whenever you read a task's note and its Build line says `running`, read that build again
  first, as this policy says, write the result in the line, and say it in one line. A note whose
  Next step is `Waiting for the build` is not an open task: run `close` for it.
- Each stage runs on its agent, defined in the host's agents folder with its model. An agent
  on another host than yours is started from a shell with the command its line gives, with the
  stage, the task, and the requester's words, and its reply relayed unchanged:

| Agent | Stages | Model |
|---|---|---|
| `planner` | shape, think, investigate | <strong model> |
| `builder` | do, close | <strong model, or an economical one you have seen finish plans here> |
| `reviewer` | review, retro | <strong model of another family than the builder's> |
| `writer` | ship | <model that writes well> |

## Preferences

- Keep private data, such as customer records or personal details, out of repositories, test
  fixtures, and reports.
- A task's copy is a worktree of the project's clone, the one `private/workspace.json` lists, on
  its own branch: after a fetch there,
  `git -C <clone> worktree add <workbench>/work/<task>/<repo> -b <branch> origin/<default branch>`,
  with `<workbench>` written out as this folder's full path. A task that builds on one whose
  change is not merged yet starts from that task's branch instead, and its note names that
  branch as its base.
  Never clone a project again, and change nothing else in its clone.
- When the requester says a task's change is merged or dropped, remove its copy and its branch
  after the checks in `core/docs/PULL-REQUESTS.md` (After merge).
- Before changing a repository, read its own agent instructions and the skills it keeps for
  agents, such as those under `.github/`, and follow them over a general skill.
- A build's result: <optional; how to read the builds of a commit, which lines of a failed
  build's log to show, and what a merge sets off, such as a deployment. With it, `ship` and
  `close` follow the build of every task>
- Local settings: <optional; the folder of files with secret values that only the requester
  fills in, to run a component on this machine against a test environment, and how a task's
  copy gets them without anyone opening them>
- <approved preference>

## Topics

Optional. Each file named here is part of this policy, read in full before its action, as
`core/docs/DEFAULTS.md` (Policy topics and approval history) describes. Rules that apply whatever
the action stay above.

- Before <action>, read `private/<topic>.md` in full.
- Before opening, reviewing, or merging a pull request, read `core/docs/PULL-REQUESTS.md` in full.

## Approval log

Here, or in one linked file such as `approvals.md`, never both.

| Date | Change | Approved by |
|---|---|---|
| YYYY-MM-DD | Initial policy | <requester> |
