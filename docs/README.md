# Flywheel Documentation

This directory contains the maintained reference documentation for the Flywheel harness.

The root-level guides are intentionally short:

- `AGENTS.md` (repo root) is the canonical, model-agnostic agent entry point;
  `CLAUDE.md` is a symlink that tracks it (`./fw doctor` enforces the sync).
- `flywheel/README.md` is the quick-start overview.
- `flywheel/HUMANS.md` is the operator guide.
- `flywheel/AGENTS.md` is the full agent operating guide.
- `flywheel/DEVELOPMENT_CYCLE.md` is the concise workflow contract.
- `flywheel/stage_contracts.yaml` is the single source of truth for stage
  checklists, exit gates, and forbidden actions.

The docs here provide the deeper system explanation.

## Reference

- [System Overview](SYSTEM_OVERVIEW.md)
- [Architecture](ARCHITECTURE.md)
- [Operations Guide](OPERATIONS.md)
- [Configuration Reference](CONFIGURATION.md)
- [Plugin System](PLUGINS.md)
- [Hook System](HOOKS.md)
- [Lane Query API](LANES.md)
- [Experience Index](EXPERIENCE.md)
- [Tool Ecosystem Projection](EXPORTS.md)
- [Evolution Roadmap](EVOLUTION.md)

## Examples

Concrete examples live beside the feature they demonstrate:

- `flywheel/plugins/review-gates/`: minimal plugin example.
- `flywheel/hooks/examples/validate_after_state_move.sh`: post-state-move validation hook (wired by default).
- `./fw demo`: seeds a sample story into engineering intake for a lifecycle walkthrough.

## Human CLI

Use `./fw help` from the repo root for the human-facing command router. The individual scripts under `flywheel/tools/` remain the stable low-level command surface.

## Maintenance Rule

Stage behavior changes happen in `flywheel/stage_contracts.yaml` and the
affected stage prompt. Update the entry docs under `flywheel/` and the
relevant reference page here only when the operator-facing workflow changes.
