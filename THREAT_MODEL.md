# Threat model: ways this repository could be wrong, and what catches each

| # | Failure | Caught by | Status |
|---|---|---|---|
| 1 | Encoder does not encode the definition (wrong clause, wrong sign) | property tests (whole group SAT at k = p; breaker-free equivalence), differential test vs an independent encoder, per-cube replay | happened once (lex-leader sign, 2026-08-23), caught by the whole-group test; all certificates re-issued |
| 2 | A proof is paired with the wrong CNF | ledger rows carry `cnf_sha256`; `audit_coverage.py` rebuilds every CNF from `gen_cnf.py` plus the cube's units and refuses a mismatch | covered |
| 3 | Cubes overlap or leave a gap | `cover_cert.py` refutes "no cube" as a checked certificate; `check_cover.py` binds it to the cubes actually used; `audit_coverage.py` applies Proposition 2 | covered |
| 4 | A split cube is closed although a child is missing | coverage audit requires every child closed; an empty child list never closes a cube | covered |
| 5 | A row claims UNSAT but the checker failed (for example OOM in drat-trim) | audit accepts only rows with `drat_trim = VERIFIED`, `cake_lpr = VERIFIED`, both return codes 0; loop alarm on UNSAT without verification | happened on the cloud workers (2026-08-18), rows removed and recomputed |
| 6 | The checker binary is substituted or missing | `verify_drat.sh` requires the status line, not only exit 0; tools pinned by commit in `tools/README.md` | partial: no fake-checker negative test in CI yet |
| 7 | Witness parse or definition error | `check_witness.py` recomputes representation counts from scratch | covered |
| 8 | Ledger edited by hand | CI re-audits every ledger on every push; cover and export summaries recomputed | covered |
| 9 | Symmetry reduction unsound (normalization, reflection) | hand proof for normalization; breaker soundness tested for p <= 23; breaker-free run possible at any time | covered by tests, not by proof at large p |
| 10 | Solver bug producing a wrong proof | proof replayed by drat-trim and by the formally verified cake_lpr | covered |
| 11 | The exact value is right but the claim overreaches (k below m(p) never refuted) | full ladders k = 2..m(p)-1 per prime; VERIFICATION_MAP tiers | p = 53 complete; others queued |

Trusted surfaces that remain: `gen_cnf.py` and `cubes.py` (tested, not proved), `audit_coverage.py` and `check_cover.py` (plain Python, readable in an hour), drat-trim and cake_lpr, and the hand proofs of normalization and of Proposition 2 (the latter now also certified).
