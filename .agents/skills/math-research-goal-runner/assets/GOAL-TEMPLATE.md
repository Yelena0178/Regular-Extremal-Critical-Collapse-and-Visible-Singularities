# GOAL: {{goal_id}} / contract {{version}}

- Authority: {{user_decision_and_source_paths}}
- Source revision / SHA-256 for dirty sources: {{versions}}
- Model, conventions and definitions: {{model}}
- Assumptions: {{assumptions}}
- Quantifiers and complete parameter intervals: {{quantifiers}}
- Function spaces, topology, regularity, gauge: {{spaces}}
- Exact conclusion and global region: {{theorem}}
- Forbidden weakenings/substitutions: {{forbidden}}
- Acceptance gates: {{gate_id_to_precise_requirement}}
- State / claims / attempts / checkpoint locations: {{existing_repository_mapping}}
- Contract changes: {{only_explicit_user_authorized_deltas}}

## Initial proof frontier

| ID | Role | Exact obligation and scope | Premises / dependencies | Existing evidence | Gap | Verification | Goal gate |
|---|---|---|---|---|---|---|---|
| {{id}} | NECESSARY / AUXILIARY / SCREEN / EXPLORATORY | {{statement}} | {{ids_or_explicit_premises}} | {{receipt}} | {{gap}} | {{method}} | {{gate}} |

## Completion receipt (fill only after verification)

For every gate: supporting claim IDs, transitive dependencies, discharged external hypotheses, domain coverage, audit receipt and inspectable proof/evidence paths. Any open required premise keeps the goal unfinished. A counterexample requires its own audited scope and does not automatically prove a substitute theorem.
