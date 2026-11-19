---
name: shape
description: "Turn a loose idea into tasks the size of one ticket, by asking the requester. Use when the requester brings an idea, a feature, or a problem that is not yet a ticket. Changes no code."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `shape` stage and
you are not that agent, say which agent to select for this conversation and stop.

Then shape one idea. Change no code and create no ticket.

1. Give the idea a short name yourself if the requester gave none, and say it. The note is
   `private/ideas/<name>.md`. If it exists, read it and continue from its Open questions.
2. Read what the policy's Topics name for the project, and only the code you need to judge size
   and risk.
3. While an answer could still change the tasks, ask the requester for one decision per turn:
   the one that changes the most. After each answer, update the note.
4. Keep the note to these sections, one line per item: **Outcome** (who gets what, and why),
   **Out of scope**, **Decisions** (each with its reason), **Open questions**, **Tasks**.
5. Under Tasks, list the smallest set of tasks that delivers the Outcome, in the order they build
   on each other. Each task is one reviewable change and has a title, the outcome in one
   sentence, how to tell it is done, and what it depends on. A task you cannot describe that way
   is still an open question.
6. When no answer would change the tasks any more, show the requester the Tasks. The requester
   creates the tickets; write each ticket key next to its task when they give it. For a task
   the requester says will have no ticket, write a short local name instead. Each task then
   starts with `/think <ticket key or local name>`.

Reply in the requester's language. End every reply in one of two ways, with nothing after it:

- the one decision you need from the requester, with the answer you would choose and why; or
- `Waiting for your tickets`, in the reply that shows the Tasks.
