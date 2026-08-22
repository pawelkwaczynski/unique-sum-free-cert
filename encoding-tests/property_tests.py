#!/usr/bin/env python3
"""Property tests for gen_cnf.py that do not need a second encoder.

1. Whole group: A = Z/pZ is unique-sum-free (every sum has p ordered
   representations), so (p, k = p) must be SAT. The lex-leader bug fixed on
   2026-08-23 made this UNSAT: the chain clause excluded every assignment whose
   first two reflection-orbit pairs were equal, and the whole group is one.
2. Symmetry breaker is sound: for every (p, k) with p <= 23 the verdict with
   the reflection breaker equals the verdict without it.

Usage: property_tests.py   (kissat on PATH; a few minutes)
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import gen_cnf


def verdict(p, k, **kw):
    nv, cl = gen_cnf.build(p, k, **kw)
    cnf = f"p cnf {nv} {len(cl)}\n" + "".join(
        " ".join(map(str, dict.fromkeys(c))) + " 0\n" for c in cl)
    r = subprocess.run(["kissat", "-q", "--time=120"], input=cnf,
                       capture_output=True, text=True)
    return {10: "SAT", 20: "UNSAT"}.get(r.returncode, f"rc{r.returncode}")


def main():
    bad = 0
    for p in (5, 7, 11, 13, 17, 19, 23):
        v = verdict(p, p)
        print(f"whole group p={p}: {v}")
        bad += v != "SAT"
    n = 0
    for p in (5, 7, 11, 13, 17, 19, 23):
        for k in range(2, p + 1):
            a, b = verdict(p, k), verdict(p, k, reflection_break=False)
            n += 1
            if a != b:
                bad += 1
                print(f"breaker changes verdict at p={p} k={k}: {a} vs {b}")
    print(f"breaker equivalence: {n} pairs checked")
    print("FAILURES", bad)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
