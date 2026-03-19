# Flywheel Config Schema

`flywheel.yaml` defines the host-project interface for the Flywheel harness.

## Goals
- Keep the harness generic.
- Remove hardcoded product-specific repo layout.
- Support both greenfield repos and existing repos.

## Keys

### `version`
- Schema version for future migrations.
- First pass uses `1`.

### `workflow.required_branch`
- Branch that stage launchers require before they run.
- Replaces hardcoded branch assumptions like `dev`.

### `workflow.cycle_commit_format`
- Commit subject template for completed cycles.
- `{cycle_id}` is the only required placeholder in the first pass.

### `paths.prompts`
- Directory containing stage prompts.

### `paths.roles`
- Directory containing role/persona contracts.

### `paths.process`
- Directory containing workflow/process docs.

### `paths.templates`
- Directory containing reusable markdown templates.

### `paths.artifacts.*`
- Output locations for generated workflow artifacts.
- `planning`: planning notes created during planning stage.
- `observer`: observer reports created at cycle closure.
- `release`: optional release bundle location.

### `paths.engineering.*`
- Logical lane locations for engineering workflow state.
- Required lanes:
  - `intake`
  - `ready`
  - `active`
  - `qa`
  - `done`
  - `blocked`
  - `archive`

### `paths.architecture.*`
- Logical lane locations for architecture workflow state.
- Same required lanes as engineering.

### `templates.*`
- Template filenames resolved relative to `paths.templates`.
- First-pass required templates:
  - story
  - bug
  - architecture_story
  - observer_report

### `artifacts.*_pattern`
- Naming patterns for generated files.
- First-pass placeholders:
  - `{date}`
  - `{slug}`
  - `{cycle_id}`
  - `{release_id}`

### `features.*`
- Optional harness capabilities.
- `planning_notes`: whether planning writes a note artifact.
- `release_bundles`: whether release bundles are part of the workflow.
- `api_adapter`: whether launch/observer tools include policy/API adapter behavior.
- `role_selection`: whether prompts explicitly route through role contracts.

## First-Pass Constraints
- All configured paths should be repo-relative.
- Flywheel should not assume a product-specific top-level directory.
- Planning and PM remain first-class stages, but they must target configured artifact paths instead of project-specific research or roadmap directories.
- Observer remains part of the core harness.

## Implementation Guidance
- Tools should load `flywheel.yaml` before resolving any workflow paths.
- Prompts and entry docs should reference logical artifact types, not hardcoded repo folders, unless those paths are provided by config.
- If a feature is disabled, tools should degrade cleanly rather than require placeholder files.
