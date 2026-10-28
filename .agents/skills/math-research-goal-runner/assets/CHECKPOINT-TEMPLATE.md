# CHECKPOINT {{id}} / {{timestamp_with_timezone}}

- Goal / immutable contract version and source hashes: {{goal_pointer}}
- Repository / branch / HEAD / upstream: {{git_identity}}
- Dirty and untracked research inputs with SHA-256: {{paths_hashes}}
- Existing GOAL / STATE / CLAIMS / ATTEMPTS locations: {{mapping}}
- Evidence integrity: {{source_certificate_hashes_and_stale_receipts}}
- Environment and scoped reproducible commands: {{cwd_commands_versions_outputs}}
- Open questions requiring user input (if any): {{precise_question_and_independent_work}}
- Runtime boundary: {{budget_context_user_pause_or_handoff_with_actual_state}}

## STATE delta

- Necessary obligations actually closed: {{ids_and_receipts}}
- Critical unresolved / conditional dependencies: {{ids_and_premises}}
- Graph changes and affected claims: {{edges_and_status_changes}}
- Rigorously excluded routes and exact scope: {{obstructions}}
- Current route and reason: {{choice}}
- Goal completion gate result: {{unfinished_or_receipt_for_all_gates}}

## ATTEMPTS delta

| Attempt ID / date | Input revision | Claim / route | Actual mathematical work and artifact | Outcome / failure signature | Reason / excluded class | Next discriminating action |
|---|---|---|---|---|---|---|
| {{id}} | {{rev}} | {{claim}} | {{derivation_or_experiment}} | {{result}} | {{diagnosis}} | {{action}} |

## Resume action

First verify versions, dirty hashes and evidence scope; do not restart the whole archive. Then execute {{specific_next_derivation_or_command}} on {{claim_id}}, using {{inputs}}. Expected result or falsification criterion: {{decision}}. Alternative route if it fails: {{alternative_and_trigger}}. Do not repeat attempts {{ids}} without a changed mathematical input.
