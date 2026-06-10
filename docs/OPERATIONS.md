# Operations Guide

This guide describes how to operate Flywheel in a local repository.

## Before Work Starts

1. Run `./fw status` — it reports the branch against `workflow.required_branch`, workflow state, lane counts, and the next active story.
2. Run `./fw doctor` when checking overall harness health.
3. Select the stage.
4. Launch the stage with `./fw launch <stage>`.

On a fresh harness with an empty backlog, `./fw demo` seeds a sample story so
the full lifecycle can be exercised end to end.

Use JSON output when another tool or agent will consume the result:

```bash
./flywheel/tools/launch_stage.sh engineering --format json
```

## During Work

Use configured paths only. Do not assume default backlog or artifact directories when `flywheel.yaml` remaps them.

When moving work between lanes, prefer:

```bash
./fw move <item> <from-lane> <to-lane> --reason "<reason>"
```

The move tool keeps the item file, frontmatter status, transition history,
lane README queues, and the root backlog summary synchronized, and the default
`post_state_move` hook validates workflow state after every move. Run
validation manually after other metadata changes:

```bash
./fw validate
```

Inspect lane state without changing it:

```bash
./fw lanes
```

## Cycle Closure

Ensure the QA verdict and validation evidence are recorded on the story, then
close the cycle in one step:

```bash
./fw close-cycle --cycle-id <cycle-id> --story <path>
```

This validates workflow state, writes the observer report and JSON trace,
refreshes the derived experience artifacts, and creates the single cycle
commit using `workflow.cycle_commit_format`. The individual tools
(`run_observer_cycle.sh`, `flywheel_experience.sh index`) remain available
when a step needs to run alone.

## Approvals

Flywheel uses a small action model:

- `read`
- `local write`
- `risky write`
- `sensitive or production`

Risky or sensitive actions require explicit human approval and a durable record.

```bash
./flywheel/tools/flywheel_approval.sh record \
  --action-class risky-write \
  --summary "<summary>" \
  --approved-by "<name>"
```

## Empty Queues

If the active queue is empty, do not invent work. Route toward Planning or PM refinement.

## Optional Integrations

The artifact workflow integration is disabled by default. When enabled in `flywheel.yaml`, stage launch and observer commands surface artifact-tool guidance.

Plugins are also optional. Validate them before use:

```bash
./flywheel/tools/flywheel_plugins.sh doctor
```

Hooks are deterministic enforcement points. A default `post_state_move` hook
validates workflow state after every lane move. Validate hook config after
changes:

```bash
./flywheel/tools/flywheel_hooks.sh doctor
```

Plan tool-specific context exports:

```bash
./fw export plan all
```

The agent-context projections are maintained in-repo: the root `AGENTS.md` is
the canonical model-agnostic agent entry point, `CLAUDE.md` is a symlink that
tracks it (enforced by `./fw doctor`), and `.claude/commands/` holds thin
per-stage slash commands that delegate to `./fw launch`.
