# Flywheel Tool Commands

These commands are the stable local interface for humans and agents. Shell scripts are the command surface; Python modules in `flywheel/tools/lib/` own structured logic.

## Human Router

Use `./fw` from the repo root for common human workflows:

```bash
./fw doctor
./fw lanes
./fw launch engineering
./fw plugins doctor
./fw export plan all
```

`./fw commands` shows how each short command maps to the stable tool scripts below.

## Command Index

- `launch_stage.sh`: emit stage launch context.
- `validate_workflow_state.sh`: validate backlog and lane consistency.
- `flywheel_lanes.sh`: inspect configured lanes.
- `flywheel_state.sh`: move items between lanes.
- `run_observer_cycle.sh`: write observer markdown and JSON traces.
- `flywheel_experience.sh`: derive experience summaries from observer traces.
- `flywheel_export.sh`: plan tool-specific context projections.
- `flywheel_approval.sh`: record approval-governed work.
- `flywheel_doctor.sh`: run whole-harness health checks.
- `flywheel_plugins.sh`: list and validate plugins.
- `flywheel_hooks.sh`: list, validate, and run hooks.

## Stage Launch

```bash
./flywheel/tools/launch_stage.sh engineering
./flywheel/tools/launch_stage.sh engineering --format json
```

Use this to get stage context, selected work, lanes, checklist, exit gates, forbidden actions, and optional artifact workflow guidance.

## Workflow State Validation

```bash
./flywheel/tools/validate_workflow_state.sh
./flywheel/tools/validate_workflow_state.sh --format json
```

Use this after backlog state changes and before cycle closure.

## Lane Query

```bash
./flywheel/tools/flywheel_lanes.sh
./flywheel/tools/flywheel_lanes.sh --format json
```

Use this to inspect configured workflow lanes without mutating state. The JSON output is the stable data surface for future displays such as a TUI.

## State Movement

```bash
./flywheel/tools/flywheel_state.sh move STORY-20260524-example active qa --reason "engineering handoff ready"
./flywheel/tools/flywheel_state.sh move ARCH-20260524-example active qa --domain architecture --format json
```

Use this instead of manually moving backlog files when practical. It moves the file, updates YAML frontmatter status and markdown metadata status, appends transition history, and keeps the source and target lane README queue sections synchronized.

## Observer Closure

```bash
./flywheel/tools/run_observer_cycle.sh --cycle-id <cycle-id>
./flywheel/tools/run_observer_cycle.sh --cycle-id <cycle-id> --story <path> --format json
```

Writes a markdown observer report plus a structured JSON trace sidecar.

## Experience Index

```bash
./flywheel/tools/flywheel_experience.sh index
./flywheel/tools/flywheel_experience.sh index --format json
./flywheel/tools/flywheel_experience.sh summarize
./flywheel/tools/flywheel_experience.sh summarize --format json
```

Use this to derive a compact experience index from observer JSON traces. Generated artifacts are written under `experience.path`.

## Tool Exports

```bash
./flywheel/tools/flywheel_export.sh plan cursor
./flywheel/tools/flywheel_export.sh plan codex
./flywheel/tools/flywheel_export.sh plan claude
./flywheel/tools/flywheel_export.sh plan all --format json
```

Use this to plan tool-specific projections without writing files. Flywheel remains the canonical source of truth.

## Approval Records

```bash
./flywheel/tools/flywheel_approval.sh record --action-class risky-write --summary "<summary>" --approved-by "<name>"
./flywheel/tools/flywheel_approval.sh record --action-class sensitive-or-production --summary "<summary>" --approved-by "<name>" --scope "<scope>" --risks "<risks>"
```

Use this when work requires explicit approval.

## Harness Doctor

```bash
./flywheel/tools/flywheel_doctor.sh
./flywheel/tools/flywheel_doctor.sh --format json
```

Runs local harness health checks for required files, config loading, stage contracts, workflow state, plugins, hooks, docs, and command surfaces.

## Plugins

```bash
./flywheel/tools/flywheel_plugins.sh list
./flywheel/tools/flywheel_plugins.sh list --format json
./flywheel/tools/flywheel_plugins.sh doctor
./flywheel/tools/flywheel_plugins.sh doctor --format json
```

Use this to list optional Flywheel plugins and validate their manifests. Plugins live under the configured `plugins.path` directory and should declare their contributions and permissions instead of mutating core Flywheel files directly.

## Hooks

```bash
./flywheel/tools/flywheel_hooks.sh list
./flywheel/tools/flywheel_hooks.sh list --format json
./flywheel/tools/flywheel_hooks.sh doctor
./flywheel/tools/flywheel_hooks.sh doctor --format json
./flywheel/tools/flywheel_hooks.sh run pre_state_move --context '{"item":"STORY-example"}'
```

Use this to list, validate, and run optional deterministic hooks. Hooks live under the configured `hooks.path` directory and are configured under `hooks.events` in `flywheel.yaml`. State moves run `pre_state_move` and `post_state_move` hooks when configured.

## Artifact Workflow Integration

```bash
./flywheel/tools/artifact_workflow.sh engineering --format json
./flywheel/tools/artifact_workflow_commands.sh --stage engineering --phase entry
```

Only emits guidance when `integrations.artifact_workflow.enabled` is `true` in `flywheel.yaml`.
