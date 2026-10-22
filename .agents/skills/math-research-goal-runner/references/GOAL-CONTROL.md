# Goal control and recovery

## Contract and source authority

Record the exact target, model/conventions, assumptions, quantifiers and parameter intervals, data class, function spaces and topology, regularity, conclusion, acceptance gates and explicitly forbidden weakenings. Record authoritative paths, commit IDs and SHA-256 of dirty sources, plus user decisions resolving conflicts. A newer status summary is not automatically a revised acceptance theorem. If authoritative sources genuinely conflict and the session does not resolve it, identify the conflicting clauses and ask a focused question while doing independent work.

Strategies, tools and candidate families may change without changing the contract. A user-approved change creates a new contract version with a delta and invalidates affected claims. Do not strengthen assumptions, shorten the parameter interval, remove a global region or substitute a related theorem just to pass a gate.

## Persistent logical objects

Map these objects to existing repository mechanisms first; create files only during actual research if no equivalent exists. Keep state outside the installed skill directory.

| Object | Minimum contents |
|---|---|
| GOAL | Immutable contract, authority/version, prohibited substitutions, completion gates |
| STATE | Contract version, critical obligation graph, frontier and blockers, current route, changed obligations |
| CLAIMS | Unique ID, exact statement/scope, premises, dependencies, evidence, three status axes, validation and relation to goal |
| ATTEMPTS | ID/date, input revision, claim/route, method, actual result/artifact, failure signature and reason, eliminated class, next discriminating action |
| CHECKPOINT | Object locations, revision and dirty hashes, evidence integrity, reproducible commands/certificates, changed conclusions, next executable task and expected decision |

Use relative repository paths in records where practical. Checkpoint timestamps include timezone. Never put credentials in checkpoints or logs. Store only deltas plus stable pointers instead of repeating the research archive each cycle.

## Recovery procedure

1. Locate the latest coherent checkpoint, authoritative contract and state index. Confirm repository, branch, commit, upstream and worktree differences. Do not switch a dirty checkout or overwrite its work.
2. Compare contract/source/evidence hashes. If a source changed, inspect only the delta and dependent claims; mark their old audit stale until checked. Preserve the old certificate and its scope.
3. Restore the graph and unresolved premises; verify referenced artifacts actually exist. Rerun the narrowest integrity/reproduction check needed, in a disposable output directory if the command overwrites evidence.
4. Read recent ATTEMPTS failure signatures before selecting work. State what is still open and carry out the checkpoint's concrete next action, or document why new evidence changes priority.

## Completion decision

For each acceptance gate list the exact supporting claims and transitive closure. Reject missing/cyclic dependencies, unresolved premises, REFUTED/OPEN/CONJECTURAL/CONDITIONAL required claims, failed/unchecked important audits, theorem-hypothesis mismatches and scope gaps. A PROVED local implication may coexist with an OPEN global application. INDEPENDENT_REVIEW is not mandatory unless the contract requires it; honest internal audit and inspectable proof are mandatory for a success claim.

Report progress as closed necessary obligations, remaining conditional links, rigorously excluded routes and the next critical uncertainty. Avoid percentages based on tasks/documents. At a runtime boundary checkpoint unfinished work and report its actual state; budget exhaustion cannot satisfy a mathematical gate. Runtime goal status APIs, when available, remain governed by their own rules, including blocked thresholds and explicit user pause requirements.
