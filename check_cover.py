#!/usr/bin/env python3
"""Check a cover ledger without a solver: every row must be PASS (drat-trim and
cake_lpr verified) and its cnf_sha256 must equal the hash of the cover formula
rebuilt from the ledger's cubes, so the certificate is bound to the partition
actually used. Exit 0 when the top-level cover and every child cover that the
coverage audit relies on are present and bound.

Usage: check_cover.py p k certified.jsonl cover.jsonl
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cubes import tag_units, children_tags, serialize_cnf
from cover_cert import card_formula


def main():
    p, k, ledger, cover = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    last = {}
    for line in open(ledger):
        if line.strip():
            r = json.loads(line); last[r["cube"]] = r
    verified = {t for t, r in last.items() if r.get("status") == "UNSAT" and r.get("proof_verified")}
    rows = {}
    for line in open(cover):
        if line.strip():
            r = json.loads(line); rows[r["cover"]] = r
    if "whole" in verified:
        print(f"p={p} k={k}: whole formula, no cover needed"); return 0
    nv, base = card_formula(p, k)
    bad = 0
    top = [f"c{c}_d{d}" for c in range(2, p) for d in range(c + 1, p)]
    expect = {"top-level": base + [[-u for u in tag_units(p, t)] for t in top]}
    for par in {t.rsplit("_", 1)[0] for t in last if t.count("_") >= 2}:
        if par not in verified and children_tags(p, par):
            expect[par] = base + [[u] for u in tag_units(p, par)] + [[-u for u in tag_units(p, kt)] for kt in children_tags(p, par)]
    for name, clauses in expect.items():
        r = rows.get(name)
        h = hashlib.sha256(serialize_cnf(nv, clauses, [])).hexdigest()
        if r is None:
            print(f"MISSING cover {name}"); bad += 1
        elif r.get("verdict") != "PASS" or r.get("drat_trim") != "VERIFIED" or r.get("cake_lpr") != "VERIFIED":
            print(f"NOT VERIFIED cover {name}"); bad += 1
        elif r.get("cnf_sha256") != h:
            print(f"HASH MISMATCH cover {name}"); bad += 1
    print(f"p={p} k={k}: {len(expect) - bad}/{len(expect)} cover certificates bound and verified")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
