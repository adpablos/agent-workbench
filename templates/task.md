# <Task title>

<!-- A status note, kept when the work spans more than one session or follows the task skills:
private/tasks/<task>.md, the same name as its folder in work/. Keep it brief and current: one
sentence for each line of this list. The lines from Reviewed down are for the task skills; leave
them out otherwise. -->

- **Goal:** <the outcome the requester asked for, in their words where possible>
- **Copy and branch:** `work/<task>/<repo>`, branch `<branch>`
- **Last commit:** <SHA>
- **Verified:** <what passed, and how>
- **Next step:** <one action>
- **Open decisions:** <what waits on the requester, or none>
- **Reviewed:** <SHA and `passed`, or not yet>
- **Build:** <SHA and `passed`, `failed` or `running`, or none>
- **Pull request:** <link, or none>

## Approach

<!-- Written by /think. One line for each way the ticket could be met: the way, and why it was
chosen or left; a way better than the repository's current pattern is left, not planned. Then
one line for each job the change needs done and each thing it takes from another part: the
part of this repository that already does that job or produces that thing, with file and
line, and how the change does it there. -->

## Plan

<!-- A step changes at most two files, one code file and its test file; more files are more
steps, in the order they build on each other. The last step changes nothing and runs the
repository's own full checks (build, tests, lint), with only commands this machine can run. -->

1. **Change:** <files, and what to add or change in them>
   **Like:** <path of the existing file to imitate>
   **Check:** <one command and the result that shows it worked>
   **Commit:** <one-line message, in the style the policy names>
2. **Change:** None; run the repository's full checks.
   **Like:** none
   **Check:** <command and expected result>
   **Commit:** none

## Form

<!-- Written by /review: each thing the change adds, the nearest existing one, same or not;
then each thing it takes from another part, the part that produces it, and how it is taken. -->

## Pull request text

<!-- Written by /ship: the title on one line, then the description. -->

## Snags

<!-- One line each, facts only: what went wrong or cost time. Read later by /retro. -->

## Worked

<!-- One line each: what made this task go well and is worth repeating. -->
