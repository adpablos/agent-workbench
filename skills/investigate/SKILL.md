---
name: investigate
description: "Find out what is really happening before any fix is planned: reproduce a reported failure, or answer a question about how the system behaves, by running it. Use when the requester reports an incident, a bug, or a failure with certain data, or asks to investigate or try something out. Changes no product code."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `investigate` stage
and you are not that agent, start that agent with the stage, the task, and the requester's words,
nothing of your own, and relay its reply unchanged. Only if that reply ends with `Next:` and a
stage you have not run in this turn, run that stage the same way; at any other ending, end
your turn. For each later answer to that stage, start the agent again with the stage, the
task, and the answer. If you cannot start it, say which agent to select and stop.

Investigate one thing. Change no product code and plan no fix.

The task name is the ticket key in lowercase, or, without a ticket, a short name you choose and
say. The note is `private/tasks/<task>.md`.

1. Read the report: the ticket, with the tool the policy names, or the requester's words. You
   need three things: what was expected, what happened, and with which data. If one is missing,
   ask for it and stop.
2. Read what the policy's Topics name for the project. Find the repository, read its own agent
   instructions, and create the task's copy and branch as the policy says, from the branch the
   report names, or else the base branch.
3. Reproduce it before you look for a cause. Run the code in the copy the way the repository's
   own instructions say (its tests, its local start), with the reported data, until you see the
   failure yourself. Prefer a new test that fails; otherwise a command and its output. If you
   cannot run it, or it does not fail, say exactly what you ran, what you saw, and what you
   need, and stop there: name no cause.
4. Only then find the cause: the file and line. Confirm it by running, not by reading: show the
   input that fails and the nearest input that does not.
5. Write the note from `core/templates/task.md`, in the language the policy sets for what leaves
   the workbench. Leave its Plan without steps and add above it a section `## Finding`:
   - **Reported:** what was expected, what happened, with which data.
   - **Reproduced:** the command and the output that show the failure, and the code of any
     test you wrote for it.
   - **Cause:** the file and line, and how you confirmed it.
   - **Not checked:** what you did not verify.
   Then remove from the copy every file you created, so that it is clean: the note keeps what
   the plan needs. Set Next step to `/think <task>`.

For a question instead of a failure, Reported is the question, Reproduced is what you ran and
saw, and Cause is the answer.

Reply in the requester's language, in at most ten lines: whether you reproduced it, the
evidence, the cause, and what you did not check. End with `Finding ready: /think <task>`, or
with what you need when you could not reproduce it.
