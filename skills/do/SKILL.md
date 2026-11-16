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

The task name is the ticket key in lowercase. Read
`private/tasks/<task>.md`. If it does not exist or has no Plan, say so, end with
`Next: /think <task>`, and stop.

Before anything else, list the steps of the Plan: each number with its `**Done:**` line copied
from the note, or `pending` if the step has none. Only this list says what is done; ignore what
the lines above the Plan say. If no step is pending, say so and stop. Otherwise the list opens
your reply at the end: do not reply before the work below is finished.

For each pending step, in order:

1. Open the file on its **Like** line and read it before you write anything.
2. Make the **Change**, copying the form of that file: names, layers, annotations, error handling,
   test structure. Add nothing the step does not name.
3. Run the **Check**. If it fails, fix it once and run it again. If it fails a second time, stop
   as described below.
4. Commit in the task's copy with the step's **Commit** message, and add to the step the
   line `**Done:** step <n>, <SHA>`, where `<n>` is the step's own number, such as `2` or `R1`.

A step whose Change is none has nothing to commit: run its Check and add
`**Done:** step <n>, checked`.

If a step is unclear, wrong, or needs something it does not name, do not improvise: stop. Never
change or delete an existing test to make a Check pass, unless the step's Change names that
test: stop.

To stop: commit nothing of that step and leave its files as they are. Add a line under Snags with
the step number and the error. Set the note's Last commit and Verified to what is true now, and
Next step to what the requester must decide. End your reply with `Stopped at step <n>` and the
question, not with a next command.

A stop holds until the requester decides. If the note's Next step is such a question, go on
only when the requester's words answer it: write what they decided into that step of the note
and continue from it. Words that do not answer it, such as a bare "go on", get the same
question and `Stopped at step <n>` again.

When every step is done, update Last commit, Verified and Next step in the note, one sentence
each, and add one line under Worked if something made this task go well. Do not push. Reply in
the requester's language: steps done, check results, snags. End with `Next: /review <task>`.
