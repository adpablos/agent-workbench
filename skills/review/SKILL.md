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
`private/tasks/<task>.md`. You did not write this change. Change nothing in the task's copy.

1. Read the repository's own agent instructions. Look for a review skill or instructions it
   keeps (`.github/`, `AGENTS.md`, a skills folder). Follow one you find as well, and say which.
2. Read the change: `git diff origin/<base>...HEAD` in the task's copy, with the base the note
   names, and the files around it. You may run the checks.
   If the Reviewed line names a commit with findings and `re-review` is not `full`, read
   instead `git diff <that commit>...HEAD` and the Plan's review steps: check each finding is
   resolved and the fix broke nothing. Anything new outside it is `P3` unless `P1`.
3. Answer three questions, each with file and line:
   - **Defects:** where does the change fail the Goal, break existing behavior, or lack a test
     that would fail without it?
   - **Different:** where does it do something another way than this repository already does it?
     Do not answer from memory. List under `## Form` in the note every thing the change adds (a
     function, a test, a configuration entry, a name), the nearest existing one of its kind with
     file and line, and `same` or what differs. List there too each thing the change takes from
     another part (a value, shared state, a setting, a service), the part that produces it, and
     how existing code takes things from the part that produces them. Each difference the
     ticket did not ask for, and each thing taken through a part that does not produce it, is a
     finding, `P2` or higher.
   - **Extra:** what could be removed and still meet the Goal?
4. Rate each finding: `P1` must fix, `P2` should fix, `P3` optional.
5. Write the result in the note:
   - No P1 or P2: set its Reviewed line to `<HEAD SHA> passed`, and Next step to
     `/ship <task>`.
   - Otherwise: add each P1 and P2 to the Plan as a new step `R1`, `R2`, with the four lines
     of the other steps (Change, Like, Check, Commit), its Change naming every file the
     fix touches, the test that checks it included. Set the Reviewed line to
     `<HEAD SHA> findings, round <n>` and Next step to `/do <task>, to fix R1...`. From
     round 3 (`review-rounds` plus 1), add no steps: set Next step to the requester's
     decision and end with the open findings, without `Next:`.
   Use only these ratings, whatever scale another document gives.

Reply in the requester's language: the verdict first, then the findings in one line each, P3
included. End with `Next: /ship <task>` after a pass, or `Next: /do <task>` when you added steps.
