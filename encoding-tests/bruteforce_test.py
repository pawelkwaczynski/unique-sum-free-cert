#!/usr/bin/env python3
"""Independently compare small unique-sum-free sets with the production CNF.

Run from the repository root. The combinatorial search does not call the
encoder or a SAT solver. SAT is used only for the comparison phase.
"""

import argparse
import importlib
import itertools
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)


def encoder():
    """Load the production encoder only for the comparison phase.

    The brute-force search below never sees this module, not even through an
    import at the top of the file. gen_cnf puts membership of residue i on
    variable i + 1 (gen_cnf.py, ``x = list(range(1, p + 1))``)."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    return importlib.import_module("gen_cnf")


def unique_sum_free(members, p):
    """True when no residue has exactly one unordered representation a + b.

    Pairs are unordered and include the diagonal a + a. The members must be
    distinct residues of Z/pZ; anything else is a caller error, not a set."""
    if len(set(members)) != len(members) or any(not 0 <= a < p for a in members):
        raise ValueError(f"not a set of residues mod {p}: {members}")
    counts = [0] * p
    for offset, a in enumerate(members):
        for b in members[offset:]:
            counts[(a + b) % p] += 1
    return 1 not in counts


def reflection_canonical(members, p):
    bits = set(members)
    return tuple(int(r in bits) for r in range(2, p)) <= tuple(
        int((1 - r) % p in bits) for r in range(2, p)
    )


def brute_force(p, k):
    """Return unrestricted, 0/1 normalized, and reflection reduced counts."""
    raw = normalized = reflected = 0
    for members in itertools.combinations(range(p), k):
        if not unique_sum_free(members, p):
            continue
        raw += 1
        if k >= 2 and members[:2] == (0, 1):
            normalized += 1
            if reflection_canonical(members, p):
                reflected += 1
    return raw, normalized, reflected


def dimacs(nvars, clauses, path):
    with path.open("w") as out:
        out.write(f"p cnf {nvars} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")


def solve(nvars, clauses, membership_count, solver, count):
    """Count distinct projections on x[0:p], blocking only membership bits."""
    with tempfile.TemporaryDirectory(prefix="bruteforce_") as tmp:
        path = Path(tmp) / "audit.cnf"
        models = 0
        while True:
            dimacs(nvars, clauses, path)
            result = subprocess.run([solver, str(path)], capture_output=True,
                                    text=True, check=False)
            if result.returncode == 20:
                return (False if models == 0 else True), models if count else None
            if result.returncode != 10:
                raise RuntimeError(f"solver returned {result.returncode}: {result.stderr[-300:]}")
            if not count:
                return True, None
            values = {}
            for line in result.stdout.splitlines():
                if line.startswith("v "):
                    for token in line[2:].split():
                        literal = int(token)
                        if literal:
                            values[abs(literal)] = literal > 0
            if any(variable not in values for variable in range(1, membership_count + 1)):
                raise RuntimeError("solver did not print a complete membership assignment")
            clauses.append([(-variable if values[variable] else variable)
                            for variable in range(1, membership_count + 1)])
            models += 1


def audit_row(p, k, solver, count_models):
    raw, normalized, reflected = brute_force(p, k)
    nvars, clauses = encoder().build(p, k)
    sat, projected = solve(nvars, clauses, p, solver, count_models)
    if sat != (reflected > 0) or sat != (raw > 0) or (
            projected is not None and projected != reflected):
        raise AssertionError((p, k, raw, normalized, reflected, sat, projected))
    if (raw > 0) != (normalized > 0) or (normalized > 0) != (reflected > 0):
        raise AssertionError(f"normalization or reflection changed existence at p={p}, k={k}")
    return {"p": p, "k": k, "raw": raw, "normalized_01": normalized,
            "reflection_reduced": reflected, "sat": sat,
            "cnf_projected": projected}


def negative_control(solver):
    """Delete the entire no-singleton clause family, then require detection."""
    p, k = 5, 2
    # Disable the implied sumset bound here: it independently rejects k=2,
    # and would mask the deliberately deleted no-singleton clauses.
    nvars, clauses = encoder().build(p, k, sumset_bound=False)
    intact_sat, _ = solve(nvars, list(clauses), p, solver, False)
    if intact_sat:
        raise AssertionError("negative control: the intact CNF is already SAT")
    first_pair = p + 1
    last_pair = p + p * (p + 1) // 2
    broken = [c for c in clauses if not (
        len(c) > 1 and -last_pair <= c[0] <= -first_pair
        and all(first_pair <= v <= last_pair for v in c[1:])
    )]
    assert len(broken) < len(clauses), "mutation did not remove any clause"
    sat, _ = solve(nvars, broken, p, solver, False)
    raw, _, _ = brute_force(p, k)
    if sat == (raw > 0):
        raise AssertionError("negative control was not detected")
    return {"p": p, "k": k, "clauses_before": len(clauses),
            "removed_clauses": len(clauses) - len(broken), "brute_existence": raw > 0,
            "intact_cnf_sat": intact_sat, "broken_cnf_sat": sat}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", default="kissat")
    parser.add_argument("--prime", type=int, choices=PRIMES)
    parser.add_argument("--count-max-p", type=int, default=11)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    primes = (args.prime,) if args.prime else PRIMES
    rows = []
    for p in primes:
        for k in range(1, p + 1):
            row = audit_row(p, k, args.solver, p <= args.count_max_p)
            rows.append(row)
            print(json.dumps(row), flush=True)
    result = {"rows": rows, "negative_control": negative_control(args.solver)}
    print(json.dumps({"negative_control": result["negative_control"]}), flush=True)
    if args.out:
        args.out.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
