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
