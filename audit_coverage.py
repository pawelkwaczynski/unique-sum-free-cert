#!/usr/bin/env python3
"""Coverage auditor for the certificate ledgers. The only source of a verdict.
Fail-closed.

The auditor does not trust what the ledger says about itself:
  - a row counts only with the full set of fields: p, k, cube, status,
    proof_verified, verdict=PASS, cake_lpr=VERIFIED (rc 0), cnf_sha256, and either
    drat_trim=VERIFIED (rc 0) or chain=cadical-lrat-cake_lpr with lrat_sha256
    (native LRAT, no drat-trim); p and k must match the arguments;
  - for every accepted tag the auditor rebuilds the exact CNF
    (gen_cnf.build plus the cube's unit clauses, same serialization as the
    certifier) and compares sha256, so a proof is bound to a formula, not to
    a name;
  - a SAT row is accepted only after its witness is checked directly against
    the definition (|A| = k, no unique sum in Z/pZ); a bad witness is a hard
    audit failure.

Coverage: the base is the set of fine cubes (c, d) with 2 <= c < d <= p-1
(k >= 4). A cube is covered directly or by the complete set of its children
(c, d, e), e in d+1..p-1 (k >= 5), recursively. The tag "whole" (the entire
formula, used for k <= 4) covers everything without a coverage argument.

Usage: audit_coverage.py p k ledger.jsonl
Exit code: 0 = UNSAT-CERTIFIED, 10 = SAT, 1 = INCOMPLETE or error
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_cnf
from cubes import tag_units, children_tags, cnf_sha256


def units_for_tag(p, tag):
    try:
        return tag_units(p, tag)
    except (ValueError, IndexError):
        return None


def witness_ok(p, k, A):
    """Check a witness directly against the definition: |A| = k and every
    element of A+A has at least two unordered pairs {a, b} (a = b allowed)."""
    A = sorted(set(A))
    if len(A) != k or any(not (0 <= a < p) for a in A):
        return False
    from collections import Counter
    pairs = Counter()
    for i, a in enumerate(A):
        for b in A[i:]:
            pairs[(a + b) % p] += 1
    return all(v >= 2 for v in pairs.values())


def covered_by_children(p, k, tag, verified, depth=0):
    """A cube is covered when every child is verified directly or covered by
    its own children. The requirement k >= (number of fixed elements) + 2
    keeps the coverage argument valid: for smaller k the cubes do not exhaust
    the search space."""
    level = len(tag.split("_")) + 1
    if k < level + 2 or depth > 6:
        return False
    kids = children_tags(p, tag)
    if not kids:
        return False
    return all(kt in verified or covered_by_children(p, k, kt, verified, depth + 1)
               for kt in kids)


def main():
    p, k, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    nvars, clauses = gen_cnf.build(p, k)

    candidates, sat_entries, rejected = {}, [], []
    for ln, line in enumerate(open(out), 1):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            rejected.append((ln, "invalid JSON"))
            continue
        if e.get("p") != p or e.get("k") != k:
            rejected.append((ln, f"p/k={e.get('p')}/{e.get('k')} does not match"))
            continue
        st = e.get("status")
        if st == "SAT":
            sat_entries.append((ln, e))
        elif st == "UNSAT":
            # Two proof chains are accepted. Either kissat -> DRAT -> drat-trim -> LRAT
            # -> cake_lpr (drat_trim must be VERIFIED), or cadical -> LRAT -> cake_lpr
            # (chain = "cadical-lrat-cake_lpr", lrat_sha256 present, drat-trim skipped by
            # design). In both the verdict comes from cake_lpr, the formally verified checker.
            native = (e.get("chain") == "cadical-lrat-cake_lpr" and bool(e.get("lrat_sha256")))
            trim_ok = (e.get("drat_trim") == "VERIFIED" and e.get("drat_trim_rc") == 0)
            if (e.get("proof_verified") is True and e.get("verdict") == "PASS"
                    and (trim_ok or native)
                    and e.get("cake_lpr") == "VERIFIED" and e.get("cake_lpr_rc") == 0
                    and e.get("cnf_sha256")):
                candidates[e["cube"]] = e["cnf_sha256"]
            elif e.get("proof_verified"):
                rejected.append((ln, f"{e.get('cube')}: proof_verified without the full field set"))
        # TIMEOUT and ERROR rows count for nothing

    for ln, e in sat_entries:
        w = e.get("witness")
        if w is None or not witness_ok(p, k, w):
            print(f"AUDIT ERROR: SAT row (line {ln}) with a witness that fails "
                  f"the definition: {w}")
            sys.exit(1)
    if sat_entries:
        print(f"VERDICT: SAT, {len(sat_entries)} witnesses checked against the "
              f"definition, first: {sat_entries[0][1].get('witness')}")
        sys.exit(10)

    verified = set()
    bad_hash = []
    for tag, claimed in candidates.items():
        units = units_for_tag(p, tag)
        if units is None:
            bad_hash.append((tag, "invalid tag"))
            continue
        if cnf_sha256(nvars, clauses, units) == claimed:
            verified.add(tag)
        else:
            bad_hash.append((tag, "cnf_sha256 does not match the rebuilt formula"))
    if bad_hash:
        for tag, why in bad_hash[:10]:
            print(f"REJECTED: {tag}: {why}")
        print("VERDICT: INCOMPLETE (rows not bound to the formula)")
        sys.exit(1)

    if "whole" in verified:
        print(f"p={p} k={k}: certificate for the whole formula, rebuilt hash matches")
        print("VERDICT: UNSAT-CERTIFIED (whole formula, proof_verified)")
        sys.exit(0)

    if k < 4:
        print("VERDICT: INCOMPLETE (k < 4 needs a whole-formula certificate; cubes do not cover)")
        sys.exit(1)

    missing = []
    n_parent = n_children = 0
    for c in range(2, p):
        for d in range(c + 1, p):
            tag = f"c{c}_d{d}"
            if tag in verified:
                n_parent += 1
                continue
            if covered_by_children(p, k, tag, verified):
                n_children += 1
                continue
            missing.append(tag)

    total = (p - 2) * (p - 3) // 2
    print(f"p={p} k={k}: cubes {total}, direct {n_parent}, "
          f"via children {n_children}, missing {len(missing)}, "
          f"rejected rows {len(rejected)}")
    if missing:
        print("MISSING:", ", ".join(missing[:20]), "..." if len(missing) > 20 else "")
        print("VERDICT: INCOMPLETE")
        sys.exit(1)
    print("VERDICT: UNSAT-CERTIFIED (full coverage, every proof bound to the "
          "formula through the rebuilt cnf_sha256)")
    sys.exit(0)


if __name__ == "__main__":
    main()
