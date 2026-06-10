# Branch And Commit Invariants

- `workflow.required_branch` is the only branch where workflow state may change.
- Stage launch is read-only: it warns on a branch mismatch but still emits context.
- State moves (`./fw move`) and cycle closure (`./fw close-cycle`) abort on a branch mismatch.
- `./fw doctor` fails when the active branch does not match `workflow.required_branch`.
- Intermediate stage transitions do not create commits.
- Each completed cycle creates exactly one commit.
- Cycle commit format is controlled by `workflow.cycle_commit_format`.
- Observer output belongs to the same cycle closure as the final commit.
