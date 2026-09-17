# Zenodo deposit, version 0.3 (2026-09-18)

Concept DOI (all versions): 10.5281/zenodo.22067682. Version 0.1: 10.5281/zenodo.22067683. Version 0.2 was
released on GitHub (tag v0.2, 2026-09-08) but never deposited; v0.3 supersedes it and is the next deposit.
Manual "New version" on the record, GitHub integration stays off for this repository.

Title: unique-sum-free-cert: machine-checked certificates for m(p), p = 53 to 73 (v0.3)
Upload type: dataset
Creators: Kwaczyński, Paweł (ORCID 0009-0004-0627-3621), Łódź, Poland
License: CC BY 4.0 (data); code MIT in the repository
Keywords: unique-sum-free sets, Green's Problem 27, OEIS A398173, OEIS A399437, SAT, DRAT, LRAT, CaDiCaL, kissat, cake_lpr, cube-and-conquer, certificates, affine classes, LUMI
Related identifiers: https://oeis.org/A398173 (isSupplementTo), https://oeis.org/A399437 (isSupplementTo), https://github.com/pawelkwaczynski/unique-sum-free-cert (isSupplementTo), doi:10.7282/t3-1w2k-jr68 (cites, Scheinerman 2019), arXiv:2303.15134 (cites, Bedert), https://github.com/mkwatson/unique-sums-notes (references)
Description (short): Ledgers of hash-bound unsatisfiability certificates refuting a unique-sum-free subset of Z/pZ of size k for every k from 2 to m(p)-1, for the six primes p = 53, 59, 61, 67, 71, 73 (OEIS A398173, a(15) to a(20)), cover certificates for every cube partition, the witnesses of size m(p), the encoder and the auditors that rebuild every CNF and check coverage. New in 0.3: the complete ladders for p = 61 (k = 2..14), 67 (k = 2..15), 71 (k = 2..15) and 73 (k = 2..15), 1,171,344 ledger rows in total, computed on cloud workers and on the EuroHPC supercomputer LUMI-C (Development Access EHPC-DEV-2026D09-324); the two largest ledgers are gzip-compressed and every tool reads both forms. Also carries what v0.2 added on GitHub: the p = 59 ladder, classes/ (OEIS A399437) and the native LRAT chain in the auditor.
Files: release tarball of the tagged repository (tag v0.3), SHA256SUMS, ledgers/ (p53 .. p73: certified.jsonl[.gz], cover.jsonl, watson-format/ per rung), classes/, witnesses/; plus the retained-proof sample: lrat_sample_p61k14.tar.zst (81 proofs, 1.3 GB), lrat_sample_p67k15.tar.zst (100, 1.5 GB), lrat_sample_p71k15.tar.zst (105, 1.4 GB), lrat_sample_p73k15.tar.zst (118, 2.1 GB), the four *_SELECTED.tsv tables and their SHA256SUMS. Each sample is 1 in 20 of the top-level cubes of the top rung, run again on LUMI-C on 2026-09-17 with CaDiCaL native LRAT and the proofs kept; cubes that timed out in the sample run carry no proof and are not in the sample.
Acknowledgement (required by the EuroHPC Development Access terms): We acknowledge EuroHPC Joint Undertaking for awarding us access to LUMI at CSC, Finland.
Version: 0.3 (2026-09-18). Next: classes for p >= 53 (A399437 a(20) once the p = 73 census finishes), m(79) cost sample.

# Zenodo deposit, version 0.2 (2026-09-08)

Concept DOI (all versions): 10.5281/zenodo.22067682. Version 0.1: 10.5281/zenodo.22067683. The
version DOI for 0.2 is minted by Zenodo when the new version is published (GitHub integration on
the v0.2 release, or "New version" on the record with the v0.2 tarball); put it in CITATION.cff
and README afterwards.

