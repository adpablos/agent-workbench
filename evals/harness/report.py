"""Summarize graded runs as Markdown tables, one per scenario, with ranges per configuration.

Usage: python3 -I evals/harness/report.py [--home DIR] [--runs GLOB]
"""

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402


def span(values, fmt="{:.2f}"):
    values = [v for v in values if v is not None]
    if not values:
        return "–"
    med = statistics.median(values)
    if len(values) == 1 or min(values) == max(values):
        return fmt.format(med)
    return f"{fmt.format(med)} ({fmt.format(min(values))}–{fmt.format(max(values))})"


def violations(r):
    s, c = r["safety"], r["config_repo"]
    found = []
    if s["pushed"]:
        found.append("push")
    if s["references_changed"]:
        found.append("reference changed")
    if c["changed_before_approval"]:
        found.append("chart before approval")
    if s["outside_file_writes"]:
        found.append("write outside")
    return found


def f2p(r):
    states = list(r["tests"].get("fail_to_pass", {}).values())
    return sum(x == "passed" for x in states) / len(states) if states else 0.0


def details(results):
    """One line per run: what the totals hide."""
    rows = ["| Run | Resolved | USD | Main USD | Sessions (main / worker / subagent) | "
            "Reviews | Claimed done | Continuity |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(results, key=lambda r: (r["config"], r["rep"])):
        c = r.get("continuity")
        cont = "–" if not c else (
            f"kept {c['partial_edit_kept']:.0%} of the cut edit; "
            f"{'duplicate copy' if c['duplicate_copy'] else 'no duplicate copy'}; "
            f"{len(c['task_records'])} task records" if c["partial_edit_kept"] is not None
            else "no edit at cut")
        roles = r["friction"]["sessions_by_role"]
        rows.append("| " + " | ".join([
            f"{r['config']} r{r['rep']}", "yes" if r["tests"]["resolved"] else "no",
            f"{r['cost']['usd']:.2f}", f"{r['cost']['usd_main']:.2f}",
            f"{roles['main']} / {roles['worker']} / {roles['subagent']}",
            str(r["review_sessions"]), "yes" if r["claimed_done"] else "no", cont]) + " |")
    return "\n".join(rows)


def table(results):
    rows = ["| Config | Runs | Resolved | Fail-to-pass passed | Chart | Violations | USD | "
            "Tokens in / cache write / cache read / out (k) | Sessions | Model calls | "
            "Peak context main (k) | Wall (min) | Replies scripted / fallback |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    by = defaultdict(list)
    for r in results:
        by[r["config"]].append(r)
    for config in sorted(by):
        rs = by[config]
        tok = lambda k: span([r["cost"]["tokens"].get(k, 0) / 1000 for r in rs], "{:.0f}")  # noqa
        chart = [r["config_repo"].get("passed") for r in rs]
        rows.append("| " + " | ".join([
            config, str(len(rs)),
            f"{sum(r['tests']['resolved'] for r in rs)}/{len(rs)}",
            span([f2p(r) for r in rs], "{:.0%}"),
            "–" if all(c is None for c in chart) else f"{sum(bool(c) for c in chart)}/{len(rs)}",
            ", ".join(sorted({v for r in rs for v in violations(r)})) or "none",
            span([r["cost"]["usd"] for r in rs]),
            " / ".join(tok(k) for k in ("input", "cache_write", "cache_read", "output")),
            span([r["friction"]["sessions"] for r in rs], "{:.0f}"),
            span([r["friction"]["model_calls"] for r in rs], "{:.0f}"),
            span([r["friction"]["peak_context_main"] / 1000 for r in rs], "{:.0f}"),
            span([r["friction"]["wall_seconds"] / 60 for r in rs], "{:.0f}"),
            f"{span([r['friction']['replies_scripted'] for r in rs], '{:.0f}')} / "
            f"{span([r['friction']['replies_fallback'] for r in rs], '{:.0f}')}",
        ]) + " |")
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home")
    ap.add_argument("--runs", default="s*-*-r*")
    args = ap.parse_args()
    results = [json.loads(p.read_text())
               for p in sorted((common.home(args.home) / "runs").glob(f"{args.runs}/result.json"))
               if not json.loads((p.parent / "record.json").read_text()).get("host_limit")]
    by = defaultdict(list)
    for r in results:
        by[r["scenario"]].append(r)
    for scenario in sorted(by):
        print(f"### {scenario}\n\n{table(by[scenario])}\n\n{details(by[scenario])}\n")


if __name__ == "__main__":
    main()
