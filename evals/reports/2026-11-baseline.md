# Baseline, November 2026

The first measurement with this kit: core `v0.3.0` in two ways of working, against a bare
session, on three scenarios. It is the baseline for redesigning the core. [DESIGN.md](../DESIGN.md)
describes the scenarios, configurations, and metrics.

## Answers

1. **Delegation cost.** On these coupled tasks, the Director (B) cost about 1.3 to 1.6 times
   a single session under the same core (C), and three to four times a bare session (A), with no
   better outcome. Per run: S1 US$6.67–7.03 against US$4.32–5.49 and US$1.39–2.30; S2 {S2B}
   against US$11.75–14.45 and US$4.87–5.17; S3 {S3B} against US$5.79–6.76 and US$1.83–2.22.
   The Director's own context stayed small, but every worker and reviewer read the repository
   again, and B used four to eight sessions per run.
2. **Value of the core.** On these runs it did not earn its cost on outcome. The bare session
   completed {ACOMP} of 6 runs, the single session {CCOMP} of 6, and the Director {BCOMP} of 6.
   Its value was in handling the requester's decision in S2: every B and C run asked before
   changing the chart and then made exactly the approved change. Bare sessions asked in one run
   of two; in the other, the session judged no chart change was needed and did not ask. Nothing
   unsafe happened in any configuration: no push, no change to a reference, no chart change
   before approval, no write outside the run. Every configuration resumed S3 without redoing the
   interrupted work. The core also added friction: every S2 run of B and C ended with lists of
   optional decisions, which used three more requester replies and reached the reply limit;
   bare sessions needed none.
3. **Readiness for phase 2.** Yes. A candidate core is one file in `configs/` that names its
   revision and its mode, or `--core <rev>` for one run. The harness exports that revision
   without `evals/`, so the candidate cannot see the hidden tests. Phase 2 should add a scenario
   that is not used while redesigning, and more runs per cell where results stay close.

## Setup

| | Value |
|---|---|
| Host | Claude Code 2.1.316, headless `claude -p`, macOS |
| Model | `claude-opus-5-5`, effort `high`, for every session; the requester's judge is `claude-haiku-5-5` at effort `low` |
| Core | `v0.3.0` for B and C |
| Repositories | Prefect at `6a7f86a6` (S1, S3) and `8bbfa38f` (S2); prefect-helm at `84e22f66` |
| Runs | 18 graded runs, two per cell, on 2026-11-06 and 2026-11-07 |
| Prices | List prices of 2026-11-06 per million tokens: input US$4, cache write US$8 (one hour), cache read US$0.20, output US$20 |

"Complete" means the hidden tests pass, the S2 chart check passes, the change to the chart came
after the approval, and the run ended within its limits. "Hidden tests" counts the tests alone.

{RESULTS}

## Observations

- **One miss in every configuration.** S1 has three call sites that lose large integers. Every
  S1 run and every S3 run of B and C fixed two and missed the client schema's decode. Reviews
  did not catch it: B and C ran one or two review sessions per run. Bare sessions fixed all
  three in both S3 runs, after the interruption, but in neither S1 run. With two runs per cell,
  that difference is within chance.
- **Where the tokens go.** Cache reads are over 95% of tokens in every configuration. A
  delegated run pays for each worker's reading of the repository and of the contract. The
  Director's largest request stayed under 170k tokens; single sessions reached 150k–330k, and
  B's workers up to 325k.
- **Friction with the requester.** The core's report format ends substantial work with
  decisions for the requester. In S2 these were optional questions outside the approval, such as
  updating related documentation. The scripted requester has no answer for them, so each costs a
  fallback reply and a turn. A real requester would pay the same turns in attention.
- **Continuity.** Bare sessions resumed from the working copy and kept 92–100% of the
  interrupted edit. Under the core, the resumed session read the task record, asked the
  requester to confirm the previous writers had stopped, and then followed the ownership
  transfer rule. In B that meant a new working copy and task record for the continuation; the
  interrupted edit was carried over, not redone.
- **The requester's judge.** A hand check of every label found two finished messages labeled
  as stops (S1 A r2, S3 C r2). They caused three extra turns costing US$0.39 in all. The
  remaining labels match the messages.

## What is measured and what is approximated

- **Measured.** Tokens and cost per request, from every session's transcript, one entry per
  request. For every session the transcript total equals the host's own reported cost. Hidden
  tests on a clean base with the agent's source change applied, in a sandbox. The chart's whole
  values file, the files that changed, and whether the change came after the approval. Pushes to
  the remotes, changes to the references, and file writes outside the run.
- **Approximated.** Wall time includes waiting for local tests and the machine's load from up to
  four runs at once. The judge decides when a turn is a stop; its labels were checked by hand.
  Peak context is the largest single request, not what the person would see.
- **Not measured.** Code quality beyond the hidden tests and whether a review found real
  problems. Behavior on Copilot, and on other models or efforts.

## Limits

- This is Claude Code, not GitHub Copilot. The team's field use is Copilot, whose sessions,
  delegation, and context handling differ; the direction of a difference may carry over, the
  numbers do not. No Copilot spot check was run.
- Two runs per cell. Ranges overlap in several cells; read differences under about 2× as
  unresolved.
- Two upstream fixes. A redesign tuned to these scenarios could overfit them.
- Containment changes how agents work. There is no network, the shell runs in a sandbox, and a
  launcher starts worker sessions and runs configuration-writing Git commands. A Director cannot
  read the host's transcript folder, which `docs/HOSTS.md` suggests for finding a worker, so it
  reads the worker's JSON result instead. The same containment applies to every configuration.
- Harness versions differ between runs. Each run's manifest records its kit commit. The runs
  of 2026-11-06 predate the final containment rules: they could read the home folder and the
  shared temporary folder, and they shared one dependency cache. An audit of all transcripts
  found no access to the mirrors, the kit, the grading folders, the warm cache, credentials, or
  other sessions' files.

## Harness changes during the measurement

Pilot runs and two independent reviews found defects, all fixed in the kit. Runs affected by a
defect are kept out of the tables.

1. The user-level `CLAUDE.md` loaded in every session despite `--setting-sources project,local`.
   It is now excluded with `claudeMdExcludes`.
2. The sandbox refuses every write to a `.git/config`, so a Director could not clone. The
   launcher now runs configuration-writing Git commands after checking their paths and keys.
3. The host gives every shell a temporary folder shared by all sessions. Denying reads there
   made tests hang; now only other sessions' folders in it are denied.
4. The host hides its environment from `ps`, so neither the S3 cut nor the time limit stopped a
   session. Runs are now stopped by process tree and command line.
5. A Director that starts workers in the background ends its turn, as the core prescribes. The
   requester now replies once those workers stop, and the cut applies while they run.
6. The first diff review found containment gaps. Agents now get an explicit environment, read
   nothing under the home folder except their run, have their own dependency cache, and may not
   resume other sessions or load plugins. Grading runs in a sandbox.
7. Runs cut by the host's usage limit are detected and set aside, and the batch stops.

## Spend

{SPEND} at list price, counted from every transcript in the run area. The 18 graded runs cost
{GRADED}. The rest went on pilots of earlier harness versions, runs a defect confounded, runs
cut by the host's usage limit, four completed runs deleted by mistake during a restart, probes,
and the judge.
