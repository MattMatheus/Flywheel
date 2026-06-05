# AGENTS

Agent operating guide for the Flywheel workflow harness.

## Mission
Execute work through the configured Flywheel stages without relying on product-specific assumptions.

## First 5 Minutes
1. Read `flywheel.yaml`.
2. Read `flywheel/HUMANS.md`.
3. Read `flywheel/DEVELOPMENT_CYCLE.md`.
4. Read `flywheel/tools/README.md` for the local command surface when needed.
5. Read `docs/README.md` when you need deeper reference documentation.
6. Read the stage prompt from `paths.prompts`.
7. Read the relevant role contract from `paths.roles` when role selection is enabled.
8. If `integrations.artifact_workflow.enabled` is `true`, read `flywheel/tools/artifact_workflow.sh <stage> --format json` for stage-specific artifact guidance.
9. Prefer `flywheel/tools/launch_stage.sh <stage> --format json` when you need machine-readable stage context.
10. Treat `flywheel/stage_contracts.yaml` as the editable machine-readable source for stage launch contracts.
11. Treat `flywheel/tools/flywheel_plugins.sh doctor --format json` as the machine-readable plugin validation gate.
12. Treat `flywheel/tools/flywheel_hooks.sh doctor --format json` as the machine-readable hook validation gate.

## Stage Prompts
Flywheel expects stage prompts for:
- planning
- architect
- engineering
- qa
- pm
- cycle

These should be resolved from `paths.prompts`.

## Mandatory Rules
- Respect `workflow.required_branch`.
- Use only the configured backlog and artifact paths.
- Respect explicit backlog state transitions.
- Do not fabricate work when the active lane is empty.
- Do not commit during intermediate stage transitions.
- Use one commit per completed cycle.
- Generate an observer artifact through `flywheel/tools/run_observer_cycle.sh` at cycle closure.
- Use `flywheel/tools/flywheel_state.sh move ...` for backlog lane movement when practical so frontmatter status, status metadata, transition history, and lane README queues stay synchronized.
- Treat QA as a gate, not a suggestion.
- Treat artifact readiness as explicit, not implied.
- Record evidence, risks, and next-state recommendation in stage handoffs.
- Treat `flywheel/tools/validate_workflow_state.sh` as the local consistency gate for backlog state before cycle closure or after workflow-state changes.
- Use `flywheel/tools/flywheel_lanes.sh --format json` when you need a machine-readable view of configured lanes.
- Use `flywheel/tools/flywheel_doctor.sh` for whole-harness health checks.
- Use `flywheel/tools/flywheel_plugins.sh doctor` after adding or changing optional plugins.
- Use `flywheel/tools/flywheel_hooks.sh doctor` after adding or changing optional hooks.
- Do not rely on plugin-provided skills, hooks, prompts, templates, or stage-contract patches unless their manifest validates.
- Do not bypass required hooks when they are configured for a workflow event.
- Use `flywheel/tools/flywheel_experience.sh index` after observer traces change when derived experience artifacts should stay current.
- Use `flywheel/tools/flywheel_export.sh plan <target>` before creating tool-specific context files.
- Treat the JSON trace written by `flywheel/tools/run_observer_cycle.sh` as the machine-readable observer artifact and the markdown report as the human-readable projection.
- Treat the artifact tool as an optional integration and use it only when the repo config enables it.
- When the artifact workflow integration is enabled, treat `flywheel/tools/artifact_workflow.sh --format json` as the canonical machine-readable source for stage entry and exit artifact guidance.
- Interpret the JSON output consistently:
  - `entry` commands help you discover or read the artifact inputs for the current stage.
  - `exit` commands help you write durable handoff or cycle-closure records after the stage work is complete.
- If you only need one phase, prefer `flywheel/tools/artifact_workflow_commands.sh --stage <stage> --phase <entry|exit>` to avoid reparsing the full JSON payload.
- Use the smallest useful action model:
  - `read`
  - `local write`
  - `risky write`
  - `sensitive or production`
- Require explicit human approval for `risky write` and `sensitive or production` actions.
- Record approval outcome when approval-governed work occurs.
- Use `flywheel/tools/flywheel_approval.sh record ...` when approval-governed work occurs.

## Required Sync
When workflow behavior changes, update together:
- `flywheel/HUMANS.md`
- `flywheel/AGENTS.md`
- `flywheel/DEVELOPMENT_CYCLE.md`
- relevant files under `docs/`
- the affected prompts
- the affected process docs
- any affected tool behavior
- plugin manifests or plugin-provided files when extension behavior changes
- hook configuration or hook scripts when enforcement behavior changes
- `flywheel/stage_contracts.yaml` when launch contract behavior changes

## Scope
Flywheel defines workflow behavior, not product strategy.

If a host repository needs product planning, release management, metrics, or additional governance, those should be layered on top of Flywheel rather than embedded into the core harness.
