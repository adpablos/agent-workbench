---
name: ship
description: "Write a task's pull request title and description and push its branch once the requester approves. Use when a task's change passed review, or the requester asks to ship, push, or open the pull request of a task. Changes no code."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `ship` stage and you
are not that agent, start that agent with the stage, the task, and the requester's words,
nothing of your own, and relay its reply unchanged. Only if that reply ends with `Next:` and a
stage you have not run in this turn, run that stage the same way; at any other ending, end
your turn. For each later answer to that stage, start the agent again with the stage, the
task, and the answer. If you cannot start it, say which agent to select and stop.

The task name is the ticket key in lowercase, or its local name. Read
`private/tasks/<task>.md`. Change no code.

1. Compare the note's Reviewed line with the HEAD of the task's copy. If the requester's
   message is `ship without review`, set that line to `<HEAD SHA> skipped by the requester`,
   or to `<HEAD SHA> open findings, accepted by the requester` when the note lists open
   findings or review steps not done. If the line does not show that same SHA as passed,
   skipped or accepted, say so, end with `Next: /review <task>`, and stop.
2. If the note already has a title and a description under `## Pull request text`, with no
   accepted finding missing, they are the text the requester saw. Never edit them on your
   own:
   - the requester's message is `Approved`: go to step 5;
   - the requester asks for a change to the text: make only that change, save it, and go to
     step 4;
   - anything else: go to step 4.
3. Otherwise read in full the style the policy names for commits and pull requests, the Goal in
   the note, and `git diff origin/<base>...HEAD` in the task's copy. Write the pull request
   title and description in that style. State only what the note and the diff show; for how it
   was tested, go by the note's Verified line and the tests in the diff. When the Reviewed
   line says open findings, end the description with each review step not done and each
   open finding, one line each. Save both in the note under `## Pull request text`.
4. Read that section again and show the requester the branch, the address of
   `origin` it will be pushed to, the output of `git diff --stat origin/<base>...HEAD`, and the
   title and description copied from the note, word for word. If a line of the policy approves
   pushing this repository's task branch in advance, go to step 5. Otherwise end with
   `Waiting for "Approved"` and stop.
5. `Approved`, or that line of the policy, is the approval of that push: push that branch to
   `origin` and nothing else. If the line also covers opening the pull request, open it with
   that title and description. Otherwise show the link the push printed and that title and
   description, for the requester to open it. Set the note's Next step to
   opening the pull request, or to the merge once it is open.
6. If the policy says how to read a build's result, set the note's Build line to
   `<pushed SHA> running` and end your reply with one line: the push starts a build that the
   next message about this task will check.

After the merge, the task ends with `/close <task>`.
