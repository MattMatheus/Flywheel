# Evolution Roadmap

Flywheel should evolve as a small workflow kernel with optional extensions around it.

## Near-Term Tracks

Each track is intentionally at a first working slice. Later work should deepen these surfaces without making Flywheel core product-specific.

### Extension Kernel

Status: started.

Implemented:

- configurable `plugins.path`
- `flywheel_plugins.sh list`
- `flywheel_plugins.sh doctor`
- manifest validation
- doctor integration

Next candidates:

- dry-run materialization
- plugin patch preview
- plugin import/export helpers

### Deterministic Hooks

Status: started.

Hooks should enforce invariants around existing commands.

Candidate hooks:

- `pre_state_move`
- `post_state_move`
- `pre_cycle_close`
- `post_observer`
- `pre_commit`

Implemented:

- configurable `hooks.path`
- configurable `hooks.events`
- `flywheel_hooks.sh list`
- `flywheel_hooks.sh doctor`
- `flywheel_hooks.sh run`
- `pre_state_move` and `post_state_move` integration in `flywheel_state.sh move`

### Observer Experience Index

Status: started.

Observer JSON traces should eventually feed a small experience index.

Candidate outputs:

- `index.jsonl`
- `lessons.md`
- `stage-metrics.json`

Implemented:

- `flywheel_experience.sh index`
- `flywheel_experience.sh summarize`
- configurable `experience.path`
- generated `index.jsonl`, `stage-metrics.json`, and `lessons.md`

### Tool Ecosystem Projection

Status: started.

Flywheel should remain canonical while exporting compatible projections for tools such as Cursor, Codex, and Claude.

Implemented:

- `flywheel_export.sh plan cursor`
- `flywheel_export.sh plan codex`
- `flywheel_export.sh plan claude`
- `flywheel_export.sh plan all`
- JSON and text export planning
- no file writes in first implementation

### Lane Query API And TUI

Status: started.

The likely display path is a terminal UI. The first step is a stable lane query command:

```bash
./flywheel/tools/flywheel_lanes.sh --format json
```

The TUI should render state and call existing Flywheel commands for mutations. It should not own workflow state directly.

Implemented:

- `flywheel_lanes.sh`
- `flywheel_lanes.sh --format json`
- configured domain and lane reporting
- item metadata/frontmatter summaries
- README queue order support with filename fallback
