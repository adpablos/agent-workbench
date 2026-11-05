# Upgrade the portal's date library

| Field | Value |
|---|---|
| Status | blocked; observed 2026-11-04 11:30 (requester message) |
| Ticket | ACME-455 |
| Owner | Sam Rivera |
| Execution handle | none |
| Workspace | none yet |
| Authorized scope | Read web-portal |
| Publication | none |

## Outcome and acceptance criteria

A list of every call site of the current date library in web-portal, the breaking changes of the
target major version that affect them, and an estimate, so the requester can decide whether to
upgrade this quarter. No code change.

## Decisions

- 2026-11-01: Investigation only; no copy needed (Sam Rivera, chat)

## Results and evidence

- 2026-11-02: 37 call sites in 12 files; 9 use the parsing API that changes in the next major
  (subagent result captured here; command: `grep -rn "dateLib\." src/`)

## Review

| SHA | Implementer (model with source and label, or person) | Reviewer (model with source and label, or person and where) | Round | Result |
|---|---|---|---|---|

## Resources

| Path or ref | Purpose | Lifetime | Expected tip | Disposition (reason or authorization, date) |
|---|---|---|---|---|

## Blockers

- The requester must confirm whether the portal still supports the legacy browser list, which
  decides two of the nine affected call sites.

## Next action

Wait for the requester's answer on browser support, then finish the estimate.

## Ownership log

| When | From | To | Scope | Evidence that previous writers stopped |
|---|---|---|---|---|
