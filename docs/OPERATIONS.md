# Operations Guide

This guide describes how to operate Flywheel in a local repository.

## Before Work Starts

1. Read `flywheel.yaml`.
2. Confirm the current branch matches `workflow.required_branch`.
3. Run `./fw doctor`.
4. Select the stage.
5. Launch the stage with `./fw launch <stage>`.

Use JSON output when another tool or agent will consume the result:

```bash
./flywheel/tools/launch_stage.sh engineering --format json
```

## During Work

Use configured paths only. Do not assume default backlog or artifact directories when `flywheel.yaml` remaps them.

When moving work between lanes, prefer:

```bash
./flywheel/tools/flywheel_state.sh move <item> <from-lane> <to-lane> --reason "<reason>"
```

Run validation after queue or metadata changes:

```bash
./flywheel/tools/validate_workflow_state.sh
```

Inspect lane state without changing it:

```bash
./fw lanes
```

## Cycle Closure

At the end of a completed cycle:

1. Ensure QA verdict and validation evidence are recorded.
2. Validate workflow state.
3. Write observer artifacts.
4. Commit once using `workflow.cycle_commit_format`.

Observer command:

```bash
./flywheel/tools/run_observer_cycle.sh --cycle-id <cycle-id>
```

Refresh derived experience artifacts when observer traces change:

```bash
./flywheel/tools/flywheel_experience.sh index
```

Experience artifacts are derived from observer JSON traces. They can be regenerated from the current observer artifact directory.

## Approvals

Flywheel uses a small action model:

- `read`
- `local write`
- `risky write`
- `sensitive or production`

Risky or sensitive actions require explicit human approval and a durable record.

```bash
./flywheel/tools/flywheel_approval.sh record \
  --action-class risky-write \
  --summary "<summary>" \
  --approved-by "<name>"
```

## Empty Queues

If the active queue is empty, do not invent work. Route toward Planning or PM refinement.

## Optional Integrations

The artifact workflow integration is disabled by default. When enabled in `flywheel.yaml`, stage launch and observer commands surface artifact-tool guidance.

Plugins are also optional. Validate them before use:

```bash
./flywheel/tools/flywheel_plugins.sh doctor
```

Hooks are optional deterministic enforcement points. Validate them after changes:

```bash
./flywheel/tools/flywheel_hooks.sh doctor
```

Plan tool-specific context exports without writing files:

```bash
./fw export plan all
```
