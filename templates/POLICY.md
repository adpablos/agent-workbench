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

## Preferences

- Keep private data, such as customer records or personal details, out of repositories, test
  fixtures, and reports.
- <approved preference>

## Topics

Optional. Each file named here is part of this policy, read in full before its action, as
`core/docs/DEFAULTS.md` (Policy topics and approval history) describes. Rules that apply whatever
the action stay above.

- Before <action>, read `private/<topic>.md` in full.
- Before opening, reviewing, or merging a pull request, read `core/docs/PULL-REQUESTS.md` in full.

## Approval log

Here, or in one linked file such as `approvals.md`, never both.

| Date | Change | Scope | Reason | Approved by | Evidence of the approved text |
|---|---|---|---|---|---|
| YYYY-MM-DD | Initial policy | This workbench | Setup | <requester> | <where the exact text was approved> |
