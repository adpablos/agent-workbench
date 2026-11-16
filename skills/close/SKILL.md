---
name: close
description: "After a task's pull request is merged or dropped, remove the task's copy and branch and archive its note. Use when the requester says a task is merged, dropped, or finished."
---
Follow the workbench `AGENTS.md` first. If the policy names an agent for the `close` stage and you
are not that agent, start that agent with the stage, the task, and the requester's words,
nothing of your own, and relay its reply unchanged. Only if that reply ends with `Next:` and a
stage you have not run in this turn, run that stage the same way; at any other ending, end
your turn. For each later answer to that stage, start the agent again with the stage, the
task, and the answer. If you cannot start it, say which agent to select and stop.

The task name is the ticket key in lowercase. Read `private/tasks/<task>.md`. The requester is
telling you this task's change is merged or dropped.

1. Read `core/docs/PULL-REQUESTS.md`, section After merge, in full.
2. If the requester's message is `Remove` and the note's Next step is `Waiting for "Remove"`,
   they have seen what would be lost: remove that copy with `git worktree remove --force` and
   that local branch with `git branch -D`, nothing else, and go to step 6.
3. Run that section's checks on the task's copy and branch, with Git commands. The requester's
   message is the word that no other session is writing there: do not inspect processes.
   Never force, reset, or clean.
4. If every check passes, remove the copy with `git worktree remove` and the local branch with
   `git branch -d`. The branch's tip being an ancestor of the fetched base branch is proof of
   the merge.
5. If you cannot show the change is merged (a dropped task, or a squash merge you cannot read
   with the tool), or a command refuses: remove nothing. Show the commits that are not in the
   base branch and the files that are not committed, set the note's Next step to
   `Waiting for "Remove"`, end your reply with those same words, and stop.
6. Remove the folder `work/<task>` if it is empty.
7. Move `private/tasks/<task>.md` to `private/tasks/archive/<task>.md`.

Run the removals in the repository's clone, with each path written out in the command, not
held in a shell variable. Never touch the remote branch.

Reply in the requester's language, one line each: what you removed, what you kept and why.
