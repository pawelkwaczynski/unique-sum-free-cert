# How these results were produced

This file answers the questions in Step I, points 3 to 5, of "Responsible Release of AI-Generated Mathematics"
(agmai.org, 29 September 2026). Those recommendations are addressed to AI labs. I am not one, but the questions
are fair to ask of any result that was computed with heavy use of AI tools, so I answer them here. The tool
disclosure itself is in DISCLOSURE.md.

## What is released

| Result | Status | Where |
|---|---|---|
| m(p) for p = 53, 59, 61, 67, 71, 73, 79 (OEIS A398173, a(15) to a(21)) | lower bounds: every k from 2 through m(p) - 1 refuted cube by cube, each proof checked by cake_lpr when it was generated, CNF and proof hashes kept, most proofs not retained (tier "solver-certified, hash-bound"); upper bounds: witness sets checked against the definition | this repository; Zenodo concept DOI 10.5281/zenodo.22067682; the release behind each value is in VERSION_POLICY.md |
| completeness of the lists of affine classes of minimum sets (OEIS A399437), p = 11 to 67 | certified (LRAT, cake_lpr); the p = 67 certificate came after v0.4 and goes into the next deposit | `classes/` |
| the same lists for p = 71 and 73 | search only, no completeness certificate | `classes/` |

The values m(53) = 14 and m(59) = 15 appear in Scheinerman's 2019 thesis (Table 3.1) with witnesses and without
proofs of minimality. For those two primes this repository adds certificates of minimality, not new values, and
README.md also cites an independent certification of both.

## Models (point 3)

- Anthropic Claude and OpenAI Codex, 2026 versions, as coding assistants and as reviewers of each other's code.
  xAI Grok was a third reviewer for some decisions and for one test of the encoder. I did not record exact model
  versions for each period, so I do not list them.
- Small local language models were tried on the problem itself and abandoned (see the last section).
- No model output is part of any proof. Proofs come from the SAT solvers (CaDiCaL, kissat), are checked by
  cake_lpr, a formally verified checker, and are bound to their formulas and audited for coverage by
  `audit_coverage.py`. Witnesses are checked against the definition by `witnesses/check_witness.py`.

## Prompts and reasoning (point 3)

- Prompts: the tasks given to the assistants were written as specifications with acceptance criteria and an
  explicit list of what not to do, and a model of a different family reviewed each change before it ran at
  scale. The prompt texts themselves are not released.
- Reasoning: I kept a dated working diary recording decisions, measurements and retractions. The part about this
  problem is released as `provenance/diary_extract.md`, without names of correspondents and without private
  correspondence. Mistakes and wrong estimates are kept in it.

## Time and cost (point 3)

| Item | Value |
|---|---|
| first own term, a(15) | submitted to OEIS on 29 July 2026, published on 4 August 2026; computed by a cube search of 26 minutes on 6 cores |
| top rung of m(79), k = 16 | 25 jobs, 35,262 allocated core-hours, 24 September to 9 October 2026, on LUMI-C |
| whole LUMI allocation, not only m(p) | 85,935 core-hours as of 21 October 2026 |
| sum of the energy readings Slurm reports for the LUMI jobs, 16 September to 21 October 2026, whole allocation | 516.6 kWh (ConsumedEnergyRaw, largest step per job, 205 jobs) |
| computation before LUMI (laptop and cloud machines) | not recorded in one place |
| cost of the AI tools | subscriptions, not metered per task |

## Formalization (point 4)

- The UNSAT results are certified in the sense above: each cube's proof was checked by cake_lpr, bound to its
  CNF by SHA-256, and the cubes were audited for coverage.
- The CNF encoding is not formally verified. It is tested: against an independently written encoder (68 whole
  instances and 300 replayed cubes), by two property tests, and against a brute-force search from the definition
  for every p up to 23 and every k (`encoding-tests/`). A clause-by-clause description of the encoding is planned
  for the accompanying note. There is no Lean formalization of these results and no formalization.yaml.
- The short form I use: UNSAT certified, encoder tested but not proved.

## How AI came to be used here, and what failed (point 5)

- The problem is Problem 27 in Ben Green's list of 100 open problems. I chose it because both halves of the
  answer can be checked without trusting anyone: a witness checks itself, and a lower bound can carry a
  certificate.
- I tried small local language models (about 4B parameters) as generators of structural rules; the rule a Qwen
  model proposed was empty, since the Cauchy-Davenport theorem already gives |A + A| >= 2k - 1, and Phi-4 failed
  twice for technical reasons. I also ran an evolutionary search loop around a local language model for witnesses;
  its best candidates still had four unique sums, so it found no witness. The released witnesses came from the
  search engines (whose code was written with AI assistance), and each is accepted only after the
  definition-level check.
- The 19 entries for this problem from my attempt log are in `provenance/dead_ends.jsonl`: 18 attempts that were
  abandoned or set aside and one retry that succeeded, each with what was tried, why it looked promising, how it
  was ruled out and the evidence. The rest of the log concerns other work and is not part of this release.
