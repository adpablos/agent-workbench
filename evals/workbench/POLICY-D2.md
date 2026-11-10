# Policy

Approved local rules and preferences for this workbench. They add to `core/OPERATING.md` and
cannot waive mandatory organizational or repository controls. Change this file only after the
requester approves the exact text.

Approved: {date} by the requester

## Agent Workbench settings

report: blocks

## Review pairing

This workbench approves one model family. Implementation by `claude-opus-5-5` is reviewed by a
fresh `claude-opus-5-5` session that did not write the change (`review: fresh session`).

## Approved models

| Use | Model |
|---|---|
| Task session | `claude-opus-5-5`, effort `high` |
| Delegated bounded reads | `claude-opus-5-5`, effort `high` |
| Review | `claude-opus-5-5`, effort `high` |

## Preferences

- Converse in English.
- Start a delegated or review session from the workbench folder with the first command below,
  where `<file>` is under `work/<task>/`. The JSON holds the session's `session_id` and its final
  message in `result`. Continue a session with the second command.

  ```bash
  claude -p "<assignment>" --model claude-opus-5-5 --effort high --output-format json > <file>
  claude -p "<message>" --resume <session_id> --model claude-opus-5-5 --effort high --output-format json
  ```
- Shell commands may run for up to an hour; give a long command an explicit timeout.

## Approval log

| Date | Change | Approved by |
|---|---|---|
| {date} | Initial policy | the requester |
