# AGENTS

Agent operating guide for the Flywheel workflow harness. The root `AGENTS.md`
is the short entry point; this file is the full reference.

## Operating Loop
1. `./fw status` — branch, lane counts, top stories, state validation.
2. `./fw launch <stage> --format json` — the authoritative stage contract:
   prompt path, selected story, checklist, exit gate, forbidden actions.
3. Read the stage prompt the launch payload points at; it carries the judgment
   guidance the contract cannot express.
4. Do the stage work. Move items only with `./fw move <item> <from> <to>`.
5. Close completed cycles with `./fw close-cycle --cycle-id <id> --story <path>`.

Stage behavior is defined once, in `flywheel/stage_contracts.yaml`. Prompts,
docs, and tools defer to it. If the launch payload includes an
`artifact_workflow` block (optional integration), use its `entry` commands to
discover stage inputs and its `exit` commands to write durable handoff records.

## Mandatory Rules
- Respect `workflow.required_branch`; mutating commands abort elsewhere.
- Resolve every path through `flywheel.yaml`; never assume directory layout.
- Respect explicit backlog state transitions; QA is a gate, and work never
  jumps from `active` to `done`.
- Do not fabricate work when the active lane is empty — report `no stories`.
- One commit per completed cycle, none during intermediate transitions.
- Record evidence, risks, and next-state recommendation in stage handoffs
  (see `flywheel/process/HANDOFF_EXPECTATIONS.md`).
- Use the smallest useful action model — `read`, `local write`, `risky write`,
  `sensitive or production` — and get explicit human approval before the last
  two. Record outcomes with `./fw approval record ...`.
- Do not rely on plugin- or hook-provided behavior unless `./fw plugins doctor`
  and `./fw hooks doctor` pass; never bypass hooks configured for an event.
- Consult a specialist role from `paths.roles` (see `STAFF_DIRECTORY.md`) when
  the work touches its domain and `features.role_selection` is enabled.

## Tool Surface
`./fw help` lists the command router. The scripts under `flywheel/tools/` are
the stable low-level surface; prefer `--format json` variants when you need
machine-readable output. `./fw doctor` is the whole-harness health gate;
`./fw validate` is the backlog consistency gate.

## Required Sync
When workflow behavior changes, update together:
- `flywheel/stage_contracts.yaml` (the behavior itself)
- the affected stage prompt (judgment guidance)
- entry docs (`AGENTS.md`, `flywheel/HUMANS.md`, `flywheel/DEVELOPMENT_CYCLE.md`)
  and `docs/` pages only when the operator-facing workflow changes

## Scope
Flywheel defines workflow behavior, not product strategy. Product planning,
release management, metrics, and extra governance belong in layers on top of
the harness, not in its core.
