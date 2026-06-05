# Flywheel Hooks

Optional hook scripts can live here.

Hooks are configured in `flywheel.yaml` under `hooks.events`. They are intended for deterministic workflow enforcement around Flywheel commands.

No hooks are enabled by default.

Use hooks when a workflow rule should be enforced by command execution.

Examples:

- validate workflow state after moving an item
- block cycle closure without QA evidence
- block commits without observer traces

See `examples/validate_after_state_move.sh` for a safe example hook.
