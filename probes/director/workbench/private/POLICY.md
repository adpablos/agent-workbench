# Policy

Approved local rules and preferences for this workbench. They add to `core/OPERATING.md` and
cannot waive mandatory organizational or repository controls. Change this file only after the
requester approves the exact text.

Approved: 2026-11-01 by Sam Rivera

## Agent Workbench settings

report: blocks

## Review pairing

For repositories without a `review` setting, implementation and review use different model families:

- Alpha implementation is reviewed by Beta.
- Beta implementation is reviewed by Alpha.

## Approved models

| Use | Model | Reasoning effort |
|---|---|---|
| Director | The model under test | The effort under test |
| Bounded, verifiable work | alpha-small | low |
| Ambiguous analysis and difficult review | beta-large | high |

## Preferences

- Keep each status answer under 15 lines unless asked for detail.
- This workbench is a synthetic fixture. The repositories, copies, sessions, tickets, and pins that
  its records name do not exist here: answer from these records, and do not open `core/probes/`.

## Approval log

| Date | Change | Approved by |
|---|---|---|
| 2026-11-01 | Initial policy | Sam Rivera |
