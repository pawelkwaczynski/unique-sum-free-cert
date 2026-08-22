#!/usr/bin/env python3
"""Cube naming and CNF serialization shared by the certifier and the auditor.

A cube fixes the smallest elements of A after the normalization 0, 1 in A.
Tag "c7_d9_e12" means: 7 is the third element, 9 the fourth, 12 the fifth,
and every residue strictly between consecutive fixed elements is excluded.
Membership of residue i lives on variable i+1 (same convention as gen_cnf).

The order of the unit clauses matters: the ledger binds each proof to the
sha256 of the CNF file bytes, so the reconstruction here must emit the units
in exactly the order the certifier wrote them.
"""
import hashlib


def parent_units(p, c, d):
    units = [c + 1, d + 1]
    units += [-(j + 1) for j in range(2, c)]
    units += [-(j + 1) for j in range(c + 1, d)]
    return units


def child_units(p, c, d, e):
    return parent_units(p, c, d) + [e + 1] + [-(j + 1) for j in range(d + 1, e)]


def tag_units(p, tag):
    """Unit clauses for a tag of any depth (c7, c7_d9, c7_d9_e12, ...)."""
    if tag == "whole":
        return []
    v = [int(part[1:]) for part in tag.split("_")]
    if len(v) == 1:                      # coarse cube "cN"
        return [v[0] + 1] + [-(j + 1) for j in range(2, v[0])]
    units = [v[0] + 1, v[1] + 1]
    units += [-(j + 1) for j in range(2, v[0])]
    units += [-(j + 1) for j in range(v[0] + 1, v[1])]
    for i in range(2, len(v)):
        units.append(v[i] + 1)
        units += [-(j + 1) for j in range(v[i - 1] + 1, v[i])]
    return units


def children_tags(p, tag):
    """Tags of the children: next element from (last+1) to p-1. Empty list
    means the cube cannot be split further."""
    parts = tag.split("_")
    last = int(parts[-1][1:])
    letters = "cdefghijklmnopqrstuvwxyz"
    if len(parts) >= len(letters):
        return []
    letter = letters[len(parts)]
    return [f"{tag}_{letter}{v}" for v in range(last + 1, p)]


def serialize_cnf(nvars, clauses, extra_units):
    """DIMACS bytes exactly as the certifier writes them. Duplicate literals in
    a clause are removed: drat-trim drops them internally and its LRAT output
    would otherwise disagree with the file cake_lpr reads."""
    out = [f"p cnf {nvars} {len(clauses) + len(extra_units)}\n"]
    for c in clauses:
        out.append(" ".join(map(str, dict.fromkeys(c))) + " 0\n")
    for u in extra_units:
        out.append(f"{u} 0\n")
    return "".join(out).encode()


def cnf_sha256(nvars, clauses, extra_units):
    return hashlib.sha256(serialize_cnf(nvars, clauses, extra_units)).hexdigest()
