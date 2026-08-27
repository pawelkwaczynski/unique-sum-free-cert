#!/usr/bin/env python3
"""Independent check of a list of affine-class representatives (msearch2 --list).

For each representative A (a line "W {..}") of size k in Z/pZ:
  - A is unique-sum-free (definition check),
  - A is canonical: the lexicographically least image over all affine maps
    x -> a x + b (so distinct lines are distinct classes),
  - |Stab(A)| under AGL(1,p), hence the number of normalized images of the
    class (images containing {0, 1}) = k (k - 1) / |Stab(A)|.
Sums over all classes:
  N = number of normalized unique-sum-free sets of size k (all classes),
  F = number of those fixed by the reflection x -> 1 - x,
  predicted msearch (v1) --count = (N + F) / 2.
If v1's independent count equals the prediction, the list is complete.
Usage: verify_classes.py p k list.txt [v1_count]
"""
import sys
from count_orbits_bruteforce import is_usf, canon


def parse(path):
    reps = []
    for line in open(path):
        if line.startswith("W "):
            body = line[2:].strip().strip("{}")
            reps.append(tuple(int(x) for x in body.split(",") if x != ""))
    return reps


def main():
    p, k, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    v1 = int(sys.argv[4]) if len(sys.argv) > 4 else None
    reps = parse(path)
    seen = set()
    N = F = 0
    bad = 0
    for A in reps:
        ok = len(A) == k and len(set(A)) == k and is_usf(A, p) and canon(A, p) == tuple(sorted(A))
        if not ok or A in seen:
            bad += 1
            print("BAD", A, "usf" if is_usf(A, p) else "not-usf",
                  "canonical" if canon(A, p) == tuple(sorted(A)) else "not-canonical",
                  "duplicate" if A in seen else "")
        seen.add(A)
        images = set()
        for a in range(1, p):
            for b in range(p):
                img = tuple(sorted((a * x + b) % p for x in A))
                if 0 in img and 1 in img:
                    images.add(img)
        stab = k * (k - 1) // len(images)
        assert k * (k - 1) % len(images) == 0, (A, len(images))
        fixed = sum(1 for img in images if tuple(sorted((1 - x) % p for x in img)) == img)
        N += len(images)
        F += fixed
    print(f"p={p} k={k} classes={len(reps)} bad={bad} normalized_witnesses={N} reflection_fixed={F} "
          f"predicted_v1={(N + F) // 2}" + (f" v1={v1} {'MATCH' if v1 == (N + F) // 2 else 'MISMATCH'}" if v1 is not None else ""))


if __name__ == "__main__":
    main()
