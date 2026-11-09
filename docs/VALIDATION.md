# Validation

How to check what a workbench actually does, and how a release of the core is accepted. Results are
private: record them in `private/`, never in this repository, with date, host and version, core
revision, what was done, what was observed, and limits. Missing capability is a failed or blocked
check, never a pass.

## Probes

Run a probe only when its answer decides the next step, and once per host and version; a result
carries over to another environment with the same host version and settings. Probes use throwaway
lines typed in the target environment, and are removed afterwards: confirm they are gone. Where the
host's record already shows the evidence, check it there instead of adding a chat turn;
[HOSTS.md](HOSTS.md) says where each host records what it loaded.

| Question | Probe | Evidence |
|---|---|---|
| Is the entrypoint loaded and followed? | Add a different word to the workbench `AGENTS.md`, `core/OPERATING.md`, and `private/POLICY.md`, each line asking the agent to end its first reply with that word. Open a new chat and ask for a small read-only task | The `AGENTS.md` word appears unprompted, or the host's record shows it in the instructions loaded at start. A read of the other two files in the host's trace, before the task's first operation. An agent's claim alone is not evidence |
| Are instruction files, skills, or agents in subfolders loaded? | In a temporary subfolder `probe/` of the workbench, add an instruction file under each name the host recognizes, and a skill or agent in each folder it recognizes for them ([HOSTS.md](HOSTS.md) lists both), each asking for a different word; put a skill's or agent's word in its description. Add a short `notes.md`. Open a new chat, ask for a one-line summary of `notes.md`, read with the host's own file tool if it has one, then ask it to list any instruction it received that asks for a specific word, and every skill and agent it can use | Any word in a reply or in the list, a probe skill or agent in the list or in the host's own listing, or a load in the host's trace; then delete the subfolder. The probe passes only if all show none. When it fails, keep reference repositories and tools outside the workbench folder, as the README's layout does |

If a probe fails, check [HOSTS.md](HOSTS.md) for a known cause before treating the capability as
missing.

## Accepting a release

A release of the core is accepted on a host when:

1. The `docs` check passes: links resolve, lines fit, and the contract stays within its word caps.
2. The entrypoint probe passes on that host with the release's `AGENTS.md`.
3. One small real or synthetic task runs end to end in a new session: a change in a copy under
   `work/`, tests that fail without it, a review if the change warrants one, and a final report.
   Record the usage the host reports and every time the requester had to step in.

A change to how hosts load instructions, such as a new host version, reruns the probes it can
affect. A larger change to the contract can also be measured with the kit in `evals/`, as its
README describes.
