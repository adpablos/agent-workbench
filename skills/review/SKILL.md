---
name: review
description: "Review a task's finished change once, against its ticket and against how the repository already does things. Use when every step of a task's plan is done, or the requester asks for a review of a task. Changes no code."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `review` stage and you
are not that agent, start that agent with the stage, the task, and the requester's words,
nothing of your own, and relay its reply unchanged. Only if that reply ends with `Next:` and a
stage you have not run in this turn, run that stage the same way; at any other ending, end
your turn. For each later answer to that stage, start the agent again with the stage, the
task, and the answer. If you cannot start it, say which agent to select and stop.

The task name is the ticket key in lowercase, or its local name. Read
`private/tasks/<task>.md`. You did not write this change. Change nothing in the task's copy;
stop if `git diff HEAD` shows changes.

1. Read the repository's agent instructions and any review skill (`.github/`, `AGENTS.md`,
   a skills folder). Follow them; say which.
2. Run the repository's pipeline checks (types, format, tests): a failure the change causes is
   a finding; one the machine causes is named as not verified.
   Read `git diff origin/<base>...HEAD` in the task's copy (the note's base) and the files
   around it.
   If the Reviewed line names a commit with findings and `re-review` is not `full`, read
   instead `git diff <that commit> HEAD`, the Plan's review steps and the open findings: check
   each is resolved, reading what else its fix changes, and nothing broke. Anything new
   outside is `P3` unless `P1` or a security risk.
3. Answer, each with file and line:
   - **Defects:** where does the change fail the Goal, break existing behavior, or lack a test
     that would fail without it?
   - **Different:** where does it do something another way than this repository does?
     Do not answer from memory. List under `## Form` in the note everything the change adds (a
     function, a test, a configuration entry, a name), the nearest existing one of its kind with
     file and line, and `same` or what differs. List there too each thing the change takes from
     another part (a value, shared state, a setting, a service), the part that produces it, and
     how existing code takes from that part. Each difference the
     ticket did not ask for, and each thing taken through a part that does not produce it, is a
     finding, `P2` or higher.
   - **Extra:** what could be removed and still meet the Goal?
4. Rate each finding: `P1` must fix, `P2` should fix, `P3` optional.
5. In the note:
   - No P1 or P2: empty `## Open findings`, set Reviewed to `<HEAD SHA> passed` and Next step
     to `/ship <task>`.
   - Otherwise: add each P1 and P2 to the Plan as a step `R1`, `R2`, with the other steps'
     four lines, its Change naming every file the fix touches, tests included. Set
     Reviewed to `<HEAD SHA> findings, round <n>` and Next step to `/do <task>, to fix R1...`. From
     round `review-rounds` plus 1 (default 3), add no steps: list the findings under
     `## Open findings`, set Next step to the requester's decision and end with them,
     without `Next:`.
   Use only these ratings, whatever scale another document gives.

Reply in the requester's language: verdict, then each finding in one line, P3 included.
End with `Next: /ship <task>` after a pass, `Next: /do <task>` when you added steps.
