# Architecture

Flywheel is organized as a small workflow kernel with stable command-line entrypoints and editable markdown/YAML contracts.

## Directory Map

```text
flywheel/
  AGENTS.md
  CONFIG_SCHEMA.md
  DEVELOPMENT_CYCLE.md
  HUMANS.md
  README.md
  artifacts/
  backlog/
  docs/
  examples/
  plugins/
  process/
  prompts/
  roles/
  templates/
  tools/
    lib/
  stage_contracts.yaml
```

## Command Surface

Shell scripts under `flywheel/tools/` are the stable interface for humans and agents.

Python modules under `flywheel/tools/lib/` own structured parsing, validation, and mutation logic.

This split keeps commands easy to discover while allowing implementation details to evolve.

## Important Commands

```bash
./flywheel/tools/launch_stage.sh engineering --format json
./flywheel/tools/flywheel_state.sh move STORY-... active qa --reason "handoff ready"
./flywheel/tools/validate_workflow_state.sh --format json
./flywheel/tools/flywheel_lanes.sh --format json
./flywheel/tools/run_observer_cycle.sh --cycle-id <cycle-id> --format json
./flywheel/tools/flywheel_experience.sh index --format json
./flywheel/tools/flywheel_export.sh plan all --format json
./flywheel/tools/flywheel_approval.sh record --action-class risky-write --summary "<summary>" --approved-by "<name>"
./flywheel/tools/flywheel_plugins.sh doctor --format json
./flywheel/tools/flywheel_doctor.sh --format json
```

## Stage Contracts

`flywheel/stage_contracts.yaml` defines:

- prompt file
- cycle label
- input lane
- output lane
- checklist
- exit gate
- forbidden actions

`launch_stage.sh` reads this file and emits either text or JSON launch context.

## State Movement

`flywheel_state.sh move` should be used when practical. It updates related state together:

- moves the markdown item between lane directories
- updates metadata status
- updates YAML frontmatter status when present
- appends transition history
- synchronizes lane README queue sections

Manual file movement should be followed by `validate_workflow_state.sh`.

## Validation Layers

Flywheel has several validation layers:

- intake validation for new items
- workflow-state validation for lane consistency
- plugin manifest validation for optional extensions
- hook validation for optional enforcement points
- experience indexing for observer trace summaries
- doctor checks for whole-harness health
- doc tests for required files, directories, and command gates

## Extension Boundary

Core Flywheel behavior should stay generic. Optional behavior belongs in plugins, integrations, or host-repo policy layered above the harness.
