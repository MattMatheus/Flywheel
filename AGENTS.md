# Flywheel Agent Entry Point

This repo is a staged workflow harness. Work moves through explicit backlog
lanes (`intake -> ready -> active -> qa -> done`), every stage has a
machine-readable contract, and each completed cycle closes with an observer
record and one commit.

This file is the canonical, model-agnostic agent entry point. `CLAUDE.md` is a
symlink to it and must never diverge (`./fw doctor` enforces this).

## Start Here

```bash
./fw status                              # branch, lane counts, top stories, state check
./fw launch <stage> --format json        # authoritative stage contract + selected story
```

`launch` returns the stage prompt path, the selected story, the checklist, the
exit gate, and forbidden actions. That JSON is the contract; the prompt file it
points at carries stage-specific judgment guidance. Stages: `planning`,
`architect`, `pm`, `engineering`, `qa`, `cycle`.

## Non-Negotiable Rules

1. Stay on `workflow.required_branch` (see `flywheel.yaml`). Mutating commands abort elsewhere.
2. Resolve all paths through `flywheel.yaml`; never assume directory layout.
3. Move backlog items only with `./fw move <item> <from> <to>` so metadata, history, and lane READMEs stay synchronized.
4. Never move work directly from `active` to `done`; QA is a gate.
5. If the active lane is empty, report `no stories` — do not invent work.
6. Close a completed cycle with `./fw close-cycle --cycle-id <id>` (validates state, writes the observer record, refreshes the experience index, creates the single cycle commit).
7. Risky or sensitive actions (anything beyond local writes) need explicit human approval; record it with `./fw approval record ...`.

## Deeper Reference

- `flywheel/AGENTS.md` — full agent operating guide.
- `flywheel/DEVELOPMENT_CYCLE.md` — workflow contract for humans.
- `flywheel/stage_contracts.yaml` — single source of truth for stage behavior.
- `docs/README.md` — system reference documentation.
