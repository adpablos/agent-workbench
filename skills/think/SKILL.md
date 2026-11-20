---
name: think
description: "Plan one development task from its ticket, as closed steps in its note. Use when asked to start, plan, or look at a ticket or task."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `think` stage and you
are not that agent, start that agent with the stage, the task, and the requester's words,
nothing of your own, and relay its reply unchanged. Only if that reply ends with `Next:` and a
stage you have not run in this turn, run that stage the same way; at any other ending, end
your turn. For each later answer to that stage, start the agent again with the stage, the
task, and the answer. If you cannot start it, say which agent to select and stop.

Change no code.

The task name is the ticket key in lowercase, or its local name. It names `work/<task>/` and
`private/tasks/<task>.md`. Without either, ask and stop.

1. Read the ticket with the tool the policy names. If you cannot, use the text the requester
   pasted, or else the task's or its idea's note; with none, ask and stop.
2. Read what the policy's Topics name for the project. Find the repository the change belongs
   to and read its agent instructions and skills.
3. Create the task's copy and branch as the policy says. If you cannot, say why and stop; write
   no plan from another copy.
4. Read in that copy the code the change touches, what calls it, and where each thing it uses
   comes from. When the ticket depends on another part or repository, read how it provides what
   the ticket needs.
5. Name the ways to meet the ticket and judge each by where things belong. For each job the
   change needs done (keeping state, reading or writing something shared, calling a service,
   formatting, validating), find the part of this repository that already does that kind of
   job: the change does it there, in that part's way. Take each thing that comes from another
   part from the part that produces it, as existing code does. That a part can reach a thing,
   or that doing a job in place is smaller, is no reason. Among the ways that fit, choose the
   smallest, and leave out what the ticket does not ask for.
6. Build each new thing like its closest example in the repository, or from what it already
   uses. Ask the requester and stop only when the ticket can be read in two ways that change
   what its user gets, or needs something you cannot reach: every other choice is yours. But
   when the ticket asks, however plainly, for what the code or its tests forbid on purpose
   without naming that rule, or leaves open what becomes of data already stored or a new
   dependency or service, its author may not know: say what you found, ask, and stop. Plan
   tests for what the ticket states, like the repository's for similar code: none where it has
   none.
7. Write `private/tasks/<task>.md` from `core/templates/task.md`, as its comments say. If the
   note has a Plan, keep its done steps and Snags; rewrite only the pending. Each step has the
   template's four lines, its Change needing no decision. Write the note in the language the
   policy sets for what leaves the workbench.

Reply in the requester's language, in at most ten lines: the goal, the way you chose, the
steps, one line each, and your choices. End with `Plan ready: /do <task>`, or with your
question alone.
