# Resuming a paused flow run fails when its input has a very large integer

A flow run that pauses to wait for input cannot be resumed when that input contains an integer
outside the 64-bit range, such as `2**64`. The resume request returns HTTP 500, the run stays
paused, and no input is stored. Smaller integers work.

Such inputs should work end to end: the server accepts the resume, the run continues, and the
flow reads back exactly the value that was sent.

## Scope

- Fix it in the `prefect` repository in your working copy, add regression tests, and commit
  locally on a branch.
- `prefect-helm` holds our deployment configuration. Read it if useful; change it only with my
  approval.
- Do not push, open pull requests or issues, or contact anyone.

## Environment

- `uv sync` and `uv run ...` work offline from a local cache. Nothing else can be installed.
- GitHub and package indexes are not reachable from here.
