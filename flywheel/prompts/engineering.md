# Engineering Prompt

Execute the top engineering story from the configured engineering active lane.

## Purpose
- implement the requested change
- update validation coverage
- prepare a QA-ready handoff

## Required Inputs
- `flywheel.yaml`
- the top story in `paths.engineering.active`
- process docs from `paths.process`
- role contract for engineering work when `features.role_selection` is enabled

## Required Actions
1. Read and restate the selected story.
2. Implement the required change.
3. Update tests for touched behavior.
4. Run the required verification commands for the change.
5. Prepare a handoff package with change summary, validation results, and open risks.
6. Move the story to the configured engineering QA lane.
7. Do not create the cycle commit yet.

## Required Output
- changed implementation
- updated validation coverage
- handoff package
- explicit QA focus areas
- new intake items for discovered gaps, when required

## Constraints
- do not fabricate work when the active queue is empty
- do not move work directly from active to done
- do not skip validation
- keep discovered gaps separate from the current story when they are out of scope

