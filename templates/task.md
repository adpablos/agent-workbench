# <Task title>

<!-- One record per recoverable task: private/tasks/YYYY-MM-DD-short-name.md. One owner writes it.
Validation runs use this record too: put environment, core revision, action, observed outcome,
and limits under Results and evidence. -->

| Field | Value |
|---|---|
| Status | open, blocked, or closed; observed YYYY-MM-DD HH:MM (how) |
| Ticket | <optional link> |
| Owner | <Director session handle or person, never a role> |
| Execution handle | <native session or subagent reference, or none> |
| Workspace | `work/<task>/<repo>` at base revision <SHA> |
| Authorized scope | <what may be read and what may be changed> |
| Publication | <none, or: push the reviewed branch and open its pull request with agent-written text in <repository>; approved by <person>, YYYY-MM-DD> |

## Outcome and acceptance criteria

<!-- Name the delivery endpoint, for example a reviewed pull request, the requester's merge,
activation or release where it applies, its verification, and the rollback point. -->

## Decisions

- YYYY-MM-DD: <decision> (<who decided, where>)

## Results and evidence

- YYYY-MM-DD: <result> (<evidence reference>)

## Review

| SHA | Implementer (model with source and label, or person) | Reviewer (model with source and label, or person and where) | Round | Result |
|---|---|---|---|---|

## Blockers

## Next action

## Ownership log

| When | From | To | Scope | Evidence that previous writers stopped |
|---|---|---|---|---|
