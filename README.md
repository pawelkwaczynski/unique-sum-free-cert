# unique-sum-free-cert

Machine-checked certificates for the exact values of m(p), the smallest size
of a unique-sum-free subset of Z/pZ, for the primes p = 53, 59, 61, 67, 71, 73.
These are the terms a(15) through a(20) of [OEIS A398173](https://oeis.org/A398173)
and the small cases of Problem 27 in Ben Green's
[100 open problems](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf).

A nonempty set A in Z/pZ is unique-sum-free when every element of A+A can be
written as a+b with {a, b} from A in at least two different ways (a = b is
allowed). m(p) is the minimum |A|. The function is not monotone in |A|, so an
exact value needs two separate things: a witness of size m(p), and a refutation
for every k below m(p), not only for k = m(p) - 1.

## Re-issue notice (2026-08-23)

The first issue of the p = 53 ledgers was produced with a symmetry breaker that
excluded part of the search space (one wrong sign in the lex-leader chain,
details in `encoding-tests/README.md`). Those files are kept under
`ledgers/p53/superseded/` and are not certificates. Everything under
`ledgers/p53/k*/` was recomputed with the fixed encoder and audited again.

## Values

| p | m(p) | witness | lower bound k = 2 .. m(p)-1 | status |
|---|---|---|---|---|
| 53 | 14 | `witnesses/` | every k = 2..13 refuted, each rung audited (`ledgers/p53/`) | solver-certified, hash-bound |
| 59 | 15 | `witnesses/` | queued | search only |
| 61 | 15 | `witnesses/` | queued | search only |
| 67 | 16 | `witnesses/` | k = 15 in progress on cloud workers | search only |
| 71 | 16 | `witnesses/` | k = 15 in progress on cloud workers | search only |
| 73 | 16 | `witnesses/` | queued | search only |

"Search only" means the value was established by two independent search
programs (an orbit-canonical branch-and-bound in C and a SAT cube-and-conquer),
with the witness checked by a third method, but no proof object has been
retained yet. This table is updated as ledgers land.

## Prior work, exactly

- Scheinerman, *Several problems in linear algebraic and additive
  combinatorics*, Ph.D. thesis, Rutgers 2019,
  [doi:10.7282/t3-1w2k-jr68](https://doi.org/10.7282/t3-1w2k-jr68), Table 3.1:
  tabulates m(p) with a witness for every prime p <= 59, without proofs of
  minimality. The values m(53) = 14 and m(59) = 15 are his; the p = 59 witness
  published in the OEIS coincides with his set, as two lex-first searches will.
- Mark Watson, [unique-sums-notes](https://github.com/mkwatson/unique-sums-notes):
  contributed A398173, holds retained LRAT proofs for m(53) and m(59) and DRAT
  proofs for m(41), m(43), m(47), a Lean 4 bridge from CNF toward the
  mathematical statement, and a DRAT-certified census of m(G) over small
  finite Abelian groups, contiguous through order 52. The next rows of that
  census are the primes 53 through 73, which are the values certified here;
  `export_ledger.py` writes this repository's ledgers in his row layout so
  the two tables can be joined without recomputation.
- Bedert, *On unique sums in Abelian groups*, Combinatorica 44 (2024),
  [arXiv:2303.15134](https://arxiv.org/abs/2303.15134): the theory.
- The values m(61), m(67), m(71), m(73) were first computed here (OEIS
  A398173, August 2026). m(53) and m(59) were proved minimal independently
  here and by Watson in the same month.

## Verification tiers

Tier names follow the usual SAT-community usage and match the ones used in
unique-sums-notes, so a claim means the same thing in both tables.

- **DRAT-certified**: the refutation is retained and replays under an
  independent checker. Nothing here is at this tier yet.
- **solver-certified, hash-bound**: every cube's DRAT proof was checked by
  drat-trim and replayed by cake_lpr at generation time; the proof was then
  deleted and only its sha256, together with the sha256 of the exact CNF, is
  kept in the ledger. The coverage auditor rebuilds each CNF from `gen_cnf.py`
  plus the cube's unit clauses and refuses any row whose hash does not match.
  p = 53 is at this tier for every k from 2 to 13. From here on the LRAT files are retained.
- **search only**: two independent programs agree, witness checked. No proof
  object.

Trusted surfaces that nothing here certifies: that `gen_cnf.py` encodes the
definition faithfully (see `encoding-tests/` for what has been tested), the
checkers themselves, and the coverage argument in `audit_coverage.py`.

## Reproduce

```
python3 witnesses/check_witness.py                      # upper bounds, no tools needed
python3 audit_coverage.py 53 13 ledgers/p53/k13/certified.jsonl   # coverage + hash binding
python3 gen_cnf.py 53 13 > p53k13.cnf                   # the formula itself
```

The auditor needs nothing beyond Python. Re-checking an individual proof needs
the tool chain in `tools/README.md` and the proof file, which for p = 53 no
longer exists; for later ledgers the retained LRAT will be deposited with a DOI.

## Layout

- `gen_cnf.py`: the SAT encoding (membership of i on variable i+1, pair
  variables, Sinz counters for |A| = k, WLOG 0 and 1 in A, a sumset bound and
  a reflection symmetry breaker).
- `cubes.py`: cube tags (position cubes: the 3rd, 4th, 5th smallest elements of
  A, every residue between them excluded), their unit clauses, and the exact
  CNF serialization the hashes are computed over.
- `audit_coverage.py`: fail-closed coverage and hash-binding audit of a ledger.
- `verify_drat.sh`: drat-trim then cake_lpr on one CNF/DRAT pair.
- `export_ledger.py`: export to the Watson row layout.
- `ledgers/p<p>/k<k>/`: one ledger per (p, k), plus the exported layout.
- `witnesses/`: the witness sets and a definition-level checker.
- `encoding-tests/`: differential test against an independent encoder.

## License

Code MIT, data CC BY 4.0 (`LICENSE`, `LICENSE-DATA.md`). Tool licenses in
`THIRD_PARTY_NOTICES.md`. Tool use is described in `DISCLOSURE.md`.
