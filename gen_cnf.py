#!/usr/bin/env python3
"""SAT encoding for m(p): minimum size of A subset of Z/pZ with no unique sum.

Question encoded: does there exist A with |A| = k and no unique sum?
  - unique sum of A: g in A+A with exactly ONE pair {a,b} (a=b allowed), a+b=g.
  - "no unique sum": every g has 0 or >=2 such unordered pairs.

Encoding:
  x_i  (i in 0..p-1)          : i in A
  y_P  (P = {i,j}, i<=j)      : both endpoints of P in A  (y <-> x_i & x_j)
  for each pair P with sum g  : y_P -> OR of other pairs with the same sum
  cardinality |A| = k         : Sinz sequential counter (at-most-k both ways)

WLOG normalization: affine maps x -> c*x + t preserve the no-unique-sum
property (pair sums transform bijectively g -> c*g + 2t), and any A with
|A| >= 2 can be mapped so that {0,1} is contained in A. Hence unit clauses
x_0 and x_1 are sound for k >= 2.

Usage: gen_cnf.py p k > out.cnf
"""
import sys


def sinz_at_most(lits, k, next_var, clauses):
    """Sequential counter: at most k of lits are true. Returns next free var."""
    n = len(lits)
    if k >= n:
        return next_var
    if k == 0:
        for l in lits:
            clauses.append([-l])
        return next_var
    # s[i][j] : among first i+1 literals at least j+1 are true
    s = [[0] * k for _ in range(n)]
    for i in range(n):
        for j in range(k):
            s[i][j] = next_var
            next_var += 1
    clauses.append([-lits[0], s[0][0]])
    for j in range(1, k):
        clauses.append([-s[0][j]])
    for i in range(1, n):
        clauses.append([-lits[i], s[i][0]])
        clauses.append([-s[i - 1][0], s[i][0]])
        for j in range(1, k):
            clauses.append([-lits[i], -s[i - 1][j - 1], s[i][j]])
            clauses.append([-s[i - 1][j], s[i][j]])
        clauses.append([-lits[i], -s[i - 1][k - 1]])
    return next_var


def build(p, k, sumset_bound=True, reflection_break=True):
    x = list(range(1, p + 1))  # x[i] = var i+1
    next_var = p + 1
    clauses = []

    pairs = []            # (i, j, var) with i <= j
    by_sum = {}           # g -> list of pair vars
    for i in range(p):
        for j in range(i, p):
            v = next_var
            next_var += 1
            pairs.append((i, j, v))
            by_sum.setdefault((i + j) % p, []).append(v)
            clauses.append([-v, x[i]])
            clauses.append([-v, x[j]])
            clauses.append([-x[i], -x[j], v])

    # no unique sum: a lone pair for some sum g is forbidden
    for g, vs in by_sum.items():
        for v in vs:
            clauses.append([-v] + [w for w in vs if w != v])

    # WLOG 0,1 in A (affine normalization)
    clauses.append([x[0]])
    clauses.append([x[1]])

    # |A| = k
    next_var = sinz_at_most(x, k, next_var, clauses)
    next_var = sinz_at_most([-v for v in x], p - k, next_var, clauses)

    if sumset_bound:
        # z_g: sum g is present (one direction suffices for the upper bound).
        # No unique sum forces >=2 pairs per present sum, and k elements give
        # k(k+1)/2 unordered pairs, so |A+A| <= floor(k(k+1)/4).
        z = {}
        for g, vs in by_sum.items():
            zg = next_var
            next_var += 1
            z[g] = zg
            for v in vs:
                clauses.append([-v, zg])
        next_var = sinz_at_most(list(z.values()), (k * (k + 1)) // 4,
                                next_var, clauses)

    if reflection_break:
        # residual symmetry fixing {0,1}: a -> 1-a. Lex-leader x <= sigma(x)
        # over residues 2..p-1 paired with their images.
        order = [r for r in range(2, p)]
        sigma = {r: (1 - r) % p for r in order}
        # chain of "all equal so far" vars
        eq_prev = None
        for r in order:
            s = sigma[r]
            if s == r or s < 2:
                continue
            xr, xs = x[r], x[s]
            if eq_prev is None:
                clauses.append([-xr, xs])          # x_r <= x_s
                eq = next_var
                next_var += 1
                # eq <-> (x_r == x_s)
                clauses.append([-eq, -xr, xs])
                clauses.append([-eq, xr, -xs])
                clauses.append([eq, xr, xs])
                clauses.append([eq, -xr, -xs])
                eq_prev = eq
            else:
                clauses.append([-eq_prev, -xr, xs])
                eq = next_var
                next_var += 1
                clauses.append([-eq, -eq_prev])
                clauses.append([-eq, -xr, xs])
                clauses.append([-eq, xr, -xs])
                clauses.append([eq, -eq_prev, xr, xs])
                clauses.append([eq, -eq_prev, -xr, -xs])
                eq_prev = eq

    return next_var - 1, clauses


def main():
    p, k = int(sys.argv[1]), int(sys.argv[2])
    nvars, clauses = build(p, k)
    out = sys.stdout
    out.write(f"p cnf {nvars} {len(clauses)}\n")
    for c in clauses:
        out.write(" ".join(map(str, c)) + " 0\n")


if __name__ == "__main__":
    main()
