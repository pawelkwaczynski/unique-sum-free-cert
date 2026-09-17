# p = 73, m(73) = 16

Every k from 2 to 15 refuted; each rung audited by `audit_coverage.py` (UNSAT-CERTIFIED) and,
for k >= 4, the cube partition certified by `cover_cert.py` and checked by `check_cover.py`.
k = 2 and k = 3 are whole-formula certificates, k >= 4 are position-cube partitions
(2,485 top-level cubes; timed-out cubes were split into children, and children into
grandchildren where needed, until every leaf was refuted).

k = 15 was started on 2026-09-08 on cloud workers (Google Cloud e2-standard-8; the early
rows use kissat with DRAT checked by drat-trim and cake_lpr, the rest CaDiCaL native LRAT checked
by cake_lpr) and finished on 2026-09-16 and 2026-09-17 on the EuroHPC supercomputer LUMI-C in four
rounds of splitting the timed-out cubes (12 nodes of 128 solver processes per round). k = 2..14
were computed on 2026-09-17 on LUMI-C (one node). The k = 15 ledger is stored as
`certified.jsonl.gz` (sha256 of the uncompressed file in `RAW_SHA256`) and its
`watson-format/results.jsonl` is gzip-compressed as well; every tool here reads both forms.
Every rung was re-audited on the author's machine on 2026-09-17 from the copy in this directory
before publication.

| k | ledger rows | certificate (last row per cube counts) | solve CPU-h | verify CPU-h | base CNF sha256 (prefix) |
|---|---|---|---|---|---|
| 2 | 1 | whole formula | 0.00 | 0.00 | c63885b3cb46 |
| 3 | 1 | whole formula | 0.00 | 0.00 | d4968cfe8b03 |
| 4 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.75 | 0.76 | 2ecf013147a3 |
| 5 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.73 | 0.76 | 756329c8c1ab |
| 6 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.74 | 0.75 | ca7898a72068 |
| 7 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.76 | 0.76 | 27be146dea65 |
| 8 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.61 | 0.64 | 8f90436601b8 |
| 9 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.78 | 0.79 | 4aec23c60668 |
| 10 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.82 | 0.79 | a1e071c26f94 |
| 11 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 1.06 | 0.70 | 25c4242b7463 |
| 12 | 2485 | 2485 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 3.92 | 1.00 | ef27f4824463 |
| 13 | 5247 | 5202 cubes UNSAT, 45 timed-out attempts (split into children), 46 cover certificates | 40.22 | 4.87 | aa0091d4e24d |
| 14 | 35440 | 34863 cubes UNSAT, 577 timed-out attempts (split into children), 578 cover certificates | 400.35 | 50.77 | c6c269ab8357 |
| 15 | 519478 | 509561 cubes UNSAT, 9909 timed-out attempts (split into children), 9778 cover certificates | 6257.25 | 908.16 | 2e4373143b64 |

Total: 582,532 ledger rows, 6708.0 CPU-h solving (timed-out attempts included), 970.8 CPU-h checking; ledgers 236 MB on disk.
Proofs checked at generation and not retained (solver-certified, hash-bound); the per-cube
`cnf_sha256` and the proof hash (`lrat_sha256` for the native chain, `drat_sha256` otherwise)
are in `certified.jsonl` (`certified.jsonl.gz` for k = 15). `watson-format/` holds the same rows in the layout of
unique-sums-notes.
