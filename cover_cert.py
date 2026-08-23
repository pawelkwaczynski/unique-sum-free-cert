#!/usr/bin/env python3
"""Machine-checked cover completeness (after Szeider, LRAT-Catcher, Thm 5.1).

For a ledger of (p, k) the cube partition is complete if the formula
    x_0 and x_1 and |A| = k and (for every cube C used: not C)
is unsatisfiable, where "not C" is the clause made of the negated unit
literals of C. A DRAT refutation of that formula, checked by drat-trim and
cake_lpr, replaces the hand proof of Proposition 2 for that (p, k).

Two certificates per ledger: the top-level cover (all c_d cubes, or the
single "whole" tag) and, for every cube that was closed through its
children, a child cover: units(parent) and (for every child: not child).

Usage: cover_cert.py p k ledger.jsonl out.jsonl  [--tools DIR]
Writes one JSON row per certificate with cnf_sha256, drat_sha256, verdict.
Exit 0 when every cover certificate verified, 1 otherwise.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_cnf
from cubes import tag_units, children_tags, serialize_cnf


def card_formula(p, k):
    """x_0, x_1 and |A| = k only (no USF clauses): the cover must not rely on them."""
    x = list(range(1, p + 1))
    nv = p
    clauses = [[x[0]], [x[1]]]
    nv = gen_cnf.sinz_at_most(x, k, nv + 1, clauses) - 1
    nv = gen_cnf.sinz_at_most([-v for v in x], p - k, nv + 1, clauses) - 1
    return nv, clauses


def refute(nv, clauses, tools, keep=None):
    cnf = serialize_cnf(nv, clauses, [])
    with tempfile.TemporaryDirectory() as d:
        cp, dp = os.path.join(d, "f.cnf"), os.path.join(d, "f.drat")
        open(cp, "wb").write(cnf)
        r = subprocess.run(["kissat", "-q", cp, dp], capture_output=True, text=True)
        if r.returncode != 20:
            return {"solver_rc": r.returncode, "verdict": "NOT-UNSAT"}
        env = dict(os.environ, DRAT_TRIM=os.path.join(tools, "drat-trim", "drat-trim"),
                   CAKE_LPR=os.path.join(tools, "cake_lpr", "cake_lpr"))
        v = subprocess.run([os.path.join(HERE, "verify_drat.sh"), cp, dp],
                           capture_output=True, text=True, env=env)
        row = json.loads(v.stdout.strip().splitlines()[-1]) if v.stdout.strip() else {"verdict": "FAIL"}
        row["cnf_sha256"] = hashlib.sha256(cnf).hexdigest()
        row["solver_rc"] = 20
        return row


def main():
    args = sys.argv[1:]
    tools = os.path.join(HERE, "tools")
    if "--tools" in args:
        i = args.index("--tools"); tools = args[i + 1]; del args[i:i + 2]
    p, k, ledger, out = int(args[0]), int(args[1]), args[2], args[3]
    last = {}
    for line in open(ledger):
        if line.strip():
            r = json.loads(line); last[r["cube"]] = r
    verified = {t for t, r in last.items() if r.get("status") == "UNSAT" and r.get("proof_verified")}
    nv, base = card_formula(p, k)
    rows, bad = [], 0

    if "whole" in verified:
        rows.append({"cover": "whole", "note": "single certificate for the whole formula, no partition"})
    else:
        top = [f"c{c}_d{d}" for c in range(2, p) for d in range(c + 1, p)]
        clauses = base + [[-u for u in tag_units(p, t)] for t in top]
        row = refute(nv, clauses, tools); row["cover"] = "top-level"; row["cubes"] = len(top)
        rows.append(row); bad += row.get("verdict") != "PASS"
        # child covers for every cube not verified directly but used through children
        parents = sorted({t.rsplit("_", 1)[0] for t in verified if "_" in t and t.count("_") >= 2} |
                         {t.rsplit("_", 1)[0] for t in last if t.count("_") >= 2})
        for par in parents:
            if par in verified:
                continue
            kids = children_tags(p, par)
            if not kids:
                continue
            clauses = base + [[u] for u in tag_units(p, par)] + [[-u for u in tag_units(p, kt)] for kt in kids]
            row = refute(nv, clauses, tools); row["cover"] = par; row["cubes"] = len(kids)
            rows.append(row); bad += row.get("verdict") != "PASS"
    with open(out, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    n = sum(1 for r in rows if r.get("verdict") == "PASS")
    print(f"p={p} k={k}: cover certificates {n}/{len(rows) - ('whole' in verified)} PASS" if "whole" not in verified
          else f"p={p} k={k}: whole formula, no cover needed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
