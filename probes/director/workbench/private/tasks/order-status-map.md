# Map the order status flow across services

| Field | Value |
|---|---|
| Status | open; observed 2026-11-03 09:00 (task record created) |
| Ticket | none |
| Owner | Sam Rivera |
| Execution handle | none |
| Workspace | none; read references by path |
| Authorized scope | Read orders-api, billing-worker, and web-portal |
| Publication | none |

## Outcome and acceptance criteria

One page in this record that lists each order status, the service that sets it, and the event or
call that moves it to the next one, with file references. Good enough to brief a new worker.

## Decisions

## Results and evidence

## Review

| SHA | Implementer (model with source and label, or person) | Reviewer (model with source and label, or person and where) | Round | Result |
|---|---|---|---|---|

## Resources

| Path or ref | Purpose | Lifetime | Expected tip | Disposition (reason or authorization, date) |
|---|---|---|---|---|

## Blockers

None.

## Next action

Delegate a read-only investigation of orders-api status transitions to an economical model.

## Ownership log

| When | From | To | Scope | Evidence that previous writers stopped |
|---|---|---|---|---|
