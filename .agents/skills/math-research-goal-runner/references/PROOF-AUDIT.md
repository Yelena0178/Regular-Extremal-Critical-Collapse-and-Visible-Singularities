# Adversarial proof audit

Audit an exact claim and its dependency closure, not the author's confidence. Start with the most likely fatal step. Produce either a concrete defect with its downstream effect or a bounded audit receipt specifying what was actually checked. Absence of a detected defect is not an independent proof.

| Attack | Required check |
|---|---|
| Hidden assumptions/circularity | Expand every imported premise; detect dependence on the desired conclusion, including bootstrap and compactness arguments |
| Quantifiers/uniformity | Track constants, parameter intervals, endpoints, and which estimates must be uniform; do not demand unnecessary uniformity |
| Limits | Justify exchanging time, radius, parameter and weak/strong limits; specify domination/compactness and uniqueness |
| Function spaces | Check weights, embeddings, dimension, derivative loss, traces, regularity at boundaries and gauge transformations |
| PDE continuation | Check well-posedness, bootstrap closure, blow-up criteria, domain coverage and compatibility; finite control must cover the continuation region |
| Center/boundary | Check axis parity, regular center, constraints, corner conditions, AF tails and boundary flux signs |
| Geometry/causality | Distinguish coordinate breakdown from singularity; identify actual I+ and event horizon before using them; distinguish local from global statements |
| External theorem | Verify version, all hypotheses, conventions and actual conclusion rather than a convenient paraphrase |
| Computation | Attempt bad inputs, sign errors, non-rigorous rounding, incomplete parameter coverage and incorrect solution transfer |

Check simple limits or known solutions as negative/positive controls when relevant. A counterexample to an intermediate step need not refute the final theorem. Record the failed step, minimal correction, affected claims and remaining uncertainty.

Construction and adversarial passes may be separated between agents if available and authorized. Do not require multiple agents. Label same-model/agent rederivation INTERNAL_AUDIT unless actual independent review is established and documented. Keep an important conclusion UNCHECKED until the stated pass has actually been performed.
