# Planning Prompt

Run an operator-guided planning cycle before architecture or implementation work begins.

## Purpose
- capture goals, constraints, risks, and assumptions
- create or refine intake artifacts
- recommend the next stage

## Required Inputs
- `flywheel.yaml`
- current backlog state from configured intake and active lanes
- current process docs from `paths.process`
- relevant role contracts from `paths.roles` when needed

## Required Actions
1. Clarify the problem, desired outcome, constraints, and success signals.
2. Write a planning note in `paths.artifacts.planning` when `features.planning_notes` is enabled.
3. Create engineering or architecture intake artifacts using the configured templates.
4. Ensure new intake items are specific, bounded, and testable.
5. Recommend the next stage:
   - `architect` for decision/design work
   - `pm` for refinement and queue placement
6. Do not implement production changes during planning.

## Required Output
- planning note or equivalent planning summary
- created intake artifact paths
- explicit next-stage recommendation
- key assumptions and risks

## Constraints
- keep planning separate from implementation
- do not create architecture work in engineering intake
- do not skip artifact creation when new work is identified

