# Validation

How to establish what a workbench can actually do, and how to accept a release. Results are
private: record each one as a task record in `private/tasks/`, never in this repository. The first
release accepted on a host passes every stage that gates base acceptance there. A later release
runs only what [Release checks](#release-checks) selects for its changes, and relies on earlier
results for the rest. An integration keeps its own gate.

Each result records date, environment, core revision, action, observed outcome, and limits.
Synthetic success does not show live-service access or enforced isolation. Missing capability is
reduced or blocked validation, never a pass.

## Preflight probes

Run a probe only when its answer decides the next step, and reuse facts already established in
your environment. Results belong to one host: probe each host you use as Director. Probes are
harmless: they use throwaway lines typed in the target environment, not imported candidates, and
they are removed afterwards.

| Question | Probe | Evidence |
|---|---|---|
| Is the root `AGENTS.md` loaded automatically? | Add a temporary line to the workbench `AGENTS.md`: "End your first reply with the word `<random word>`." Open a new Director chat and only say hello. | The word appears unprompted; any read trace the host shows |
| Are `core/OPERATING.md` and `private/POLICY.md` read before acting? | Add a different word to each file, open a new Director chat, and ask for a small read-only task; a greeting may not count as acting. In the same chat, ask for a second one; where the host compacts on request, compact and ask for a third | A read of each file in the host's trace, before the task's first operation. Where the host shows no order, the words prove only that the files were read: record the order as unverified. An agent's claim alone is not evidence. The second task reads neither file again; after compaction, both are read again before the third |
| Does a delegated agent follow the instruction paths it is given? | Delegate a trivial task naming a file that holds a third probe word | The word in the returned result |
| Can a new Director reach existing sessions? | Start a session from one Director chat; from a new chat, list it, read it, and send it one message | Host listing, the delivered message |
| Which confirmations appear? | Count the prompts during the probes above | Count and type of each prompt |
| Which model ran a delegated task? | Delegate with an explicitly selected model and note what the host shows | Reported or configured evidence, as defined in `OPERATING.md` (Review); [HOSTS.md](HOSTS.md) says where each host shows it |
| Do delegated tasks run in parallel? | Two independent tasks that each wait 20 seconds and report start and end times | Overlapping times; otherwise sequence the work |
| Are instruction files in subfolders loaded? | In temporary subfolders `repos/probe/` and `tools/probe/`, add an instruction file in each location and under each name the host recognizes ([HOSTS.md](HOSTS.md) lists them), each asking for a different word, plus a short `notes.md`. Open a new Director chat, say hello, ask for a one-line summary of both `notes.md` files, read with the host's own file tool, if it has one, then ask it to list any instruction it received, in any form, that asks for a specific word. Some names hide others, so repeat in a new chat with only `AGENTS.md` in those subfolders | Any word in a reply or in the list, or a load in the host's trace; then delete the subfolders. The probe passes only if all show none and the trace shows that tool, on a host that has one: a read through a shell may load nothing, and an agent may ignore a file the host loaded, so a clean reply alone proves nothing |
| Can agents read outside the opened root? | Ask for the first line of an approved file outside the root | Result and any prompt shown |
| What isolation do experiments have? | Inspect host sandbox and permission settings without changing them | Observed settings; record limits as procedural if none apply |

Remove the probe lines afterwards and confirm they are gone. If a probe fails, check
[HOSTS.md](HOSTS.md) for a known cause before treating the capability as missing.

## Reference baselines

Before and after work that must not touch a reference repository, record its state by running
this block in Bash (Git Bash on Windows) at the repository's top level. It only reads: it runs no
Git filters, external diff drivers, or hooks, and it hashes file bytes exactly as they are on disk.

```bash
(
  set -eo pipefail
  git rev-parse HEAD
  git ls-files --stage | sha256sum
  find . -name .git -prune -o -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum
  echo "capture complete"
)
```

A capture counts only if the block exits with status 0 and its last line is `capture complete`;
otherwise fix the cause and capture again. Equal captures mean that the checked-out commit, the
index entries (staged paths, modes, and object IDs), and the path and exact bytes of every regular
file outside `.git` (tracked, untracked, or ignored) are unchanged. They do not cover other Git
internals such as branches, stashes, or configuration, nor symbolic links, empty directories,
permissions, or timestamps. Hashing every file can take a while in large trees. Pre-existing
changes stay as they are; never clean or reset a repository to make a comparison pass.

## Acceptance stages

| Stage | Exercise and required evidence | Gates base acceptance |
|---|---|---|
| Core payload | Generic English content, no private material, valid relative links | Yes, before publication |
| Environment preflight | The probes above that decide the next step | Yes |
| Deterministic checks, if any | Synthetic tests of observable properties and real failure modes, on each platform the check supports | Only if a check ships |
| Synthetic delegation | Two independent bounded tasks with explicit roles and separate handles; parallel if supported, otherwise sequenced | Yes |
| Synthetic code change | Small change in an isolated copy, meaningful checks, independent review of the final SHA, reference baseline unchanged | Yes |
| Review stop behavior | Missing or unattributed reviewer, stale revision, and exhausted rounds all leave readiness pending | Yes |
| Recovery and continuity | Resume, Check in, and Wrap up across sessions: ownership reconciled, an unresolved commitment kept, no duplicate dispatch or competing writers | Yes |
| Boundary behavior | Writable destinations, preserved reference content, permitted reads, mock-only experiments, approval stops, persistent outputs in the configured language | Yes |
| First integration | One read-only integration: provenance, coverage gaps, declared local side effects | No; it has its own gate |

The synthetic code change uses a small fixture that is built after the preflight, once the
target environment's toolchain is known.

## Release checks

Every release passes Core payload. For each behavior that a release changes, wherever it is
written, run the checks of its row on the host whose acceptance the release extends. A change of
wording that leaves every behavior as it was needs only Core payload. Combine checks in one session
where they do not interfere, reuse the workbench and fixtures of the earlier acceptance, and record
what was not rerun. A change that fits no row, or that changes the contract's structure, such as
adding a role, takes the base journey.

| Behavior changed | Checks |
|---|---|
| What is read before acting, and when a read counts | The probe of whether `core/OPERATING.md` and `private/POLICY.md` are read before acting |
| Roles, delegation, or how results return | One delegation with explicit roles, separate handles, and its return route |
| Review, readiness, or pull requests, including review settings | Synthetic code change and review stop behavior |
| Ownership, resuming, or handover | Recovery and continuity |
| Access to sources, writable destinations, approval, references, executables and their local side effects, precedence, or the language of outputs | Boundary behavior, for the rule that changed |
| Updating the core or a pinned tool | One core update from the previous release to the candidate |
| Setup, or a template that setup or an update writes | The setup or core update step that writes it |
| A default's value, with its behavior unchanged | A Director lists the settings and shows the new value |
| When a project's release is proposed, closed, or tagged | In a synthetic consumed repository, a merged change leads the Director to propose a release that closes Unreleased before any tag |
| The reference baseline block | Two captures of an unchanged fixture match; captures before and after a change to a tracked and to an ignored file differ |
| A probe | That probe |
| How the core itself is released or accepted | The release that ships the change follows the new rule |
| A host's behavior, in its section of `docs/HOSTS.md` | On that host, the probes whose answer the change affects; none on other hosts |
| A check in CI | The changed check, run once on input it must reject and once on input it must accept |

## Base journey

1. Open the workbench and establish capabilities with the probes that matter.
2. Delegate two independent tasks.
3. Complete a small verified code change with independent review of its final SHA.
4. Recover from another session with Resume, then run Check in and Wrap up.

Record elapsed time, visible usage, and requester interventions once during this journey; no
telemetry is needed.
