# p = 53, m(53) = 14

Every k from 2 to 13 refuted; each rung audited by `audit_coverage.py` (UNSAT-CERTIFIED). k <= 4 are whole-formula certificates, k >= 5 are cube partitions.

| k | cube rows | solve CPU-h | verify CPU-h |
|---|---|---|---|
| 2 | 1 | 0.0 | 0.0 |
| 3 | 1 | 0.0 | 0.0 |
| 4 | 1 | 0.0 | 0.0 |
| 5 | 1275 | 0.01 | 0.18 |
| 6 | 1275 | 0.01 | 0.27 |
| 7 | 1275 | 0.01 | 0.18 |
| 8 | 1275 | 0.02 | 0.18 |
| 9 | 1275 | 0.02 | 0.21 |
| 10 | 1275 | 0.04 | 0.21 |
| 11 | 1275 | 0.13 | 0.36 |
| 12 | 1275 | 1.32 | 2.09 |
| 13 | 6020 | 1.49 | 2.86 |

Total: 3.05 CPU-h solving, 6.54 CPU-h checking. Proofs for these rungs were checked at generation and not retained (solver-certified, hash-bound).
