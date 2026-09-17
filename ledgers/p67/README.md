# p = 67, m(67) = 16

Every k from 2 to 15 refuted; each rung audited by `audit_coverage.py` (UNSAT-CERTIFIED) and,
for k >= 4, the cube partition certified by `cover_cert.py` and checked by `check_cover.py`.
k = 2 and k = 3 are whole-formula certificates, k >= 4 are position-cube partitions
(2,080 top-level cubes; timed-out cubes were split into children, and children into
grandchildren where needed, until every leaf was refuted).

k = 15 was computed between 2026-08-28 and 2026-09-02 on cloud workers (Google Cloud
e2-standard-8, six solver processes each; the early rows use kissat with DRAT checked by drat-trim
and cake_lpr, the rest CaDiCaL native LRAT checked by cake_lpr) and audited on 2026-09-08.
k = 2..14 were computed on 2026-09-17 on the EuroHPC supercomputer LUMI-C (one node, 128 solver
processes, CaDiCaL native LRAT, every proof checked by cake_lpr at generation).
Every rung was re-audited on the author's machine on 2026-09-17 from the copy in this directory
before publication.

| k | ledger rows | certificate (last row per cube counts) | solve CPU-h | verify CPU-h | base CNF sha256 (prefix) |
|---|---|---|---|---|---|
| 2 | 1 | whole formula | 0.00 | 0.00 | 5abd44c7e1ab |
| 3 | 1 | whole formula | 0.00 | 0.00 | 1ff98723f8c0 |
| 4 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.52 | 0.54 | c39c275e4bab |
| 5 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.53 | 0.53 | ab9a9d0cd3ed |
| 6 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.55 | 0.55 | 1df10f554b56 |
| 7 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.54 | 0.55 | 5b777eb18cf5 |
| 8 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.54 | 0.56 | d154e280d4f5 |
| 9 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.55 | 0.56 | a1f430074ee4 |
| 10 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.59 | 0.57 | 5fd0d664718e |
| 11 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.66 | 0.44 | aa5af1c65963 |
| 12 | 2080 | 2080 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 2.62 | 0.70 | 3e04775c908c |
| 13 | 3827 | 3796 cubes UNSAT, 31 timed-out attempts (split into children), 32 cover certificates | 26.84 | 3.23 | 06027b75b187 |
| 14 | 26347 | 25882 cubes UNSAT, 465 timed-out attempts (split into children), 466 cover certificates | 309.13 | 34.83 | 0b0878a9d985 |
| 15 | 54785 | 52790 cubes UNSAT, 1995 timed-out attempts (split into children), 925 cover certificates | 1080.55 | 350.90 | 8bd5cc76e23e |

Total: 103,681 ledger rows, 1423.6 CPU-h solving (timed-out attempts included), 394.0 CPU-h checking; ledgers 130 MB on disk.
Proofs checked at generation and not retained (solver-certified, hash-bound); the per-cube
`cnf_sha256` and the proof hash (`lrat_sha256` for the native chain, `drat_sha256` otherwise)
are in `certified.jsonl`. `watson-format/` holds the same rows in the layout of
unique-sums-notes.
