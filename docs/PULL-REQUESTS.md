# Pull requests

What a pull request contains and how its review ends, so that two people or two agents finish a
change the same way. `OPERATING.md` (Review) sets the sequence; this adds the detail. It applies to
any repository that uses pull requests, unless the repository is disposable or its own rules differ.

## Before review

- Keep one cohesive change per pull request. Before parallel work, declare the files each task will
  touch; if they overlap, sequence the work.
- Re-read the complete base-to-head diff. Remove needless indirection, duplication, dead code, and
  tests that only restate the implementation. In documents, look for duplication and contradiction.
- Put information where its lifetime fits: behavior and non-obvious invariants in code and comments,
  the current contract in standing documents, open work in the backlog, and history, measurements,
  and investigation in the pull request or commit.
- When you rename, move, or delete something, update its references in the same change.
- A bug fix starts with a regression test when one can express the failure. Confirm the test fails
  without the fix.
- Run the repository's local checks.

## Description

State the problem, the approach, the impact, the scope with its deliberate non-changes, the
validation that ran on the final head, and what was not verified. After the last push, reconcile the
title and body with the complete diff and remove anything that no longer holds.

## Review request

Keep one request active at a time. Give the reviewer the exact head, base head, and merge base, and
ask for this:

- Inspect the complete diff and its immediate dependencies, then sweep it again by risk:
  correctness, security and privacy, data integrity, concurrency, error handling, compatibility,
  maintainability, validation evidence, and information placement.
- Report only material findings, all at once: severity, file and line, a concrete failure scenario,
  why validation missed it, and the smallest correction. Change nothing.
- End with the reviewed head, base head, and merge base, and one verdict: `ready to merge` or
  `changes required`.

## Material findings

A finding is material only when a concrete scenario affects correctness, security or privacy, data
integrity, concurrency, error handling, compatibility, maintainability, or the truth of validation
evidence. Severity and materiality are separate. A style preference is at most a non-blocking note.

## Verdicts

A verdict counts only when the configured reviewer gives it after the request, for the current head,
with no blocking finding open. Under `re-review: delta`, a new finding outside the diff is recorded
as a follow-up and does not block, unless it is P0, P1, or a real security risk. A review tool that
gives no verdict line counts as clean only through a submitted review of that head with no findings.

These are not verdicts: an acknowledgement, a reaction, a started workflow, a partial review, a
timeout, silence, passing checks, or approval of an earlier head.

## Answering findings

- Fix the neighbourhood, not only the reported line: read the whole file and its siblings, and
  search for the same claim elsewhere. Re-read whatever refers to what you changed.
- Put all in-scope fixes in one commit and one push, then ask for the next round.
- To reject a finding, record concrete evidence in the pull request, where others can check it.
- If a fix needs work outside the scope, stop: it normally belongs in another pull request.
- After the correction rounds in `review-rounds`, stop and report, as `OPERATING.md` says.

## Rounds after the first

The first review is complete and independent, with every finding at once. After it, the `re-review`
setting decides what a round covers. Under the default, `delta`:

- The reviewer gets the earlier findings and the diff since the reviewed commit, and checks only
  that the findings are resolved and that the fix broke nothing. Where the host allows it, resume
  the same reviewer session with the model set explicitly.
- Anything new outside that diff does not block, unless it is P0, P1, or a real security risk. It
  goes to a follow-up list or another pull request. An earlier finding stays open until it is fixed
  or rejected with evidence, wherever it is.
- `review-rounds` still applies: if the rounds run out, stop, and people decide.

A delta round can miss what a new look at everything would find. Save a full review from scratch for
risk and milestones: signing or security changes, before a release, and before a repository goes
public. What it finds is new work, not a failure of the earlier review.

## When the base moves

If only the base moved and its changes touch neither the files in the pull request nor anything they
depend on, update the branch and rerun the checks: the review stands, and you record the new head.
If they touch either, if the update needed a manual merge, or if you cannot tell, review the
integration on the new head.

## Mixed authorship

If two model families wrote parts of a change, each part is reviewed by the other family.
