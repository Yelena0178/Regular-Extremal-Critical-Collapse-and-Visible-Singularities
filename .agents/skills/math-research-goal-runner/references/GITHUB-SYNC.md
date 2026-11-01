# Authorized synchronization after each research round

Apply when the user has authorized ongoing per-round GitHub synchronization. A request to sync every round authorizes the necessary scoped commits and pushes to the confirmed research destination; do not request that permission again each round. This skill alone grants no publication authority. A current read-only/no-push instruction takes precedence, and a one-off historical push is not standing permission.

## Resolve and retain the destination

At first use, map the active research project to its local repository, verified GitHub remote owner/repository, existing branch, upstream configuration and authorization source. Check fetch and push destinations; multiple push URLs or a mismatched project need resolution. Prefer the existing research branch, not a default main branch chosen for convenience. Inspect explicit branch configuration and remote refs if local upstream tracking is absent. Reuse an unambiguous existing mapping without asking again.

If no corresponding repository/branch can be identified, ask one focused question and continue local research. Do not invent/create a remote, repository or branch, change credentials, force-push, merge a PR, or publish unrelated content under a per-round sync instruction. Never redirect to another project's repository after a failure.

## Round-end transaction

At every completed research round, including negative findings and strategic reviews, and before a runtime handoff with new work:

1. Save the actual research delta: arguments, code, admissible data/evidence, failed attempts, audit limitations, strategic-review receipt, current state and next executable action. Preserve raw evidence according to the project's data policy; when it cannot be stored in Git, record its legitimate storage pointer and reproducible derivation, and report any unavailable artifact. Reuse the existing records and update required navigation/manifests.
2. Inspect worktree/index and capture the precommit HEAD. Select an explicit path list belonging to this round; exclude unrelated edits, credentials, temporary outputs and data outside the publication scope. Do not use blanket staging. Preserve existing staged work; when an unrelated staged file prevents a scoped commit, isolate this round's index or record pending sync rather than including or discarding it.
3. Run the narrow checks appropriate to the changed artifacts, including project-required integrity checks. A negative scientific result is publishable with an accurate scope; a corrupt receipt, unexplained validation failure or falsely upgraded conclusion must be repaired or clearly excluded. Do not require proof of the entire research goal before archiving a valid intermediate result.
4. Review the exact staged change and commit only this round's material, using a message that identifies the research result/review without claiming unearned success. If there is no new delta and the previous commit is remotely confirmed, do not create an empty commit or a receipt-only commit loop. If an earlier push is pending, retry that existing commit instead.
5. Check the confirmed remote branch and push the saved commit with an explicit destination ref. Remote changes require a scoped integration review; follow repository rules, preserve both sides and do not overwrite concurrent work. A conflict or unclear ownership is pending sync, not permission to force or rewrite history.
6. Verify the remote ref after the push. Success requires the saved local commit to be present on the intended remote branch: equal tips, or verified ancestry if another authorized commit arrived concurrently. Record repository/branch, round, local commit, observed remote commit, verification time and outcome. If remote verification cannot run, report unverified rather than synchronized.

Record the current commit receipt in the final message or an external operational log, then carry it into the next research checkpoint. A tracked checkpoint can include the prior confirmed receipt and the current precommit identity; it cannot contain its own final commit hash. Do not create endless commits just to embed the newest receipt.

## Failure and retry

Keep local results and any completed commit when network/authentication/push/verification fails. Classify the failure and save destination, pending round/commit, concise error and next retry action. Retry at most twice in the current round for an apparently transient error, with a short bounded backoff; do not repeatedly retry unchanged authentication failures, conflicts or rejected publication. Resume pending work at the next round or after the relevant condition changes, without duplicate commits. Do not use a different transport to bypass an explicit denial.

Pending GitHub sync does not erase scientific progress or authorize abandonment of independently feasible research. Surface the missing user action once if needed and keep the backlog visible; if remote availability is itself necessary for the next research step, explain that dependency. Final status distinguishes locally saved, committed/push pending, pushed/verification pending, and remotely confirmed.

This is an active research-loop operation, not a background scheduler. If the user separately requests monitoring or retries while no research run is active, use an authorized host automation with an explicit target/cadence; do not simulate it in these instructions.
