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

1. Read the repository's own agent instructions. Look for a review skill or review instructions it
   keeps (for example under `.github/`, `AGENTS.md`, or a skills folder). If there is one, follow
   it as well, and say which one you used.
2. Read the change: `git diff origin/<base>...HEAD` in the task's copy, with the base the note
   names, and the files around it. You may run the checks.
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
   - No P1 or P2: set the value of its Reviewed line to `<HEAD SHA> passed`, and its Next step
     to `/ship <task>`.
   - Otherwise: add each P1 and P2 to the Plan as a new step `R1`, `R2`, with the same four
     lines as the other steps (Change, Like, Check, Commit), and set Next step to
     `/do <task>, to fix R1...`.
   Use only the ratings above, whatever scale another document gives.

Reply in the requester's language: the verdict first, then the findings in one line each, P3
included. End with `Next: /ship <task>` after a pass, or `Next: /do <task>` when you added steps.