Title: unique-sum-free-cert: machine-checked certificates for m(p), p = 53 and 59 (v0.2)
Upload type: dataset
Creators: Kwaczyński, Paweł (ORCID 0009-0004-0627-3621), Łódź, Poland
License: CC BY 4.0 (data); code MIT in the repository
Keywords: unique-sum-free sets, Green's Problem 27, OEIS A398173, OEIS A399437, SAT, DRAT, LRAT, CaDiCaL, cake_lpr, cube-and-conquer, certificates, affine classes
Related identifiers: https://oeis.org/A398173 (isSupplementTo), https://oeis.org/A399437 (isSupplementTo), https://github.com/pawelkwaczynski/unique-sum-free-cert (isSupplementTo), doi:10.7282/t3-1w2k-jr68 (cites, Scheinerman 2019), arXiv:2303.15134 (cites, Bedert), https://github.com/mkwatson/unique-sums-notes (references)
Description (short): Ledgers of hash-bound unsatisfiability certificates refuting a unique-sum-free subset of Z/pZ of size k for every k from 2 to m(p)-1, for p = 53 (k = 2..13, kissat, DRAT checked by drat-trim and cake_lpr) and p = 59 (k = 2..14, CaDiCaL native LRAT checked by cake_lpr), cover certificates for every cube partition, the witnesses of size m(p), the encoder and the auditors that rebuild every CNF and check coverage. New in 0.2: the complete p = 59 ladder (28,496 ledger rows, 151.8 CPU-h), the affine classes of minimizers with completeness certificates for 11 <= p <= 47 (classes/, OEIS A399437), and an auditor that accepts the native LRAT chain. Values for p = 61, 67, 71, 73 are not certified in this version (see VERIFICATION_MAP.md); single rungs for those primes are finished on cloud workers and will follow.
Files: release tarball of the tagged repository (tag v0.2), SHA256SUMS, ledgers/ (p53, p59: certified.jsonl, cover.jsonl, watson-format/ per rung), classes/, witnesses/.
Version: 0.2 (2026-09-08). Next versions add p = 61, 67, 71, 73 and the completeness certificates for the classes at p >= 53.

# Zenodo deposit: PUBLISHED 2026-08-23

Record https://zenodo.org/records/22067683, version DOI 10.5281/zenodo.22067683, concept DOI (all versions) 10.5281/zenodo.22067682. Next versions: use "New version" on the record (or the GitHub integration) and keep the concept DOI in citations.

# Zenodo deposit (to be created by the author; this file is the metadata draft)

Title: unique-sum-free-cert: machine-checked certificates for m(p), p = 53 (v0.1)
Upload type: dataset (software as a second record at the next tag)
Creators: Kwaczyński, Paweł (ORCID 0009-0004-0627-3621), Łódź, Poland
License: CC BY 4.0 (data); code MIT in the repository
Keywords: unique-sum-free sets, Green's Problem 27, OEIS A398173, SAT, DRAT, LRAT, cake_lpr, cube-and-conquer, certificates
Related identifiers: https://oeis.org/A398173 (isSupplementTo), https://github.com/pawelkwaczynski/unique-sum-free-cert (isSupplementTo), doi:10.7282/t3-1w2k-jr68 (cites, Scheinerman 2019), arXiv:2303.15134 (cites, Bedert), https://github.com/mkwatson/unique-sums-notes (references)
Description (short): Ledgers of hash-bound unsatisfiability certificates for every k from 2 to 13 refuting a unique-sum-free subset of Z/53Z of size k, cover certificates for the cube partition, the witness of size 14, the encoder and the auditors that rebuild every CNF and check coverage. Proof objects were replayed by drat-trim and the verified checker cake_lpr at generation time; hashes are retained. Values for p = 59..73 are not certified in this version (see VERIFICATION_MAP.md).
Files: release tarball of the tagged repository (tag v0.1), SHA256SUMS, ledgers/ (certified.jsonl, cover.jsonl, watson-format/ per rung), witnesses/.
Version: 0.1 (2026-08-23). Next versions add p = 61, 67, 71, 73 and retained LRAT samples.
Procedure: tag v0.1 (`git tag -a v0.1 -m v0.1 && git push origin v0.1`), download the GitHub tarball, upload to Zenodo with this metadata, then put the DOI in README, CITATION.cff and the OEIS entry (LINKS line).
