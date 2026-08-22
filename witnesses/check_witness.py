#!/usr/bin/env python3
"""Check every witness in witnesses.json directly against the definition.
Independent of the SAT encoding: this is the upper-bound half of m(p)."""
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))


def is_usf(p, A):
    A = sorted(set(A))
    if not A or any(not (0 <= a < p) for a in A):
        return False
    pairs = Counter()
    for i, a in enumerate(A):
        for b in A[i:]:
            pairs[(a + b) % p] += 1
    return all(v >= 2 for v in pairs.values())


def main():
    data = json.load(open(os.path.join(HERE, "witnesses.json")))
    bad = 0
    for p, A in sorted(data["witnesses"].items(), key=lambda kv: int(kv[0])):
        ok = is_usf(int(p), A)
        bad += not ok
        print(f"p={p:>3} |A|={len(A):>2} {'ok' if ok else 'FAIL'}  {A}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
