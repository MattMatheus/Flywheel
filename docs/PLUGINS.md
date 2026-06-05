# Plugin System

Flywheel plugins are optional extensions to the harness.

The plugin system is intentionally conservative. A plugin can declare contributions and permissions, but core Flywheel behavior should not rely on a plugin unless its manifest validates.

## Why Add A Plugin?

Add a plugin when you have reusable workflow behavior that should travel as a named bundle instead of being baked directly into Flywheel core.

Good plugin candidates:

- review checklists for a specific quality bar
- project-specific stage prompts
- optional hook scripts
- templates for a recurring artifact type
- tool-specific export material
- team-specific skills or operating rules

Plugins help keep Flywheel generic. Core stays small, while optional behavior is grouped, named, documented, and validated.

Do not add a plugin for one-off project work, a single backlog item, or behavior every Flywheel installation should always have. Put those in backlog items, docs, or core harness files instead.

## What A Plugin Does Today

Today, a plugin is a validated declaration.

Flywheel can:

- discover plugin directories
- validate `flywheel-plugin.yaml`
- report contributed files
- report declared permissions
- include plugin validation in `flywheel_doctor.sh`

Flywheel does not yet automatically install, apply, run, or materialize plugin contributions. That is intentional for the first version: plugins establish a safe extension boundary before they become executable machinery.

## Quick Start

Create a plugin directory under `plugins.path`:

```bash
mkdir -p flywheel/plugins/review-gates/skills
```

Add `flywheel/plugins/review-gates/flywheel-plugin.yaml`:

```yaml
name: review-gates
description: Adds reusable review guidance for QA and engineering handoffs.
version: 0.1.0
publisher: local
source: ""
sha256: ""
contributions:
  skills: skills
permissions:
  shell: false
  network: false
  writes: []
```

Add a contributed file, such as `flywheel/plugins/review-gates/skills/review-gates.md`.

Validate:

```bash
./flywheel/tools/flywheel_plugins.sh doctor
./flywheel/tools/flywheel_plugins.sh list
```

If validation passes, the plugin is now visible to Flywheel as a declared extension. Operators and future tooling can decide how to use its contributions.

## Location

Plugins live under `plugins.path` from `flywheel.yaml`.

Default:

```yaml
plugins:
  path: "flywheel/plugins"
```

Each plugin lives in its own directory:

```text
flywheel/plugins/<plugin-name>/
  flywheel-plugin.yaml
  README.md
  skills/
  hooks/
  prompts/
  templates/
  stage_contract_patches.yaml
```

Only `flywheel-plugin.yaml` is required for a plugin directory to validate as a plugin. `README.md` is recommended.

## Example Included In This Repo

Flywheel includes an example plugin at:

```text
flywheel/plugins/review-gates/
```

It demonstrates the smallest useful plugin shape: a manifest, README, and a contributed skill document.

## Manifest

Example:

```yaml
name: review-gates
description: Adds review-focused skills and future QA gate hooks.
version: 0.1.0
publisher: local
source: ""
sha256: ""
contributions:
  skills: skills
  hooks: hooks
  prompts: prompts
  templates: templates
  stage_contract_patches: stage_contract_patches.yaml
permissions:
  shell: false
  network: false
  writes:
    - flywheel/artifacts/**
```

## Required Fields

- `name`: must match the plugin directory name.
- `description`: short human-readable description.
- `version`: plugin version.

## Optional Metadata

- `publisher`
- `source`
- `sha256`

These fields support provenance and future supply-chain checks.

## Contributions

Supported contribution keys:

- `skills`
- `hooks`
- `prompts`
- `templates`
- `stage_contract_patches`

Each contribution value may be a string path or a list of string paths. Paths must stay inside the plugin directory.

## Permissions

Supported permission keys:

- `shell`: whether the plugin expects shell execution.
- `network`: whether the plugin expects network access.
- `writes`: path globs the plugin expects to write.

Permissions are declarations. Future hook and materialization tooling can use them for stronger enforcement.

## Commands

List installed plugins:

```bash
./flywheel/tools/flywheel_plugins.sh list
./flywheel/tools/flywheel_plugins.sh list --format json
```

Validate installed plugins:

```bash
./flywheel/tools/flywheel_plugins.sh doctor
./flywheel/tools/flywheel_plugins.sh doctor --format json
```

`flywheel_doctor.sh` also runs plugin validation.

## Current Limits

The first plugin implementation validates manifests and reports contributions. It does not yet:

- materialize plugin files into tool-specific locations
- apply stage-contract patches
- run plugin hooks
- install plugins from remote sources
- enforce declared permissions

These capabilities should be added incrementally.
