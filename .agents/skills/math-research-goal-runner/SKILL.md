---
name: math-research-goal-runner
description: Advance long-running mathematical physics research goals through proof construction, dependency tracking, adversarial audits, adaptive strategy, and resumable checkpoints. Use for sustained theorem research or recovery of a research goal, rather than routine paper summaries.
---

# Math Research Goal Runner

Codex owns execution, budget, and lifecycle. This skill owns mathematical method and evidence quality; it is not a scheduler and promises no unlimited runtime. Use the user's language for research records.

## Start or resume

1. Inspect Git status, branch, upstream, nearest AGENTS.md and any atlas-map.md/task-rules.md. Locate authoritative definitions, acceptance contract, current research index and checkpoint. Missing files may live on unmerged branches: inspect refs/PR metadata before declaring them missing. Preserve existing work.
2. Read [goal control](references/GOAL-CONTROL.md). Extract or recover the immutable Goal Contract, with precise quantifiers, topology, regularity, conclusions and forbidden substitutions. Reuse existing equivalent GOAL/STATE/CLAIMS/ATTEMPTS/CHECKPOINT records; do not create a parallel management system. At installation time create no empty research records.
3. For RECCVS only, read [project profile](references/RECCVS-PROFILE.md), then its authoritative repository sources. Other projects use their own definitions.
4. Reconcile checkpoint branch/commit, dirty-file hashes, source versions and evidence before reusing conclusions. Select a critical unresolved proof obligation and begin mathematical work, not merely another plan.

## Research loop

- Read [research methodology](references/RESEARCH-METHODOLOGY.md) for route selection, dependency graphs and stagnation. Construct an actual lemma, estimate, counterexample, theorem-interface audit or scoped computation that reduces a critical uncertainty.
- Record unique claim IDs, exact statements, assumptions, dependencies, domain/parameter scope, evidence and remaining gaps. Separate necessary obligations, auxiliary lemmas, candidate screens and exploration.
- Read [evidence standards](references/EVIDENCE-STANDARDS.md) before assigning or upgrading any status. Keep logic (PROVED/CONDITIONAL/CONJECTURAL/OPEN/REFUTED), evidence type, and audit status on separate axes. A proved implication does not prove its unverified premises.
- Read [proof audit](references/PROOF-AUDIT.md) for important conclusions or inherited proofs. Seek a concrete failure of the argument. Self-review is INTERNAL_AUDIT; an auxiliary agent is not automatically external independent verification. Delegation is optional and subject to the active authorization rules.
- Compare the new result with the contract and critical graph. Repeated equivalent failures require a diagnosis and a changed route or discriminating test. Prefer closing a necessary gap to increasing irrelevant numerical precision or document counts.
- Persist changed claims, attempts and a restartable checkpoint before budget/context limits, handoff, or a material strategy change. Continue within the runtime's actual lifecycle rules; no invented pauses, automatic background jobs or completion on budget exhaustion.

## Completion gate

Declare success only when the original conclusion holds, all necessary dependencies and external theorem hypotheses close, all computational evidence has justified scope, all required global regions are covered, no fatal audit defect remains, and proof plus evidence are independently inspectable. Conditional interfaces, local trapping, finite simulations, formal lemma statements and auxiliary endpoint roots cannot close a global theorem.

If the exact goal is rigorously refuted, report the precise counterexample/impossibility and its scope. A restricted-class obstruction only rules out that class. Never silently replace the goal; lifecycle termination for refutation follows runtime/user rules rather than claiming the requested theorem was proved.

## Resources

Copy/adapt only when needed: [Goal](assets/GOAL-TEMPLATE.md), [Claim](assets/CLAIM-TEMPLATE.md), [Checkpoint](assets/CHECKPOINT-TEMPLATE.md). The checkpoint template also specifies STATE and ATTEMPTS.

Run `python .agents/skills/math-research-goal-runner/scripts/validate_skill.py` from the repository root; add `--self-test` for isolated structural negative controls and a synthetic completion-gate exercise. These checks validate packaging and bookkeeping, not mathematical truth or model behavior. See [installation and examples](README.md).
