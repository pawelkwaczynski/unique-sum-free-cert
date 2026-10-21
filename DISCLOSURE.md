# Tool disclosure

I signed the Leiden Declaration on AI in mathematics and this is the
disclosure it asks for. RELEASE.md answers the more detailed questions of the
AGMAI recommendations on releasing AI-assisted mathematics.

AI coding assistants (Anthropic Claude and OpenAI Codex, 2026 versions) were
used heavily while writing the scripts in this repository, the search engines
that produced the witnesses, and the certification pipeline that produced the
ledgers. They also drafted much of the documentation, including RELEASE.md and
the files in `provenance/`; I read every sentence before it went in. The SAT
encoding and the cube partition were worked out together with the assistants.
I chose the problem, decided what to compute and how to check it, ran the
computations, and checked the results against the ledgers before they went
into the OEIS.

No mathematical claim here rests on an assistant's word. Each lower bound rests
on proofs that the formally verified checker cake_lpr accepted when they were
generated (directly from CaDiCaL's LRAT output, or after drat-trim for kissat's
DRAT output; the ledger row says which), bound to their CNF by sha256 and
audited for coverage by `audit_coverage.py`. Most proofs were deleted after
checking; README.md, "Verification tiers", says what is kept. Each upper bound
is a witness set checked against the definition by `witnesses/check_witness.py`.
Anyone can rerun the witness check and the coverage audit without trusting me
or any model.
