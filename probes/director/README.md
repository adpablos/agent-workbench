# Director probe kit

Fixed records, requests, and a written answer for the probe "Which model and reasoning effort can
the Director use?" in [docs/VALIDATION.md](../../docs/VALIDATION.md). With one kit, no workbench
writes its own records or answer, and one reference run confirms the answer for every host.

Never give [answer.md](answer.md) to the agent under test.

## Set up a run

Give each run its own folder outside the opened root of any workbench, `<run>` below:

1. Copy the contents of `workbench/` into `<run>`, so that `<run>/private/POLICY.md` exists.
2. Copy `core/templates/workbench-entrypoint.md` to `<run>/AGENTS.md`.
3. Check out the core under test as `<run>/core`, for example from a workbench's core:
   `git -C <workbench>/core worktree add --detach <run>/core <revision>`.
4. Open `<run>` as the root of a new session, with the candidate model and reasoning effort
   selected explicitly.

## Run

In that session, send each request after the previous answer:

```text
Resume: what is the next action on the top priority, and is anything blocked on me?
```

```text
The review of 9a2c771 is back with no findings; the reviewer's session record reports beta-large. Record that in the invoice-retry task and tell me the next action.
```

Compact the chat if the host compacts on request; otherwise record that check of the read probe as
not run. Then send:

```text
What does the portal date library task need from me?
```

## Judge

Compare the three replies, `<run>/private/tasks/invoice-retry.md`, and the host's record of the
session with [answer.md](answer.md). Take the run's usage from the host's record, not from the
agent. Then remove the run: `git -C <workbench>/core worktree remove <run>/core`, and delete
`<run>`.

## Reference

A change to this kit needs a reference run before it merges: the strongest model available to the
maintainers, at its highest reasoning effort, must pass it. If the reference finds something the
records support that the answer lacks, correct the answer and judge every run again. The pull
request that last changed this kit records that run.
