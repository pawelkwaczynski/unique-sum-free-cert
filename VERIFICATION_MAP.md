# Verification map

One row per claim the README makes, with the file that carries it and the tier it sits at. Tiers: **checked certificate** (proof object replayed by drat-trim and cake_lpr, hash-bound to a reconstructible CNF, coverage audited, cover certificate present), **search only** (two independent search programs agree, witness checked, no proof object), **external** (someone else's result, cited), **queued** (not started).

| Claim | Tier | Evidence | Status history |
|---|---|---|---|
| m(53) = 14, upper bound | checked witness | `witnesses/witnesses.json`, `check_witness.py` | 2026-08-22 published |
| m(53) >= 14, every k = 2..13 refuted | checked certificate | `ledgers/p53/k*/certified.jsonl`, `cover.jsonl`, `audit_coverage.py`, `check_cover.py` | 2026-08-22 first issue (over-constrained breaker, now `superseded/`); 2026-08-23 re-issued against the fixed encoder, cover certificates added |
| m(59) = 15 | search only here; external certificate | witness in `witnesses/`; retained LRAT by Watson (unique-sums-notes) | queued for this repository |
| m(61) = 15 | search only | witness; two engines | k = 14 running (2026-08-23) |
| m(67) = 16 | search only | witness; two engines | k = 15 running |
| m(71) = 16 | search only | witness; two engines | k = 15 and k = 14 running |
| m(73) = 16 | search only | witness; two engines | k = 15 running |
| Values m(53), m(59) tabulated earlier without proof | external | Scheinerman 2019, Table 3.1 | cited |
| Encoder agrees with an independent encoder | tested (p <= 31; 300 cubes) | `encoding-tests/` | 2026-08-22 |
| Whole group accepted at k = p; breaker never changes a verdict | tested (p <= 23) | `encoding-tests/property_tests.py`, CI | 2026-08-23 |
| Cube partition is complete | checked certificate | `cover.jsonl` per rung, `check_cover.py` | 2026-08-23 |
| Normalization 0, 1 in A is sound | hand proof | README, paper | |

"Search only" rows are not certificates and must not be cited as such.
