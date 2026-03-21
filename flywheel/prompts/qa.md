# QA Prompt

Validate the top engineering story from the configured engineering QA lane.

## Purpose
- determine whether the story satisfies acceptance criteria
- detect regressions and quality gaps
- decide the next backlog state

## Required Inputs
- `flywheel.yaml`
- the story in `paths.engineering.qa`
- handoff artifacts from engineering
- QA rubric and state transition rules from `paths.process`
- role contract for QA work when `features.role_selection` is enabled

## Required Actions
1. Review the story against its acceptance criteria.
2. Review validation evidence and regression risk.
3. Treat missing or weak validation evidence as a blocking QA issue.
4. Review action and approval notes when risky work occurred.
5. File bugs using the configured bug template when defects are found.
6. Decide the result:
   - move to `paths.engineering.done` if the quality bar is met
   - move back to `paths.engineering.active` if blocking defects exist
7. Run observer for the completed cycle.
8. Create the cycle commit using `workflow.cycle_commit_format`.

## Required Output
- explicit pass/fail verdict
- evidence summary
- evidence quality call
- bug paths when defects are filed
- state transition decision

## Constraints
- no silent failures
- no reprioritization during QA
- treat missing validation evidence as a QA problem
