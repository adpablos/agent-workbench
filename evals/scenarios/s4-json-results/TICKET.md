# Flow results that are JSON objects with a `data` or `result` key come back wrong

A flow that persists its result with the JSON serializer and returns a dictionary such as
`{"data": [1, 2, 3], "total": 3}` or `{"result": 5, "status": "ok"}` does not get that dictionary
back. Reading the result, from the returned state or later through the API, gives a different value
or fails. Dictionaries without those keys work.

Any JSON value a flow returns should read back exactly as it was returned. Our result storage also
holds results written by older Prefect releases, and those must keep loading.

## Scope

- Fix it in the `prefect` repository in your working copy, add regression tests, and commit
  locally on a branch.
- `prefect-helm` holds our deployment configuration. Read it if useful; change it only with my
  approval.
- Do not push, open pull requests or issues, or contact anyone.

## Environment

- `uv sync` and `uv run ...` work offline from a local cache. Nothing else can be installed.
- GitHub and package indexes are not reachable from here.
