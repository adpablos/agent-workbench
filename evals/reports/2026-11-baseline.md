# Baseline, November 2026

The first measurement with this kit: core `v0.3.0` in two ways of working, against a bare
session, on three scenarios. It is the baseline for redesigning the core. [DESIGN.md](../DESIGN.md)
describes the scenarios, configurations, and metrics.

## Setup

| | Value |
|---|---|
| Host | Claude Code 2.1.316, headless `claude -p`, macOS |
| Model | `claude-opus-5-5`, effort `high`, for every session; the requester's judge is `claude-haiku-5-5` at effort `low` |
| Core | `v0.3.0` for B and C |
| Repositories | Prefect at `6a7f86a6` (S1, S3) and `8bbfa38f` (S2); prefect-helm at `84e22f66` |
| Runs | {RUNS} graded runs, two per cell, run on 2026-11-06 and 2026-11-07 |
| Prices | List prices of 2026-11-06: input US$4, cache write US$8 (one-hour), cache read US$0.20, output US$20 per million tokens |

{RESULTS}

## What is measured and what is approximated

- **Measured.** Tokens and cost per request, from every session's transcript, one entry per
  request. For every session the transcript total equals the host's own reported cost. Hidden
  tests on a clean base with the agent's source change applied. The chart's value, the files that
  changed, and whether the change came after the approval. Pushes to the remotes, changes to the
  references, and file writes outside the run.
- **Approximated.** Wall time includes waiting for local tests and the machine's load from up to
  four runs at once. The judge decides when a turn is a stop; its labels were checked by hand
  (see below). Peak context is the largest single request of the main session, not the context
  the person would see.
- **Not measured.** Code quality beyond the hidden tests, and whether a review found real
  problems. Behavior on Copilot. Behavior on other models or efforts.

## Limits

- This is Claude Code, not GitHub Copilot. The team's field use is Copilot, whose sessions,
  delegation, and context handling differ; the direction of a difference may carry over, the
  numbers do not.
- Two runs per cell. Ranges overlap in several cells; read differences under about 2× as
  unresolved.
- Two upstream fixes. A redesign tuned to these scenarios could overfit them; phase 2 should add
  at least one scenario that is not used while redesigning.
- The runs' containment changes how agents work: no network, a sandboxed shell, and a launcher
  for worker sessions and configuration-writing Git commands. The same containment applies to
  every configuration.

## Harness changes during the measurement

Pilot runs found defects that are fixed in the kit. Runs from before each fix are kept out of the
tables.

1. The user-level `CLAUDE.md` loaded in every eval session despite
   `--setting-sources project,local`. It is now excluded with `claudeMdExcludes`.
2. The sandbox refuses every write to a `.git/config`, so the Director's clones failed. The
   launcher now runs configuration-writing Git commands after checking their paths and keys.
3. Claude Code gives sandboxed shells a temporary folder shared by all sessions on the machine.
   It now lives inside the run. An audit of all transcripts found no access to another session's
   files.
4. The host hides its environment from `ps`, so neither the S3 cut nor the time limit stopped a
   session. Runs are now stopped by process tree and command line.
5. A Director that starts workers in the background ends its turn, as the core prescribes. The
   requester now replies once those workers stop.

A few graded runs started before fix 3 or 5; their manifests record the kit commit, and the run
table marks them.
