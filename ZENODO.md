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
