# p = 59, m(59) = 15

Every k from 2 to 14 refuted; each rung audited by `audit_coverage.py` (UNSAT-CERTIFIED) and,
for k >= 4, the cube partition certified by `cover_cert.py` and checked by `check_cover.py`.
k = 2 and k = 3 are whole-formula certificates, k >= 4 are position-cube partitions
(1,596 top-level cubes; the timed-out cubes of k = 13 and k = 14 were split into children
until every leaf was refuted).

Proof chain: CaDiCaL with native LRAT output, every proof checked by the verified checker
cake_lpr at generation time (`chain = cadical-lrat-cake_lpr`, `lrat_sha256` retained,
drat-trim skipped). Computed 2026-08-30 and 2026-08-31 on cloud workers (e2-standard-8,
six solver processes each), re-audited on the author's machine on 2026-09-08 before
publication. Watson replayed the 1,596 top-level cubes of k = 14 through his own encoder
and solver chain on 2026-08-25 (see the main README).

| k | ledger rows | certificate (last row per cube counts) | solve CPU-h | verify CPU-h | base CNF sha256 (prefix) |
|---|---|---|---|---|---|
| 2 | 1597 | whole formula (one whole-formula row; the 1,596 earlier cube rows are kept, the audit uses the whole-formula row) | 0.01 | 0.07 | d14daa60ccdd |
| 3 | 1597 | whole formula (as for k = 2) | 0.02 | 0.07 | b646fe442715 |
| 4 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.02 | 0.07 | 2d669e8228c9 |
| 5 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.02 | 0.07 | 8fbab8c6d74f |
| 6 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.02 | 0.07 | 15e49900352f |
| 7 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.02 | 0.07 | 764f87ebc3fa |
| 8 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.02 | 0.08 | 04bb73a38ccd |
| 9 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.02 | 0.08 | 8c716ae5ce00 |
| 10 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.05 | 0.09 | f95c7c92ae56 |
| 11 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.31 | 0.21 | 8d9c65f46ed9 |
| 12 | 1596 | 1596 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 1.63 | 0.54 | aaabdf3fc5c3 |
| 13 | 2871 | 2845 cubes UNSAT, 26 timed-out attempts (split into children), 27 cover certificates | 21.41 | 3.39 | da3aeb747a2d |
| 14 | 8067 | 7855 cubes UNSAT, 209 timed-out attempts (split into children), 134 cover certificates | 128.30 | 17.67 | 3950e2e74166 |

Total: 28,496 ledger rows, 151.8 CPU-h solving (timed-out attempts included),
22.5 CPU-h checking. Proofs checked at generation and not retained (solver-certified,
hash-bound); the per-cube `lrat_sha256` and `cnf_sha256` are in `certified.jsonl`.
`watson-format/` holds the same rows in the layout of unique-sums-notes.
