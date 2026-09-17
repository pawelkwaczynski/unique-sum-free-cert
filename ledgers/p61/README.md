# p = 61, m(61) = 15

Every k from 2 to 14 refuted; each rung audited by `audit_coverage.py` (UNSAT-CERTIFIED) and,
for k >= 4, the cube partition certified by `cover_cert.py` and checked by `check_cover.py`.
k = 2 and k = 3 are whole-formula certificates, k >= 4 are position-cube partitions
(1,711 top-level cubes; timed-out cubes were split into children, and children into
grandchildren where needed, until every leaf was refuted).

k = 14 was computed on 2026-09-02 on cloud workers (Google Cloud e2-standard-8, six solver
processes each; the early rows use kissat with DRAT checked by drat-trim and cake_lpr, the rest
CaDiCaL native LRAT checked by cake_lpr) and audited on 2026-09-08. k = 2..13 were computed on
2026-09-17 on the EuroHPC supercomputer LUMI-C (one node, 128 solver processes, CaDiCaL native
LRAT, every proof checked by cake_lpr at generation).
Every rung was re-audited on the author's machine on 2026-09-17 from the copy in this directory
before publication.

| k | ledger rows | certificate (last row per cube counts) | solve CPU-h | verify CPU-h | base CNF sha256 (prefix) |
|---|---|---|---|---|---|
| 2 | 1 | whole formula | 0.00 | 0.00 | 19ffe3ab8059 |
| 3 | 1 | whole formula | 0.00 | 0.00 | dc15a710965a |
| 4 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.36 | 0.38 | b3b858573bbb |
| 5 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.35 | 0.37 | e0a4d3c0304a |
| 6 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.23 | 0.25 | 6bec98e85f52 |
| 7 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.37 | 0.38 | 264ed252ce72 |
| 8 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.38 | 0.39 | 37c582e9cfed |
| 9 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.25 | 0.27 | de6a9304bf16 |
| 10 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.39 | 0.38 | 0f21127f6f92 |
| 11 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.54 | 0.40 | c5392fdff262 |
| 12 | 1711 | 1711 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 1.69 | 0.48 | ebc5ad6af37c |
| 13 | 2333 | 2321 cubes UNSAT, 12 timed-out attempts (split into children), 13 cover certificates | 16.57 | 2.11 | c9f0ff1af4c9 |
| 14 | 25354 | 24367 cubes UNSAT, 987 timed-out attempts (split into children), 476 cover certificates | 468.71 | 142.31 | 1701acefef6f |

Total: 43,088 ledger rows, 489.8 CPU-h solving (timed-out attempts included), 147.7 CPU-h checking; ledgers 73 MB on disk.
Proofs checked at generation and not retained (solver-certified, hash-bound); the per-cube
`cnf_sha256` and the proof hash (`lrat_sha256` for the native chain, `drat_sha256` otherwise)
are in `certified.jsonl`. `watson-format/` holds the same rows in the layout of
unique-sums-notes.
