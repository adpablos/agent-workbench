---
name: think
description: "Plan one development task from its ticket: read the ticket and the code, and write closed steps in the task note. Use when the requester asks to start, plan, or look at a ticket or task. Changes no code."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `think` stage and you
are not that agent, start that agent with the stage, the task, and the requester's words,
nothing of your own, and relay its reply unchanged. Only if that reply ends with `Next:` and a
stage you have not run in this turn, run that stage the same way; at any other ending, end
your turn. For each later answer to that stage, start the agent again with the stage, the
task, and the answer. If you cannot start it, say which agent to select and stop.

Plan one task. Change no code.

The task name is the ticket key in lowercase, or the local name its idea's note gives it. It
names `work/<task>/` and `private/tasks/<task>.md`. Without either, ask for it and stop.

1. Read the ticket with the tool the policy names. If you cannot, use the text the requester
   pasted in this session, or else what the task's note or its idea's note says; if there is
   none, ask for it and stop.
2. Read what the policy's Topics name for the project. Find the repository the change belongs
   to and read its own agent instructions and skills.
3. Create the task's copy and branch as the policy says. If you cannot, say why and stop; write
   no plan from another copy. Read the code in that copy.
4. For each thing the change needs (an endpoint, a component, a test, a configuration entry), find
   the closest existing example in the same repository. If something has no close example, or the
   ticket can be read in two ways, ask the requester now and stop.
5. Choose the smallest change that meets the ticket, and leave out what it does not ask for.
   Plan tests for what the ticket states, as many and as detailed as the repository's tests for
   similar code, and no more.
6. Write `private/tasks/<task>.md` from `core/templates/task.md`. If the note already has a
   Plan, keep its done steps and its Snags and rewrite only the pending steps. Under Plan, write
   numbered steps, each with exactly these four lines:
   - **Change:** the file or files, and what to add or change in them, specific enough to do
     without a decision.
   - **Like:** the path of the existing file to imitate.
   - **Check:** one command and the result that shows the step worked.
   - **Commit:** the one-line commit message, in the style the policy names.
   A step changes at most two files, one code file and its test file; more files are more
   steps, in the order they build on each other. The last step changes nothing and
   runs the repository's own full checks (build, tests, lint), with only commands this machine
   can run.
   Keep the lines above the Plan to one sentence each. Write the note in the language the policy
   sets for what leaves the workbench.
7. If you see a better way than the repository's current pattern, add one line under Open
   decisions that starts with `Alternative:`. Do not plan it.

Reply in the requester's language, in at most ten lines: the goal, the steps in one line each,
the files you will imitate, and your questions. End with `Plan ready: /do <task>`, or with
your question alone when the plan waits on an answer.
