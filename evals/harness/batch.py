"""Run and grade a grid of scenario, configuration, and repetition in a shuffled order.

Usage: python3 -I evals/harness/batch.py --scenarios s1-run-input s2-db-outage --configs A B C
                                         --reps 1 2 [--parallel 3] [--seed 7] [--home DIR]
"""

import argparse
import random
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenarios", nargs="+", required=True)
    ap.add_argument("--configs", nargs="+", required=True)
    ap.add_argument("--reps", nargs="+", type=int, default=[1])
    ap.add_argument("--parallel", type=int, default=3)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--home")
    args = ap.parse_args()
    home = ["--home", args.home] if args.home else []
    jobs = [(s, c, r) for s in args.scenarios for c in args.configs for r in args.reps]
    random.Random(args.seed).shuffle(jobs)
    print("order:", " ".join(f"{s.split('-')[0]}-{c}-r{r}" for s, c, r in jobs), flush=True)
    slots = threading.Semaphore(args.parallel)

    def work(job):
        s, c, r = job
        with slots:
            out = subprocess.run([sys.executable, "-I", str(HERE / "run.py"), s, c, "--rep", str(r),
                                  *home], capture_output=True, text=True)
            run = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else ""
            if out.returncode or not run:
                print(f"failed {s} {c} r{r}: {out.stderr[-500:]}", flush=True)
                return
            g = subprocess.run([sys.executable, "-I", str(HERE / "grade.py"), run],
                               capture_output=True, text=True)
            print(f"{'graded' if g.returncode == 0 else 'grade failed'} {run}", flush=True)

    threads = []
    for job in jobs:
        t = threading.Thread(target=work, args=(job,))
        t.start()
        threads.append(t)
        time.sleep(5)
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
