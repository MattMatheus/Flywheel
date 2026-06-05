# Flywheel Documentation

This directory contains the maintained reference documentation for the Flywheel harness.

The root-level guides are intentionally short:

- `flywheel/README.md` is the quick-start overview.
- `flywheel/HUMANS.md` is the operator guide.
- `flywheel/AGENTS.md` is the agent operating guide.
- `flywheel/DEVELOPMENT_CYCLE.md` is the concise workflow contract.

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
- `flywheel/hooks/examples/validate_after_state_move.sh`: optional post-state-move hook example.

## Human CLI

Use `./fw help` from the repo root for the human-facing command router. The individual scripts under `flywheel/tools/` remain the stable low-level command surface.

## Maintenance Rule

When workflow behavior changes, update the concise entry docs under `flywheel/` and the relevant reference page here in the same change.
