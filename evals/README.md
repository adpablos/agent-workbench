# Evals

An empirical eval of the core's way of working. It runs real coding tickets on real repositories
under several configurations and measures outcome, safety, continuity, cost, and friction from
the host's own records. [DESIGN.md](DESIGN.md) says what it measures and why; the latest results
are in [reports/](reports/).

It is a measurement kit, not part of the operating contract: nothing here changes what a
workbench does.

## Contents

| Path | What it holds |
|---|---|
| `scenarios/<name>/` | `scenario.json` (pinned repositories, fix commit, hidden test identifiers, expected stops and their replies, configuration check), `TICKET.md` in our words, and `hidden-tests.patch`, the upstream fix's test changes |
| `configs/<name>.json` | One configuration: layout (`bare` or `workbench`), core revision, and the prompt |
| `workbench/POLICY.md` | The approved policy for workbench runs |
| `harness/run.py` | Builds a run, runs its sessions with the scripted requester, and writes `record.json` |
| `harness/grade.py` | Grades a run into `result.json`; `--selfcheck` checks a scenario's hidden tests |
| `harness/report.py` | Tables per scenario and configuration, with ranges |
| `harness/probe.py` | Checks a run's containment before you rely on it |
| `harness/launcher.py` | Starts the sessions that agents request, with the run's fixed settings |
| `harness/judge.md` | The rubric that classifies the agent's last message for the scripted requester |

The hidden tests come from Apache-2.0 projects and keep that license. Tickets are written for this
kit and link to the source issues only in `scenario.json`, which agents never see.

## Requirements

- macOS with Claude Code signed in. The shell sandbox and the `ps` options it uses are macOS
  ones; other platforms need their own containment check.
- Git, Python 3.14 as `python3.14`, and network access for the first run of each scenario, which
  clones the repositories and fills the dependency cache.
- A run area outside any repository, `~/awe-runs` by default or `AWE_HOME`. It holds mirrors,
  caches, runs, and grading folders, and never goes into this repository: runs contain session
  transcripts.

## Run

From the root of this repository:

```bash
python3 -I evals/harness/grade.py --selfcheck s1-run-input
python3 -I evals/harness/probe.py
python3 -I evals/harness/run.py s1-run-input B --rep 1
python3 -I evals/harness/grade.py ~/awe-runs/runs/<run>
python3 -I evals/harness/report.py
```

`run.py` prints the run folder. Run several at once from separate shells; each run has its own
folder, remotes, and launcher. A run stops after four requester replies or 120 minutes
(`--limit-minutes`).

## Add a configuration

A candidate core is a new file in `configs/`, for example `configs/D.json`:

```json
{
  "title": "Candidate core",
  "layout": "workbench",
  "core": "<commit or tag of this repository>",
  "prompt": "Work on the ticket in TICKET.md."
}
```

`run.py` exports that revision of this repository into the workbench's `core/` with `git
archive`, so a candidate needs a commit, not a release. `--core <rev>` overrides the revision for
one run. The harness does not change.

## Add a scenario

Pick a fix merged after the model's training data ends, in a project whose instructions accept
AI-assisted work. Pin the base (the fix's parent) and the fix, write the ticket in your own
words, save the fix's test changes as `hidden-tests.patch`, and list the tests that fail before
the fix. Then run `grade.py --selfcheck <scenario>` and copy the collected count into
`expected_count`.
