# Affine classes of minimum unique-sum-free sets

For each odd prime p with m(p) known (A398173), the number of subsets of Z/pZ of size m(p)
with no unique sum, counted up to the affine maps x -> a x + b (a != 0), one representative
per class, and a certificate that the list is complete.

| p  | m(p) | classes | how the list was obtained | completeness |
|----|------|---------|---------------------------|--------------|
| 3  | 3  | 1  | engine B; brute force over all subsets | trivial (brute force) |
| 5  | 4  | 1  | engine B; brute force | trivial (brute force) |
| 7  | 5  | 1  | engine B; brute force | trivial (brute force) |
| 11 | 7  | 4  | engine B; brute force; SAT model enumeration | certified, whole formula |
| 13 | 7  | 1  | engine B; brute force | certified, whole formula |
| 17 | 8  | 1  | engine B; brute force | certified, whole formula |
| 19 | 9  | 9  | engine B; brute force; SAT model enumeration | certified, whole formula |
| 23 | 10 | 35 | engine B; brute force; SAT model enumeration | certified, whole formula |
| 29 | 11 | 30 | engine B; brute force; SAT model enumeration | certified, whole formula |
| 31 | 11 | 5  | engine B; brute force; SAT model enumeration | certified, whole formula |
| 37 | 12 | 13 | engine B; SAT model enumeration | certified, whole formula |
| 41 | 13 | 69 | engine B; v1 count agrees (5,274) | certified, 741 position cubes |
| 43 | 13 | 23 | engine B; v1 count agrees (1,794) | certified, 820 position cubes |
| 47 | 13 | 2  | engine B; v1 count agrees (156) | certified, 990 position cubes |
| 53 | 14 | 2  | engine B; v1 count agrees (182) | certified, 1,275 position cubes (1,227 directly, 48 through their children) |
| 59 | 15 | 12 | engine B list only | not certified |
| 61 | 15 | 3  | engine B list only | not certified |
| 67 | 16 | 24 | engine B list only | not certified |
| 71 | 16 | 2  | engine B list only | not certified |

The p = 53 certificate was finished on 2026-09-18. The 48 position cubes that had timed out in August
were split into 2,084 children, each refuted with a CaDiCaL native LRAT proof checked by cake_lpr at
generation time; a coverage audit over the ledger confirms that all 1,275 top-level cubes are closed,
1,227 directly and 48 through a complete set of children. The run took 67 core-hours on LUMI-C
(EuroHPC Development Access EHPC-DEV-2026D09-324). The ledger is in
`certificates/certc_p53k14.jsonl.gz` (3,359 cube rows plus the summary line).
Before that run the certifier was re-verified by recomputing p = 47 from scratch on the same machine:
all 990 cubes came back UNSAT with byte-identical `cnf_sha256` and `lrat_sha256` to the original
ledger produced on different hardware in August.

Brute force stops at p = 31, SAT model enumeration was run for p = 11, 19, 23, 29, 31, 37
(it times out at p = 41 and 43), and the whole-formula certificate covers 11 <= p <= 37.
Engine v1 shares the author and the search idea with engine B, so agreement of its count is
a consistency check, not an independent method. The certificate is what makes a list
complete; where the last column says "not certified", the count is the output of one
program.

Sequence: 1, 1, 1, 4, 1, 1, 9, 35, 30, 5, 13, 69, 23, 2, 2, 12, 3, 24, 2 for p = 3 to 71,
[OEIS A399437](https://oeis.org/A399437) (approved 2026-09-06).

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
