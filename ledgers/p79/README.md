# p = 79, m(79) = 17

Every k from 2 to 16 refuted; each rung audited by `audit_coverage.py` (UNSAT-CERTIFIED) and,
for k >= 4, the cube partition certified by `cover_cert.py` and checked by `check_cover.py`.
k = 2 and k = 3 are whole-formula certificates, k >= 4 are position-cube partitions
(2,926 top-level cubes; timed-out cubes were split into children, and children into
grandchildren where needed, until every leaf was refuted).

k = 2..15 were computed between 2026-09-17 and 2026-09-20 on the EuroHPC supercomputer LUMI-C
(one node, 128 solver processes, CaDiCaL native LRAT, every proof checked by cake_lpr at
generation). k = 16 was computed between 2026-09-24 and 2026-10-09 on LUMI-C in 24 iterations of a
self-resubmitting one-node job; the cubes that timed out in one iteration were split into children
for the next, and the coverage audit passed after the 24th. The k = 15 ledger is stored as `certified.jsonl.gz`
(sha256 of the uncompressed file in `RAW_SHA256`) and its `watson-format/results.jsonl` is
gzip-compressed as well. The k = 16 ledger (2,468,318 rows) is over the GitHub file limit: it is
deposited in the Zenodo record of v0.4, `k16/EXTERNAL_LEDGER` gives its URL and sha256, and
`fetch_external.sh` downloads it and refuses it if the hash differs. Every rung was re-audited
before publication from this directory layout with the repository scripts, on LUMI-C (2026-10-13).

| k | ledger rows | certificate (last row per cube counts) | solve CPU-h | verify CPU-h | base CNF sha256 (prefix) |
|---|---|---|---|---|---|
| 2 | 1 | whole formula | 0.00 | 0.00 | 7520a9c44862 |
| 3 | 1 | whole formula | 0.00 | 0.00 | abcf2be30a17 |
| 4 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.80 | 0.84 | 083f626faa75 |
| 5 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.58 | 0.62 | 709236456c8d |
| 6 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 1.03 | 1.05 | af62bccb1b5d |
| 7 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 1.03 | 1.05 | dc50286899eb |
| 8 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 1.04 | 1.05 | 38f6176cc048 |
| 9 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.66 | 0.68 | 89955ad43f4b |
| 10 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 0.73 | 0.69 | f9bac33ca047 |
| 11 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 1.63 | 1.06 | ff762b07c964 |
| 12 | 2926 | 2926 cubes UNSAT, 0 timed-out attempts (split into children), 1 cover certificates | 5.90 | 1.39 | 5b647a183aae |
| 13 | 7934 | 7858 cubes UNSAT, 76 timed-out attempts (split into children), 77 cover certificates | 59.92 | 7.37 | 0dbceb108b0b |
| 14 | 49315 | 48566 cubes UNSAT, 749 timed-out attempts (split into children), 750 cover certificates | 543.87 | 63.28 | 39a4b8c51151 |
| 15 | 577215 | 567209 cubes UNSAT, 10006 timed-out attempts (split into children), 10007 cover certificates | 7136.44 | 841.75 | 2eb1b706c154 |
| 16 | 2468318 | 2424701 cubes UNSAT, 43617 timed-out attempts (split into children), 43618 cover certificates | 30226.93 | 4213.99 | 06982acd1ce2 |

Total: 3,129,118 ledger rows, 37980.6 CPU-h solving (timed-out attempts included), 5134.8 CPU-h checking; ledgers 638 MB on disk, of which the k = 16 ledger (320 MB compressed) is in the Zenodo record.
Proofs checked at generation and not retained (solver-certified, hash-bound); the per-cube
`cnf_sha256` and the proof hash (`lrat_sha256` for the native chain) are in `certified.jsonl`
(`certified.jsonl.gz` for k = 15 and, from Zenodo, k = 16). `watson-format/` holds the same rows
in the layout of unique-sums-notes (for k = 16 only `summary.json`).
