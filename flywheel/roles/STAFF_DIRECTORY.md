# Staff Directory

Canonical index of specialist roles for Flywheel role selection
(`features.role_selection`).

## What Roles Are For

Stage behavior — what to do in planning, architect, PM, engineering, QA, and
cycle — is fully defined by `flywheel/stage_contracts.yaml` and the stage
prompts. Roles do not restate it.

A role file exists only when it adds domain expertise a stage prompt lacks.
Consult one when the current work touches its domain, regardless of stage. A
role that merely rewords a stage prompt should be deleted, not maintained.

## Specialist Roles
- `SDET.md` — validation strategy, coverage design, automation priorities.
- `SRE.md` — reliability risk, observability, operational readiness.
- `Database Expert.md` — schema, integrity, migration, storage tradeoffs.
- `Technical Writer.md` — documentation accuracy and stale-content cleanup.

## Role File Schema
Each role file contains: `Mission`, `Scope`, `Inputs Required`,
`Outputs Required`, `Workflow Template`, `Quality Checklist`,
`Handoff Template`, `Constraints`.

## Role Boundary
Roles refine execution quality. The workflow contract remains defined by
`flywheel/stage_contracts.yaml`, the stage prompts, and the process docs.
