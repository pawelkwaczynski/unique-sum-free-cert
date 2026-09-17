# p = 71, m(71) = 16

Every k from 2 to 15 refuted; each rung audited by `audit_coverage.py` (UNSAT-CERTIFIED) and,
for k >= 4, the cube partition certified by `cover_cert.py` and checked by `check_cover.py`.
k = 2 and k = 3 are whole-formula certificates, k >= 4 are position-cube partitions
(2,346 top-level cubes; timed-out cubes were split into children, and children into
grandchildren where needed, until every leaf was refuted).

k = 14 was computed between 2026-08-24 and 2026-08-30 on cloud workers (Google Cloud
e2-standard-8; the early rows use kissat with DRAT checked by drat-trim and cake_lpr, the rest
CaDiCaL native LRAT checked by cake_lpr) and audited on 2026-09-08. k = 15 was started on
2026-09-08 on the same kind of workers and finished on 2026-09-16 and 2026-09-17 on the EuroHPC
supercomputer LUMI-C in four rounds of splitting the timed-out cubes (8 nodes of 128 solver
processes per round). k = 2..13 were computed on 2026-09-17 on LUMI-C (one node). The k = 15
ledger is stored as `certified.jsonl.gz` (sha256 of the uncompressed file in `RAW_SHA256`) and its
`watson-format/results.jsonl` is gzip-compressed as well; every tool here reads both forms.
Every rung was re-audited on the author's machine on 2026-09-17 from the copy in this directory
before publication.

| k | ledger rows | certificate (last row per cube counts) | solve CPU-h | verify CPU-h | base CNF sha256 (prefix) |
|---|---|---|---|---|---|
| 2 | 1 | whole formula | 0.00 | 0.00 | 44ad12a98bab |
| 3 | 1 | whole formula | 0.00 | 0.00 | afea6583e313 |
| 4 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.50 | 0.52 | 3133ddc7a7ba |
| 5 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.68 | 0.69 | ffac460f52df |
| 6 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.68 | 0.69 | 0ab859664073 |
| 7 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.69 | 0.71 | c97dea5640e3 |
| 8 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.69 | 0.70 | 678216a3530b |
| 9 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.38 | 0.40 | f1ed96ca7ced |
| 10 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.74 | 0.71 | 3ea901ec8186 |
| 11 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 1.04 | 0.72 | 4df7bacea96e |
| 12 | 2346 | 2346 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 3.43 | 0.89 | 5042b458279e |
| 13 | 4850 | 4808 cubes UNSAT, 42 timed-out attempts (split into children), 43 cover certificates | 36.02 | 4.38 | 96fe8444516c |
| 14 | 33616 | 32704 cubes UNSAT, 912 timed-out attempts (split into children), 540 cover certificates | 505.77 | 293.76 | f2f7ee5e17c5 |
| 15 | 382461 | 374981 cubes UNSAT, 7465 timed-out attempts (split into children), 7301 cover certificates | 4767.06 | 687.21 | 875e0349e90a |

Total: 442,043 ledger rows, 5317.7 CPU-h solving (timed-out attempts included), 991.4 CPU-h checking; ledgers 196 MB on disk.
Proofs checked at generation and not retained (solver-certified, hash-bound); the per-cube
`cnf_sha256` and the proof hash (`lrat_sha256` for the native chain, `drat_sha256` otherwise)
are in `certified.jsonl` (`certified.jsonl.gz` for k = 15). `watson-format/` holds the same rows in the layout of
unique-sums-notes.
