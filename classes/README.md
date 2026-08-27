# Affine classes of minimum unique-sum-free sets

For each odd prime p with m(p) known (A398173), the number of subsets of Z/pZ of size m(p)
with no unique sum, counted up to the affine maps x -> a x + b (a != 0), one representative
per class, and a certificate that the list is complete.

| p  | m(p) | classes | evidence |
|----|------|---------|----------|
| 3  | 3  | 1  | three methods (B, brute force, SAT enumeration) |
| 5  | 4  | 1  | three methods |
| 7  | 5  | 1  | three methods |
| 11 | 7  | 4  | three methods; completeness certified |
| 13 | 7  | 1  | three methods; certified |
| 17 | 8  | 1  | three methods; certified |
| 19 | 9  | 9  | three methods; certified |
| 23 | 10 | 35 | three methods; certified |
| 29 | 11 | 30 | three methods; certified |
| 31 | 11 | 5  | three methods; certified |
| 37 | 12 | 13 | three methods; certified |
| 41 | 13 | 69 | engine B list; stabilizer count matches engine v1 (5,274); certificate by cubes in progress |
| 43 | 13 | 23 | engine B list; matches v1 (1,794); certificate in progress |
| 47 | 13 | 2  | engine B list; matches v1 (156); certificate in progress |
| 53 | 14 | 2  | engine B list; matches v1 (182); certificate queued |
| 59 | 15 | 12 | engine B list; v1 count running (predicted 1,260) |
| 61 | 15 | 3  | engine B list; v1 count queued (predicted 231) |

Sequence: 1, 1, 1, 4, 1, 1, 9, 35, 30, 5, 13, 69, 23, 2, 2, 12, 3 (not in the OEIS as of 2026-08-26).

## Methods

- `engine_b_counts.log`: `msearch2 p k --count` (orbit-canonical search, counts canonical
  representatives under AGL(1, p)); `list_p<p>k<k>.txt`: `msearch2 --list`, one line `W {...}`
  per class, the lexicographically least normalized image.
- `count_orbits_bruteforce.py`: brute force over all subsets with a canonical form computed
  from every affine map (p <= 31), also reports which sizes k admit a unique-sum-free set.
- `verify_classes.py`: for a list, checks every representative from the definition
  (unique-sum-free, canonical, pairwise distinct), computes stabilizers, and predicts the
  number of normalized witnesses N and of reflection-fixed ones F; the independent engine v1
  (`msearch --count`, which counts classes under the reflection only) must report (N + F) / 2.
  Agreement is a completeness check by counting; `engine_v1_reflection_classes.log`.
- `cert_classes.py`: completeness as a certificate (after Krug, arXiv:2607.23766, Prop. 15):
  the formula "0, 1 in A, |A| = k, no unique sum, A is not one of the normalized images of any
  listed class" is refuted by CaDiCaL with a native LRAT proof checked by cake_lpr. A model
  would be a set outside every listed class. `certificates_whole_formula.jsonl` holds one row
  per p with the sha256 of the CNF and of the LRAT proof; p = 11 to 37 are
  `LIST-COMPLETE-CERTIFIED`; p = 41 and 43 time out on the whole formula.
- `cert_classes_cubes.py`: the same certificate by cube-and-conquer over the position cubes
  (c, d) used for the m(p) certificates, for p >= 41.

The blocking clauses use the same variable convention as `gen_cnf.py` (membership of i on
variable i + 1) and the encoder without the reflection breaker, so the certificate does not
depend on the breaker. Paths in the scripts follow the cloud worker layout
(`/home/green27/...`); adjust `sys.path` and the tool paths to run elsewhere.
