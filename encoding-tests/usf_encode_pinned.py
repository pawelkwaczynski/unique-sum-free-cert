#!/usr/bin/env python3
"""Pinned USF CNF encoder, derived from the validated unpinned baseline.

For k >= 2 this adds the theorem-certified unit clauses x_0 and x_1.  All
other clauses are intentionally identical to usf_encode.py.
"""
import sys


class CNF:
    def __init__(self, nvars):
        self.n = nvars
        self.clauses = []

    def new(self):
        self.n += 1
        return self.n

    def add(self, *lits):
        self.clauses.append(list(lits))

    def dimacs(self):
        out = [f"p cnf {self.n} {len(self.clauses)}"]
        out += [" ".join(map(str, c)) + " 0" for c in self.clauses]
        return "\n".join(out) + "\n"


def seq_counter_atmost(cnf, lits, k):
    """Sinz sequential counter: at most k of lits are true."""
    n = len(lits)
    if k >= n:
        return
    if k == 0:
        for x in lits:
            cnf.add(-x)
        return
    s = [[cnf.new() for _ in range(k)] for _ in range(n)]
    cnf.add(-lits[0], s[0][0])
    for j in range(1, k):
        cnf.add(-s[0][j])
    for i in range(1, n):
        cnf.add(-lits[i], s[i][0])
        cnf.add(-s[i - 1][0], s[i][0])
        for j in range(1, k):
            cnf.add(-lits[i], -s[i - 1][j - 1], s[i][j])
            cnf.add(-s[i - 1][j], s[i][j])
        cnf.add(-lits[i], -s[i - 1][k - 1])


def encode(p, k):
    """CNF for a size-k USF subset, pinned to contain 0 and 1 when k >= 2."""
    assert p % 2 == 1, "odd modulus only; the halving argument needs 2 invertible"
    cnf = CNF(p)
    x = lambda i: i + 1  # noqa: E731  variable for membership of i

    inv2 = pow(2, p - 2, p)
    for s in range(p):
        h = (s * inv2) % p
        pairs = []
        seen = set()
        for a in range(p):
            b = (s - a) % p
            if a == b:
                continue
            key = (min(a, b), max(a, b))
            if key in seen:
                continue
            seen.add(key)
            pairs.append(key)
        ys = []
        for (a, b) in pairs:
            y = cnf.new()
            cnf.add(-y, x(a))
            cnf.add(-y, x(b))
            cnf.add(-x(a), -x(b), y)
            ys.append(y)
        cnf.add(-x(h), *ys)
        for j, yj in enumerate(ys):
            cnf.add(x(h), -yj, *[ys[m] for m in range(len(ys)) if m != j])

    mem = [x(i) for i in range(p)]
    seq_counter_atmost(cnf, mem, k)
    seq_counter_atmost(cnf, [-v for v in mem], p - k)

    if k >= 2:
        cnf.add(x(0))
        cnf.add(x(1))
    return cnf


def is_usf(p, A):
    """Reference predicate, independent of the encoder. Ordered count criterion."""
    S = set(A)
    for s in range(p):
        r = 0
        for a in S:
            if (s - a) % p in S:
                r += 1
        if r == 1 or r == 2:
            return False
    return True


if __name__ == "__main__":
    p, k = int(sys.argv[1]), int(sys.argv[2])
    sys.stdout.write(encode(p, k).dimacs())
