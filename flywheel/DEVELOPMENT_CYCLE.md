# Development Cycle

Flywheel runs a staged workflow with explicit queue movement and cycle closure.

## Canonical Flow
1. Planning creates or refines intake work.
2. Architect processes architecture decision work when needed.
3. PM maintains clear, ordered active queues.
4. Engineering executes the top active implementation story.
5. QA validates the story and decides `done` or return to `active`.
6. Cycle closure validates workflow state, writes the observer record
   (markdown plus JSON trace), and creates the single cycle commit
   (`./fw close-cycle`).

Per-stage checklists, exit gates, and forbidden actions are defined once in
`flywheel/stage_contracts.yaml` and surfaced by `./fw launch <stage>`. Stage
prompts in `flywheel/prompts/` add judgment guidance.

## Invariants
- Required branch and commit format come from `workflow.*` in `flywheel.yaml`;
  see `flywheel/process/BRANCH_AND_COMMIT_INVARIANTS.md`.
- All workflow locations are resolved from `flywheel.yaml`.
- Backlog movement uses `./fw move` so lane placement, metadata status,
  transition history, and lane README queues update together; configured
  `post_state_move` hooks run automatically.
- Backlog state must pass `./fw validate` before cycle closure.
- Observer is part of cycle closure, not optional cleanup; the JSON trace is
  the machine-readable artifact, the markdown report the human projection.
- Artifact readiness must be explicit before promotion.
- Risky or sensitive actions require explicit approval and a recorded outcome
  (`./fw approval record ...`).
- Plugins and hooks are optional, validated extensions
  (`./fw plugins doctor`, `./fw hooks doctor`).
- The artifact workflow integration is optional; when enabled in config, its
  guidance appears in the `./fw launch` payload.

## Empty Queue Rule
If the configured engineering active lane is empty, report `no stories` and
route work toward planning or PM refinement instead of inventing execution
work.

## Examples
Lifecycle examples live under `flywheel/examples/`. They are not active backlog
state and should not be moved through lanes unless copied into intake as real
work.
