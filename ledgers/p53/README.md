# p = 53, m(53) = 14

Every k from 2 to 13 refuted; each rung audited by `audit_coverage.py` (UNSAT-CERTIFIED). k <= 4 are whole-formula certificates, k >= 5 are cube partitions.

Re-issued 2026-08-23 against the fixed encoder (see `encoding-tests/README.md`); the first issue, produced with the over-constrained symmetry breaker, is kept in `superseded/` for the record and must not be cited as a certificate.

| k | cube rows | solve CPU-h | verify CPU-h | base CNF sha256 (prefix) |
|---|---|---|---|---|
| 2 | 1 | 0.0 | 0.0 | e244f0ca836e |
| 3 | 1 | 0.0 | 0.0 | f39e8ecd68c6 |
| 4 | 1 | 0.0 | 0.0 | 09f9dc78d1a5 |
| 5 | 1275 | 0.01 | 0.09 | 6a6165e9db2e |
| 6 | 1275 | 0.01 | 0.19 | 12ae6a525500 |
| 7 | 1275 | 0.01 | 0.19 | 7a82cacd1e14 |
| 8 | 1275 | 0.01 | 0.09 | cdcf7a31c2f7 |
| 9 | 1275 | 0.01 | 0.09 | 78840d3cd838 |
| 10 | 1275 | 0.02 | 0.12 | e0b4d18b1399 |
| 11 | 1275 | 0.13 | 0.28 | 1c62ed6e8cfc |
| 12 | 1275 | 1.15 | 2.27 | 54698777bc55 |
| 13 | 2865 | 11.4 | 24.59 | 049c1b341ba0 |

Total: 12.75 CPU-h solving, 27.91 CPU-h checking (laptop, 6 cores at 70 percent). Proofs checked at generation and not retained (solver-certified, hash-bound).
