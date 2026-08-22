# Tool disclosure

I signed the Leiden Declaration on AI in mathematics and this is the
disclosure it asks for.

AI coding assistants (Anthropic Claude and OpenAI Codex, 2026 versions) were
used heavily while writing the scripts in this repository, the search engines
that produced the witnesses, and the certification pipeline that produced the
ledgers. I designed the encoding and the cube partition, chose what to compute,
ran the computations, and read every number before it went into a ledger or
into the OEIS.

No mathematical claim here rests on an assistant's word. Each lower bound is a
DRAT proof checked by drat-trim and replayed by the formally verified checker
cake_lpr, bound to its CNF by sha256 and audited for coverage by
`audit_coverage.py`. Each upper bound is a witness set checked against the
definition by `witnesses/check_witness.py`. Anyone can rerun both without
trusting me or any model.
