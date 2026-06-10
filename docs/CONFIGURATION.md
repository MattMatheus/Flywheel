# Configuration Reference

`flywheel.yaml` is the host-repo interface for the harness.

## Required Sections

### `version`

Schema version for future migrations.

### `workflow`

Controls branch and commit expectations.

```yaml
workflow:
  required_branch: main
  cycle_commit_format: "cycle-{cycle_id}"
```

### `paths`

Defines prompt, role, process, template, artifact, and lane locations.

All configured paths should be repo-relative.

### `templates`

Maps logical template names to filenames under `paths.templates`.

### `artifacts`

Defines naming patterns for generated artifacts.

Supported placeholders depend on the artifact type. Current common placeholders include:

- `{date}`
- `{slug}`
- `{cycle_id}`
- `{release_id}`

### `features`

Enables or disables optional harness features.

```yaml
features:
  planning_notes: true
  release_bundles: false
  api_adapter: false
  role_selection: true
```

### `plugins`

Defines optional plugin location.

```yaml
plugins:
  path: "flywheel/plugins"
```

If omitted, tools default to `flywheel/plugins`.

### `hooks`

Defines optional deterministic hook locations and event bindings.

```yaml
hooks:
  path: "flywheel/hooks"
  events:
    pre_state_move: []
    post_state_move:
      - name: validate-workflow-state
        command: "flywheel/hooks/examples/validate_after_state_move.sh"
        required: true
    pre_cycle_close: []
    post_observer: []
    pre_commit: []
```

The `post_state_move` validation hook ships enabled so every lane move is
followed by workflow state validation.

Hook entries may be command strings:

```yaml
hooks:
  events:
    pre_commit:
      - "./flywheel/hooks/pre_commit.sh"
```

Or mappings:

```yaml
hooks:
  events:
    pre_commit:
      - name: require-observer
        command: "./flywheel/hooks/require_observer.sh"
        required: true
```

### `experience`

Defines where derived experience artifacts are written.

```yaml
experience:
  path: "flywheel/artifacts/experience"
```

If omitted, tools default to `flywheel/artifacts/experience`.

### `integrations`

Defines optional external integrations.

```yaml
integrations:
  artifact_workflow:
    enabled: false
    command: ""
```

## Config Rules

- Tools should load `flywheel.yaml` before resolving workflow paths.
- Prompts and docs should refer to logical locations unless concrete config paths are needed.
- Optional features should degrade cleanly when disabled.
- JSON output should be preferred when commands are consumed by automation.
