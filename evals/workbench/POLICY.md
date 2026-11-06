# Policy

Approved local rules and preferences for this workbench. They add to `core/OPERATING.md` and
cannot waive mandatory organizational or repository controls. Change this file only after the
requester approves the exact text.

Approved: {date} by the requester

## Agent Workbench settings

report: blocks

## Review pairing

This workbench approves one model family. Implementation by `claude-opus-5-5` is reviewed by a
fresh `claude-opus-5-5` session that did not write the change, which `core/docs/DEFAULTS.md` lists
as `review: fresh session`.

## Approved models

| Use | Model |
|---|---|
| Director | `claude-opus-5-5`, effort `high` |
| Bounded, verifiable work | `claude-opus-5-5`, effort `high` |
| Ambiguous analysis and difficult review | `claude-opus-5-5`, effort `high` |

## Preferences

- Converse in English.
- Start a worker or review session from the workbench folder with
  `claude -p "<assignment>" --model claude-opus-5-5 --effort high --output-format json > <file>`,
  where `<file>` is under `work/<task>/`. The JSON holds the session's `session_id` and its final
  message in `result`. Continue a session with
  `claude -p "<message>" --resume <session_id> --model claude-opus-5-5 --effort high --output-format json`.
- Shell commands may run for up to an hour; give a long command an explicit timeout.

## Approval log

| Date | Change | Approved by |
|---|---|---|
| {date} | Initial policy | the requester |
