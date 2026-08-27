#!/usr/bin/env python3
"""Independent check for msearch2 --count: brute-force count of affine-orbit
classes of minimum unique-sum-free sets in Z/pZ.

A is unique-sum-free (USF) if no residue g has exactly one unordered
representation g = a + b with a, b in A (a = b allowed, counted once).
Orbits under AGL(1,p): x -> a x + b, a != 0. Canonical form = lexicographically
smallest sorted image; count distinct canonical forms among all USF sets of
size k containing {0, 1} (every orbit has such a representative).
Also reports which sizes k in [m(p), p] admit a USF set (interval check).
Usage: count_orbits_bruteforce.py p k [--sizes]
"""
import sys
from itertools import combinations


def is_usf(A, p):
    reps = [0] * p
    lst = sorted(A)
    n = len(lst)
    for i in range(n):
        for j in range(i, n):
            reps[(lst[i] + lst[j]) % p] += 1
    return all(r != 1 for r in reps)


def canon(A, p):
    best = None
    for a in range(1, p):
        for b in range(p):
            img = tuple(sorted((a * x + b) % p for x in A))
            if best is None or img < best:
                best = img
    return best


def count_orbits(p, k):
    rest = [x for x in range(2, p)]
    classes = set()
    total = 0
    for comb in combinations(rest, k - 2):
        A = (0, 1) + comb
        if is_usf(A, p):
            total += 1
            classes.add(canon(A, p))
    return total, classes


def main():
    p, k = int(sys.argv[1]), int(sys.argv[2])
    if "--sizes" in sys.argv:
        sizes = []
        for kk in range(k, p + 1):
            found = any(is_usf((0, 1) + c, p) for c in combinations(range(2, p), kk - 2))
            sizes.append((kk, found))
        print(f"p={p} sizes " + " ".join(f"{kk}:{'SAT' if f else 'UNSAT'}" for kk, f in sizes))
        return
    total, classes = count_orbits(p, k)
    reps = sorted(classes)
    print(f"p={p} k={k} normalized_witnesses={total} orbits={len(classes)} reps={[list(r) for r in reps]}")


if __name__ == "__main__":
    main()
