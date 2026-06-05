# Hook System

Flywheel hooks are optional deterministic enforcement points around workflow commands.

Hooks are different from skills:

- Skills guide agent behavior.
- Hooks enforce local invariants.

No hooks are enabled by default.

## Why Add A Hook?

Add a hook when a workflow rule should be enforced by a command, not remembered by a person or agent.

Good hook candidates:

- run workflow validation after state movement
- block cycle closure when QA evidence is missing
- block commits without an observer trace
- record extra audit data after observer closure
- call a local policy checker for sensitive actions

Do not add a hook for advice, style preferences, or exploratory process ideas. Put those in docs, prompts, or plugins first. Hooks should be boring, deterministic, and quick.

## What A Hook Does Today

Today, Flywheel can:

- validate hook configuration
- list configured hooks
- run configured hook commands for supported events
- pass event context through environment variables
- run `pre_state_move` and `post_state_move` around `flywheel_state.sh move`

Hooks are local shell commands. A required hook that exits non-zero fails the event.

## Quick Start

1. Add or choose a hook script under `flywheel/hooks/`.
2. Add it to `hooks.events` in `flywheel.yaml`.
3. Validate hook config.
4. Run the event normally.

Example config:

```yaml
hooks:
  path: "flywheel/hooks"
  events:
    post_state_move:
      - name: validate-after-state-move
        command: "./flywheel/hooks/examples/validate_after_state_move.sh"
        required: true
```

Validate:

```bash
./flywheel/tools/flywheel_hooks.sh doctor
./flywheel/tools/flywheel_hooks.sh list
```

## Location

Hook scripts live under `hooks.path` from `flywheel.yaml`.

Default:

```yaml
hooks:
  path: "flywheel/hooks"
```

## Events

Supported events:

- `pre_state_move`
- `post_state_move`
- `pre_cycle_close`
- `post_observer`
- `pre_commit`

`flywheel_state.sh move` runs `pre_state_move` before changing files and `post_state_move` after the transition is complete.

## Example Included In This Repo

Flywheel includes an example hook script at:

```text
flywheel/hooks/examples/validate_after_state_move.sh
```

It runs workflow-state validation after a state move. It is not enabled by default; copy the quick-start config above when you want to try it.

## Configuration

Hook entries may be command strings:

```yaml
hooks:
  events:
    pre_commit:
      - "./flywheel/hooks/pre_commit.sh"
```

Hook entries may also be mappings:

```yaml
hooks:
  events:
    pre_commit:
      - name: require-observer
        command: "./flywheel/hooks/require_observer.sh"
        required: true
```

If `required` is omitted, it defaults to `true`.

## Context

When a hook runs, Flywheel sets:

- `FLYWHEEL_HOOK_EVENT`
- `FLYWHEEL_HOOK_CONTEXT`

`FLYWHEEL_HOOK_CONTEXT` is a JSON object containing event-specific context.

For state moves, context includes:

- `domain`
- `from_lane`
- `to_lane`
- `source_path`
- `target_path` for post-state hooks
- `history_recorded` for post-state hooks
- `synced_readmes` for post-state hooks

## Commands

List configured hooks:

```bash
./flywheel/tools/flywheel_hooks.sh list
./flywheel/tools/flywheel_hooks.sh list --format json
```

Validate hook config:

```bash
./flywheel/tools/flywheel_hooks.sh doctor
./flywheel/tools/flywheel_hooks.sh doctor --format json
```

Run an event manually:

```bash
./flywheel/tools/flywheel_hooks.sh run pre_state_move --context '{"item":"STORY-example"}'
```

## Current Limits

The first hook implementation validates configuration and runs configured event commands. It does not yet:

- install hook scripts from plugins
- enforce plugin-declared hook permissions
- provide first-party hook scripts for cycle closure or commit checks
- serialize hook run records into observer traces
