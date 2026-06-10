# HUMANS

Operator guide for the Flywheel workflow harness.

## Purpose
Flywheel provides a staged workflow for planning, architecture, implementation,
QA, PM refinement, and cycle closure. The harness does not require a
product-specific repo layout; all locations come from `flywheel.yaml`.

## Daily Driver
```bash
./fw status               # branch, lane counts, top stories, state check
./fw launch <stage>       # stage contract and selected story
./fw move <item> <a> <b>  # explicit lane movement, history preserved
./fw close-cycle ...      # validate + observer + experience + cycle commit
./fw doctor               # whole-harness health check
```

Stages: `planning`, `architect`, `pm`, `engineering`, `qa`, `cycle`.
Stage behavior is defined in `flywheel/stage_contracts.yaml`; the prompts in
`flywheel/prompts/` add judgment guidance per stage.

When delegating to an agent, point it at the root `AGENTS.md` (Claude reads the
same content via the `CLAUDE.md` symlink). Per-stage slash commands live in
`.claude/commands/`.

## Core Rules
- Work on `workflow.required_branch`; state moves and cycle closure abort
  elsewhere.
- Do not invent work when the active queue is empty.
- Use explicit backlog state transitions via `./fw move` so file location,
  metadata, transition history, and lane README queues stay synchronized.
- QA is a gate: no `active` to `done` shortcuts.
- One commit per completed cycle, created at closure (`./fw close-cycle`),
  never during intermediate transitions.
- Risky or sensitive actions require explicit approval; record outcomes with
  `./fw approval record ...`.
- Validate plugins and hooks (`./fw plugins doctor`, `./fw hooks doctor`)
  before relying on their behavior.

## Config-Owned Surfaces
`flywheel.yaml` owns: prompt, role, process, and template directories; planning
and observer artifact directories; plugin and hook locations; engineering and
architecture lanes. `flywheel/stage_contracts.yaml` owns stage launch behavior.

Examples live under `flywheel/examples/` and are not active work.

## Changing The Workflow
Edit `flywheel/stage_contracts.yaml` for stage behavior and the affected prompt
for judgment guidance. Update the entry docs and `docs/` only when the
operator-facing workflow changes. Run `./fw doc-test` after doc or tool
changes.
