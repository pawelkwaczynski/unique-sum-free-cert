# Encoding tests

`diff_test.py` compares `gen_cnf.py` with an independently written encoder of
the same question (Mark Watson's pinned `usf_encode_pinned.py`, sha256
`2eeec8ec926f80ee0d9db55a4f396acc3fe92110cc9bfc78908260a53b1c9003`, from his
p = 59 certification pipeline). That encoder is his and is not redistributed
here; the test expects a copy next to the script.

Result (2026-08-22, kissat 4.0.4): 68 instances, p in {7, 11, 13, 17, 19, 23,
29, 31}, k from 2 to m(p)+1. Zero verdict mismatches between the encoders, and
every verdict agrees with the known value of m(p) (Scheinerman 2019, Table
3.1). See `results.txt` and `results.json`.

Tested, not proved: agreement at p <= 31 does not prove that either encoding is
faithful at p = 67. It does rule out a shared misreading of the definition,
since the two encoders were written independently and differ in structure
(this one adds a sumset bound and a reflection symmetry breaker; the other does
not).

## Per-cube replay

`replay_cubes.py` takes a seeded random sample of our certified p = 53, k = 13
cubes, applies their unit clauses to the other encoder's CNF (same variable
convention) and solves with kissat. Result (2026-08-23, seed 2026): 300 of 300
cubes UNSAT on the other encoder, zero mismatches (`replay_p53k13.json`). This
checks that the two encodings agree not only on whole instances but on every
sampled sub-instance of the partition actually used for the certificates.

## Property tests (no second encoder needed)

`property_tests.py` checks two things a differential test near m(p) never
reaches: that the whole group Z/pZ (which is trivially unique-sum-free) is
accepted at k = p, and that the reflection symmetry breaker never changes a
verdict (p <= 23, every k). The first test is what exposed the lex-leader
defect fixed on 2026-08-23: the chain clause was `[-eq, -eq_prev]` instead
of `[-eq, eq_prev]`, which excluded every assignment whose first two orbit
pairs are equal. Certificates produced before the fix prove unsatisfiability
of that over-constrained formula; they are being re-issued against the fixed
encoder, with new base and per-cube hashes. The values were never in doubt
(independent search engine, independent encoder, per-cube replay), the
proof objects were.
