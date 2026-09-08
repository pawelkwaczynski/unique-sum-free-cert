# Verification map

One row per claim the README makes, with the file that carries it and the tier it sits at. Tiers: **checked certificate** (proof object replayed by cake_lpr, via drat-trim for DRAT proofs or directly for CaDiCaL native LRAT, hash-bound to a reconstructible CNF, coverage audited, cover certificate present), **search only** (two independent search programs agree, witness checked, no proof object), **external** (someone else's result, cited), **queued** (not started).

| Claim | Tier | Evidence | Status history |
|---|---|---|---|
| m(53) = 14, upper bound | checked witness | `witnesses/witnesses.json`, `check_witness.py` | 2026-08-22 published |
| m(53) >= 14, every k = 2..13 refuted | checked certificate | `ledgers/p53/k*/certified.jsonl`, `cover.jsonl`, `audit_coverage.py`, `check_cover.py` | 2026-08-22 first issue (over-constrained breaker, now `superseded/`); 2026-08-23 re-issued against the fixed encoder, cover certificates added |
| m(59) = 15, upper bound | checked witness | `witnesses/witnesses.json`, `check_witness.py` | published; the same set as Scheinerman's |
| m(59) >= 15, every k = 2..14 refuted | checked certificate | `ledgers/p59/k*/certified.jsonl`, `cover.jsonl`, `audit_coverage.py`, `check_cover.py`; independent retained LRAT by Watson (unique-sums-notes) | 2026-08-30 and 08-31 computed on cloud workers (CaDiCaL native LRAT checked by cake_lpr at generation, hashes retained); 2026-09-08 every rung re-audited on the author's machine, cover certificates added, published |
| m(61) = 15 | search only | witness; two engines | k = 14 refuted 2026-09-02 (ledger audited, not yet in this repository); k = 2..13 queued |
| m(67) = 16 | search only | witness; two engines | k = 15 refuted 2026-09-02 (ledger audited, not yet in this repository); k = 2..14 queued |
| m(71) = 16 | search only | witness; two engines | k = 14 refuted 2026-08-30 (ledger audited, not yet in this repository); k = 15 running (2026-09-08) |
| m(73) = 16 | search only | witness; two engines | k = 15 running (2026-09-08) |
| Values m(53), m(59) tabulated earlier without proof | external | Scheinerman 2019, Table 3.1 | cited |
| Encoder agrees with an independent encoder | tested (p <= 31; 300 cubes) | `encoding-tests/` | 2026-08-22 |
| Whole group accepted at k = p; breaker never changes a verdict | tested (p <= 23) | `encoding-tests/property_tests.py`, CI | 2026-08-23 |
| Cube partition is complete | checked certificate | `cover.jsonl` per rung, `check_cover.py` | 2026-08-23 |
| Normalization 0, 1 in A is sound | hand proof | README, paper | |

"Search only" rows are not certificates and must not be cited as such.
