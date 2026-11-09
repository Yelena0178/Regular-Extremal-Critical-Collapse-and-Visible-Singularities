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

## Research health / strategic review delta

- Core bottleneck signature (necessary gap / missing input / mechanism): {{signature}}
- Last valid strategic movement (round / time / evidence / before-after gap): {{baseline}}
- Local gains that do not yet move that frontier: {{local_results_and_bridge_still_missing}}
- Rounds / active minutes since strategic movement; unknown timing stays unknown: {{counters}}
- Thresholds and last check (default 5 rounds OR 180 active minutes; 2 equivalent failures): {{settings_and_check}}
- Last review / unchanged-frontier review count / next review deadline: {{review_history}}
- Review receipt and actual route change, or evidence for a bounded continuation: {{receipt}}
- Next discriminating test / rejection criterion / effort budget: {{test_and_budget}}

## GitHub synchronization delta

- Ongoing authorization source, or explicit no-sync restriction: {{authorization}}
- Confirmed local repository / GitHub remote and push destination / existing branch: {{mapping}}
- Current round artifact paths / precommit HEAD / actual validation: {{round_scope}}
- Previous confirmed round / local commit / remote observation / verification time: {{previous_receipt}}
- Pending round/commit and status (local-only / committed-pending / verification-pending): {{pending_or_none}}
- Error / retry count / next retry or required action: {{sync_recovery}}

Carry the current commit's post-push receipt in the user report or an external log, then into the next checkpoint; do not try to embed this checkpoint's own commit hash or create a receipt-only commit loop.

## Resume action

First verify versions, dirty hashes, evidence scope, research-health counters and pending sync; do not restart the whole archive or reset the strategic clock. Perform a due strategic review before repeating the same route. Then execute {{specific_next_derivation_or_command}} on {{claim_id}}, using {{inputs}}. Expected result or falsification criterion: {{decision}}. Alternative route if it fails: {{alternative_and_trigger}}. Do not repeat attempts {{ids}} without a changed mathematical input.
