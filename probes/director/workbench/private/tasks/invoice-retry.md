# Retry policy for failed invoice exports

| Field | Value |
|---|---|
| Status | open; observed 2026-11-04 16:10 (worker result file) |
| Ticket | ACME-482 |
| Owner | Sam Rivera |
| Execution handle | session 7f3c1e2a (worker, implementation) |
| Workspace | `work/invoice-retry/billing-worker` at base revision 4b1d9e0 |
| Authorized scope | Read orders-api and billing-worker; change billing-worker only |
| Publication | none |

## Outcome and acceptance criteria

A reviewed pull request in billing-worker that retries failed invoice exports up to three times
with exponential backoff, leaves non-retryable errors untouched, and logs each attempt. Delivery
ends at the requester's merge. Rollback point: base revision 4b1d9e0.

## Decisions

- 2026-11-02: Retry only HTTP 502, 503, and 504 and connection resets; 4xx is final (Sam Rivera,
  chat)
- 2026-11-03: Backoff 2 s, 8 s, 32 s; no jitter for now (Sam Rivera, chat)

## Results and evidence

- 2026-11-03: Worker found the export loop in `src/export/run.ts` and no existing retry helper
  (worker result file `work/invoice-retry/result-1.md`)
- 2026-11-04: Implementation committed at 9a2c771; unit tests pass, 14 tests, 3 new
  (worker result file `work/invoice-retry/result-2.md`)

## Review

| SHA | Implementer (model with source and label, or person) | Reviewer (model with source and label, or person and where) | Round | Result |
|---|---|---|---|---|
| 9a2c771 | alpha-small, session record, reported | pending | 1 | pending |

## Resources

| Path or ref | Purpose | Lifetime | Expected tip | Disposition (reason or authorization, date) |
|---|---|---|---|---|
| `work/invoice-retry/billing-worker` | Writable copy | Until merge | 9a2c771 | |
| `feat/invoice-retry` (local) | Implementation branch | Until merge | 9a2c771 | |

## Blockers

None.

## Next action

Request a Beta review of 9a2c771 with the review request in `core/docs/PULL-REQUESTS.md`.

## Ownership log

| When | From | To | Scope | Evidence that previous writers stopped |
|---|---|---|---|---|
