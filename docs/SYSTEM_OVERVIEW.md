# System Overview

Flywheel is a local workflow harness for human and agent delivery.

It is built around explicit queue movement, reviewable markdown artifacts, machine-readable launch context, and durable observer records. The harness should make it clear what work is ready, what stage owns it, what evidence exists, and what state transition is allowed next.

## Core Model

Flywheel separates workflow behavior into five surfaces:

- Config: `flywheel.yaml` defines host-repo paths and feature toggles.
- Contracts: `flywheel/stage_contracts.yaml` defines stage launch behavior.
- State: configured backlog lanes contain markdown work items.
- Tools: `flywheel/tools/` provides stable command entrypoints.
- Records: configured artifact paths hold planning notes, observer traces, approvals, and future release artifacts.

## Stages

Flywheel ships with these stages:

- Planning: turns goals, constraints, risks, and assumptions into intake artifacts.
- Architect: handles architecture decision work and follow-on implementation paths.
- PM: refines intake and maintains active queue order.
- Engineering: implements the top active engineering item and prepares QA handoff.
- QA: validates the item and moves it to `done` or back to `active`.
- Cycle: repeats engineering and QA until the active queue is drained or blocked.

## Lanes

Each supported domain has the same logical lanes:

- `intake`
- `ready`
- `active`
- `qa`
- `done`
- `blocked`
- `archive`

The default domains are:

- `engineering`
- `architecture`

Lane locations are configured in `flywheel.yaml`. Tools should resolve logical paths through config instead of assuming default directories.

## Source Of Truth

Markdown remains the human-reviewable source of truth. YAML frontmatter and structured sections provide enough machine-readable state for tools and agents.

Observer reports are written twice:

- markdown report for humans
- JSON sidecar for automation and future experience indexing

## Design Principles

- Make state movement explicit.
- Keep generated and human-authored artifacts reviewable.
- Prefer narrow tools with JSON output over prose-only instructions.
- Keep Flywheel generic; layer product-specific policy outside core.
- Treat plugins as declared extensions rather than edits to core files.

