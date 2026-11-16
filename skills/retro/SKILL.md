---
name: retro
description: "Every few tasks, read what went wrong and what went well in the archived task notes and propose improvements to this workbench and to the core. Use when the requester asks for a retro or for lessons from finished tasks."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `retro` stage and you
are not that agent, start that agent with the stage, the task, and the requester's words,
nothing of your own, and relay its reply unchanged. Only if that reply ends with `Next:` and a
stage you have not run in this turn, run that stage the same way; at any other ending, end
your turn. For each later answer to that stage, start the agent again with the stage, the
task, and the answer. If you cannot start it, say which agent to select and stop.

Before the requester approves, write only `private/retro.md`. If that file exists and the
requester's message is `Approved`, do only step 5.

1. In `private/tasks/archive/`, read only the Snags and Worked sections of each note that has no
   `Retro:` line. Read nothing else of them unless one line cannot be understood without it.
2. Group them. A snag seen once is noted, not acted on, unless it caused real damage. Something
   that worked more than once is worth keeping as a rule.
3. Propose two lists, each item one line, at most five items in all:
   - **Private:** the exact line to add, change, or remove, and in which file of `private/`.
     Prefer removing or shortening to adding.
   - **Core:** an improvement for the core itself, written with no name of the organization, its
     people, its projects, or its tools.
4. Save both lists and the names of the notes you read in `private/retro.md`, replacing what is
   there. Reply in the requester's language with both lists, copied from that file word for
   word, and end with `Waiting for "Approved"`.
5. After `Approved`, go by `private/retro.md`, not by memory: apply its Private lines, append
   its Core lines to `private/core-feedback.md` with the date and the core version, and add
   `Retro: <date>` to each note it names. If you changed `POLICY.md`, add a row to its Approval
   log. Then delete `private/retro.md`.

`private/core-feedback.md` is what the requester takes back to the core's maintainers.
