# Version policy: which release stands behind which number

Every value this repository has put into the OEIS, into a Zenodo record or into
a note is backed by one tagged release, and the release is backed by one encoder
hash. This file is the map. It is kept so that a reader can tell, for any number,
which encoder produced the certificate, which auditor checked it, and whether
anything was later withdrawn.

## Rules

1. Cite the version DOI (or the tag) of the release that carries the certificate,
   never the concept DOI alone. The concept DOI resolves to whatever version is
   current and says nothing about the state a number was checked in.
2. A certificate is valid only against the encoder hash recorded with its release.
   `audit_coverage.py` rebuilds every CNF from `gen_cnf.py` plus the cube's unit
   clauses and compares sha256, so a changed encoder would fail the audit rather
   than silently re-interpret old proofs.
3. Ledgers are never edited in place. A ledger that turns out wrong moves to a
   `superseded/` directory with the reason, and the re-issue is a new ledger,
   audited again. CI re-audits every live ledger on every push.
4. A withdrawn or corrected number gets a dated row in the second table below, a
   note in the README, and a correction wherever it was cited. The wrong value
   stays visible here.
5. A tag that was not deposited on Zenodo is listed as such; the next deposit
   supersedes it.

## Releases

Hashes are sha256, first 12 hex digits, of the file at that tag.

| Release | Date | Tag commit | `gen_cnf.py` | `cubes.py` | `audit_coverage.py` | Zenodo version DOI | What it certifies |
|---|---|---|---|---|---|---|---|
| v0.1 | 2026-08-23 | 1269619 | 5bec02f0d5e6 | 7222898f7fcb | 868ba1ea8f58 | 10.5281/zenodo.22067683 | p = 53, every rung k = 2..13, kissat DRAT checked by drat-trim and cake_lpr; cover certificates for the cube partition |
| v0.2 | 2026-09-08 | 7025502 | 5bec02f0d5e6 | 7222898f7fcb | 8cee50221de3 | not deposited | adds p = 59, k = 2..14 (CaDiCaL native LRAT checked by cake_lpr; the auditor now accepts that chain), and `classes/` with completeness certificates for the lists of affine classes up to p = 47 |
| v0.3 | 2026-09-17 | 0599f18 | 5bec02f0d5e6 | 181abd7f9b2d | 8a96401726fc | 10.5281/zenodo.22820692, completed as 0.3.1: 10.5281/zenodo.22821129 (2026-09-18) | adds p = 61, 67, 71, 73, every rung; retained-proof samples (404 LRAT files) deposited with 0.3.1; gzip ledgers and the hash-cache self-test in the auditor |
| v0.4 | 2026-10-13 | 3665a95 | 5bec02f0d5e6 | 181abd7f9b2d | 8a96401726fc | 10.5281/zenodo.23327304 (published 2026-10-13) | adds p = 79, k = 2..16 (the k = 16 ledger lives in the Zenodo record and is fetched by sha256); the class list certificates for p = 53, 59 and 61 |
| after v0.4 | 2026-10-15 | 2b473ab | 5bec02f0d5e6 | 181abd7f9b2d | 8a96401726fc | next deposit | completeness certificate for the class list of p = 67 (`classes/certificates/`) |

The encoder has the same hash in every tag. The only change to `gen_cnf.py` in
the repository's history is the lex-leader fix of 2026-08-23, made before v0.1;
the ledgers produced before that fix are the superseded ones listed below. The
`cubes.py` change in v0.3 is a hash-prefix cache; the bytes hashed are the same,
and `audit_coverage.py --selftest` checks the cached hash against the plain
serialization on 300 cubes in CI.

## Published numbers and the release behind each

| Number | Where | Release with the certificate |
|---|---|---|
| m(53) = 14, A398173 a(15) | OEIS, Zenodo | v0.1 |
| m(59) = 15, A398173 a(16) | OEIS, Zenodo | v0.2 (tag only); first deposited with v0.3 |
| m(61) = 15, m(67) = 16, m(71) = 16, m(73) = 16, A398173 a(17) to a(20) | OEIS, Zenodo | v0.3 / 0.3.1 |
| m(79) = 17, A398173 a(21) | OEIS, Zenodo | v0.4 |
| affine class counts, A399437, p up to 47 | OEIS | v0.2 (commit 0f03d0c, 2026-08-27) |
| affine class counts for p = 53, 59, 61 (2, 12, 3) | OEIS | v0.4 (commits 0cdcd1f, 8a76137, 95069f8 of 2026-09-18 to 09-25) |
| affine class count for p = 67 (24) | OEIS | commit 2b473ab (2026-10-15); next deposit |
| affine class counts for p = 71, 73 (2, 4) | OEIS | search only, no completeness certificate; `classes/README.md` says so |

The OEIS entries for a(16) to a(20) were accepted in August 2026, before any
certificate existed, on two independent search programs and checked witnesses;
this repository does not keep the submission text, only the certificates that
followed (v0.2, v0.3) and that the entry's links point to now. Values are upper bounds from `witnesses/` plus lower
bounds from the ladders; the witness side needs no release, `check_witness.py`
recomputes it from the definition.

## Withdrawn and superseded

| Date | What | Why | Where it went | Effect on published numbers |
|---|---|---|---|---|
| 2026-08-22, superseded 2026-08-23 | first issue of the p = 53 ledgers, k = 2..13 (the k = 13 first-issue ledger is the one kept; the lower rungs were simply recomputed) | one wrong sign in the lex-leader chain of the symmetry breaker excluded part of the search space (`encoding-tests/README.md`); caught by the property test "the whole group is accepted at k = p" | `ledgers/p53/superseded/`, kept, not certificates | none: m(53) = 14 stood, every rung was recomputed with the fixed encoder and audited again before v0.1 |
| 2026-09-17, completed 2026-09-18 | Zenodo record of v0.3 | the record was published while files were still uploading; it holds the tarball, the manifest and one proof sample | version 0.3.1 (10.5281/zenodo.22821129) carries the complete file set | none; a deposit correction, not a value correction |
| 2026-09-09 | README sentence that the concept DOI resolves to the latest version | it resolved to v0.1 at the time | commit 0d2556a | none |

Nothing published from this repository has been withdrawn as a value. If that
changes, the row goes here first.
