#!/usr/bin/env python3
"""Differential test of two independent CNF encoders of the same question
"is there a unique-sum-free A in Z/pZ with |A| = k".

OURS is gen_cnf.py from this repository. OTHER is the pinned encoder
usf_encode_pinned.py from Mark Watson's p59 pipeline (sha256
2eeec8ec926f80ee0d9db55a4f396acc3fe92110cc9bfc78908260a53b1c9003), which is
not redistributed here; ask its author for a copy and put it next to this
script. Both encoders take "p k" and print DIMACS; both put membership of
residue i on variable i+1. For every (p, k) both CNFs go through kissat and
the verdicts are compared with each other and with the known values of m(p).

Usage: diff_test.py out.json  (needs kissat on PATH)
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OURS = os.path.join(HERE, "..", "gen_cnf.py")
OTHER = os.path.join(HERE, "usf_encode_pinned.py")
M = {7: 5, 11: 7, 13: 7, 17: 8, 19: 9, 23: 10, 29: 11, 31: 11}


def solve(enc, p, k):
    cnf = subprocess.run([sys.executable, enc, str(p), str(k)],
                         capture_output=True, text=True, check=True).stdout
    t = time.time()
    r = subprocess.run(["kissat", "-q", "--time=120"], input=cnf,
                       capture_output=True, text=True)
    v = "SAT" if r.returncode == 10 else "UNSAT" if r.returncode == 20 else f"rc{r.returncode}"
    return v, round(time.time() - t, 2), cnf.split("\n", 1)[0]


def main():
    rows, bad = [], 0
    for p, m in M.items():
        for k in range(2, m + 2):
            a, b = solve(OURS, p, k), solve(OTHER, p, k)
            exp = "UNSAT" if k < m else "SAT"
            ok = a[0] == b[0] == exp
            bad += not ok
            rows.append((p, k, a[0], b[0], exp, a[1], b[1], a[2], b[2]))
            print(f"p={p:2d} k={k:2d} ours={a[0]:5s} other={b[0]:5s} expected={exp:5s} "
                  f"{'ok' if ok else 'MISMATCH'}", flush=True)
    print("MISMATCH_COUNT", bad)
    json.dump(rows, open(sys.argv[1], "w"))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
