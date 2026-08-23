#!/usr/bin/env python3
"""Export a certificate ledger to the per-cube row layout used by
mkwatson/unique-sums-notes (results.jsonl), so the two projects' hash-bound
certificates can be compared and cross-referenced.

Usage: export_ledger.py p k ledger.jsonl out_dir
Writes out_dir/results.jsonl and out_dir/summary.json. Only rows that are
UNSAT with proof_verified are exported; the coverage argument itself lives in
audit_coverage.py and is summarized, not re-derived, here.
"""
import collections
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_cnf
from cubes import serialize_cnf

CUBER = "position cubes: c, d, e = 3rd, 4th, 5th smallest element of A after fixing 0, 1 in A; residues between fixed elements excluded"


def main():
    p, k, ledger, out_dir = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    enc_sha = hashlib.sha256(open(os.path.join(here, "gen_cnf.py"), "rb").read()).hexdigest()
    nv, cl = gen_cnf.build(p, k)
    base_sha = hashlib.sha256(serialize_cnf(nv, cl, [])).hexdigest()

    last = {}
    for line in open(ledger):
        if line.strip():
            r = json.loads(line)
            last[r["cube"]] = r
    rows = []
    for tag, r in last.items():
        if r.get("status") != "UNSAT" or not r.get("proof_verified"):
            continue
        rows.append({
            "cube_id": tag, "assumptions": r["units"], "depth": len(r["units"]),
            "cuber": CUBER, "p": p, "k": k,
            "encoder_path": "gen_cnf.py", "encoder_sha256": enc_sha,
            "base_cnf_sha256": base_sha, "cnf_sha256": r["cnf_sha256"],
            "solver": "kissat", "solver_returncode": 20, "verdict": "UNSAT",
            "solve_seconds": r["solve_s"],
            "drat_sha256": r["drat_sha256"], "drat_bytes": r.get("drat_bytes"),
            "drat_trim_verified": r.get("drat_trim") == "VERIFIED",
            "cake_lpr_verified": r.get("cake_lpr") == "VERIFIED",
            "verify_seconds": r["verify_s"],
            "proof_retained": bool(r.get("lrat_path")),
        })
    with open(os.path.join(out_dir, "results.jsonl"), "w") as f:
        for o in rows:
            f.write(json.dumps(o) + "\n")
    summary = {
        "p": p, "k": k, "cubes_recorded": len(rows),
        "verdicts": dict(collections.Counter(o["verdict"] for o in rows)),
        "drat_trim_verified": sum(o["drat_trim_verified"] for o in rows),
        "cake_lpr_verified": sum(o["cake_lpr_verified"] for o in rows),
        "encoder_sha256": enc_sha, "base_cnf_sha256": base_sha,
        "solve_cpu_hours": round(sum(o["solve_seconds"] for o in rows) / 3600, 2),
        "verify_cpu_hours": round(sum(o["verify_seconds"] for o in rows) / 3600, 2),
    }
    json.dump(summary, open(os.path.join(out_dir, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
