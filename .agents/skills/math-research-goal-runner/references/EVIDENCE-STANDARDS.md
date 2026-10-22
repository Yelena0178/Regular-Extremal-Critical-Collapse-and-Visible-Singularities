# Evidence standards

## Three independent axes

| Axis | Values and interpretation |
|---|---|
| Logic | PROVED: exact statement established with discharged premises; CONDITIONAL: application still assumes listed unresolved premises; CONJECTURAL: plausible without proof; OPEN: unresolved; REFUTED: exact statement has a valid counterexample or contradiction |
| Evidence (one or more) | ANALYTIC: inspectable proof; EXACT_ALGEBRA: exact identity or finite deduction; CERTIFIED_NUMERICS: rigorous error enclosure under stated arithmetic assumptions; EXPERIMENTAL: floating-point simulation or sampled check; LITERATURE: sourced external theorem; HEURISTIC: plausibility argument |
| Audit | UNCHECKED; INTERNAL_AUDIT (including same-model adversarial pass); INDEPENDENT_REVIEW (name actual reviewer, independence and scope); FAILED (unresolved defect) |

Evidence types are not an ordinal ladder. An exact finite identity can be PROVED/EXACT_ALGEBRA/INTERNAL_AUDIT while its proposed PDE consequence remains CONDITIONAL. A lemma entered in a proof assistant is only a statement until checked without untrusted axioms/sorry/admit in its dependency closure. A checked formal proof still needs a model-to-formal-statement correspondence audit.

## Evidence receipt

Record claim ID, exact covered statement, domain/time/parameter range, input data and source version/hash, algorithm or theorem locator, assumptions, outputs/certificate paths, reproducible command/environment, actual outcome and limitations. A missing receipt cannot be filled by a remembered PASS.

For certified numerics include outward rounding or exact arithmetic, all discretization/truncation/interpolation errors, infinite tails, interval coverage, well-posedness and transfer from the certified auxiliary object to the actual PDE. State any trusted implementation/arithmetic assumptions. A finite enclosure does not prove a global development, exact extremality, all-time decay or causal identity without a separate analytic bridge.

For external theorems record author/title/version/DOI or URL, theorem/page/section, exact hypotheses, normalization and sign conversion, data topology, domain, conclusion and which project claim it supports. Verify every premise; a cited theorem does not discharge its own applicability. Distinguish the paper's theorem from a proposed corollary.

## Invalid upgrades

- No counterexample found does not prove existence or universality.
- Higher precision and mesh convergence alone remain EXPERIMENTAL.
- A finite parameter sample is not an interval theorem.
- Local trapping is not complete formation/criticality; a fitted endpoint is not an exact equality.
- A model's second pass or a second agent is not automatically an independent external review.
- A certificate with changed source hashes is evidence for its original object until transfer is justified.

If an audit fails, retain the receipt, mark FAILED, and invalidate or downgrade affected downstream conclusions. A correction must state what changed and what remains valid.
