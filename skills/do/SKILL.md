---
name: do
description: "Carry out the plan in a task note, step by step, with one commit per step. Use when a task has a plan with pending steps, or the requester asks to implement, continue, or fix a planned task. Pushes nothing."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `do` stage and you
are not that agent, start that agent with the stage, the task, and the requester's words,
nothing of your own, and relay its reply unchanged. Only if that reply ends with `Next:` and a
stage you have not run in this turn, run that stage the same way; at any other ending, end
your turn. For each later answer to that stage, start the agent again with the stage, the
task, and the answer. If you cannot start it, say which agent to select and stop.

The task name is the ticket key in lowercase, or its local name. Read
`private/tasks/<task>.md`. If it does not exist or has no Plan, say so, end with
`Next: /think <task>`, and stop.

Before anything else, list the steps of the Plan: each number with its `**Done:**` line copied
from the note, or `pending` if the step has none. Only this list says what is done; ignore what
the lines above the Plan say. If no step is pending, say so and stop. Otherwise the list opens
your reply at the end: do not reply before the work below is finished.

For each pending step, in order:

1. Read the file on its **Like** line before you write.
2. Make the **Change**, copying the form of that file: names, layers, annotations, error handling,
   test structure. Add nothing the step does not need.
3. Run the **Check**. If it fails, fix it once and run it again. If it fails again, stop.
4. Commit in the task's copy with the step's **Commit** message, and add to the step the
   line `**Done:** step <n>, <SHA>`, where `<n>` is the step's own number, such as `2` or `R1`.

A step whose Change is none has nothing to commit: run its Check and add
`**Done:** step <n>, checked`.

Stop only for what the requester must decide: a step that is unclear or cannot be done as
written, or a change the ticket and the Goal do not settle. What they settle, repair and name
under Snags: a file the Change needs but does not name, an existing test that asserts what the
ticket changes, a Check that passes only after a later step (run it again then). A Check the
machine cannot run: name it under Snags as not verified and go on. Never change or delete an
existing test otherwise: stop.

To stop: commit nothing of that step, leave its files as they are, and add the step number and
the error under Snags. Set the note's Last commit and Verified to what is true now, and Next
step to what the requester must decide. End your reply with `Stopped at step <n>` and the
question, not a next command.

A stop holds until the requester's words answer the note's question: write what they decided
into that step and continue from it. A bare "go on" gets the same question and
`Stopped at step <n>` again.

When every step is done, update Last commit, Verified and Next step in the note, one sentence
each, and add one line under Worked if something made this task go well. Do not push. Reply in
the requester's language: steps done, check results, snags. End with `Next: /review <task>`.
