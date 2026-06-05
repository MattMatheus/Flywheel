# Lane Query API

`flywheel_lanes.sh` provides a read-only view of configured Flywheel lanes.

It is the first stable display-oriented surface for future tools such as a terminal UI.

## Why Use It?

Use the lane query API when you need to inspect workflow state without launching a stage or mutating files.

Good uses:

- show current work across all domains
- feed a future TUI
- let an agent inspect queue state before choosing a stage
- verify lane item counts in automation
- debug queue ordering without moving items

Do not use it to validate correctness. It reports what exists. Use `validate_workflow_state.sh` to decide whether the state is consistent.

## Quick Start

Human-readable view:

```bash
./flywheel/tools/flywheel_lanes.sh
```

Machine-readable view:

```bash
./flywheel/tools/flywheel_lanes.sh --format json
```

Expected empty-harness text output:

```text
engineering
  intake (0)
  ready (0)
  active (0)
  qa (0)
  done (0)
  blocked (0)
  archive (0)
architecture
  intake (0)
  ready (0)
  active (0)
  qa (0)
  done (0)
  blocked (0)
  archive (0)
```

## Commands

Text output:

```bash
./flywheel/tools/flywheel_lanes.sh
```

JSON output:

```bash
./flywheel/tools/flywheel_lanes.sh --format json
```

## Behavior

The command reads lane locations from `flywheel.yaml`.

For each configured domain and lane, it reports:

- lane name
- lane path
- whether the lane directory exists
- item count
- ordered items

For each item, it reports:

- order
- path
- filename
- id
- kind
- status
- ready value
- title
- markdown metadata
- YAML frontmatter

## Ordering

When a lane README contains numbered queue entries, that order is used first.

Any markdown item not listed in the lane README is appended in filename order. This mirrors the current launch behavior, where explicit queue order is preferred but file presence remains visible.

## Scope

The lane query command does not validate or mutate state.

Use `validate_workflow_state.sh` to validate consistency and `flywheel_state.sh move` to mutate lane state.

## Example Workflow

1. Inspect lanes:

```bash
./flywheel/tools/flywheel_lanes.sh
```

2. If items exist and you need consistency checks:

```bash
./flywheel/tools/validate_workflow_state.sh
```

3. If a workflow item should move:

```bash
./flywheel/tools/flywheel_state.sh move <item> <from-lane> <to-lane> --reason "<reason>"
```

## TUI Path

A future TUI should consume `flywheel_lanes.sh --format json` for display and call existing Flywheel commands for mutations. The TUI should not own workflow state directly.
