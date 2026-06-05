# Tool Ecosystem Projection

Flywheel should remain the canonical workflow source while supporting projections into coding-agent tool formats.

The first export implementation is read-only. It plans exports but does not write files.

## Why Use It?

Use export planning when you want Flywheel context to appear in another coding-agent tool without making that tool the source of truth.

Good uses:

- see what Cursor files Flywheel could generate
- see what Codex skill/context files Flywheel could generate
- see what Claude context or hook settings Flywheel could generate
- check whether source docs exist before creating tool-specific files
- review planned outputs before allowing file writes in a later implementation

Do not hand-edit generated tool files as the canonical workflow. Keep Flywheel docs and config authoritative, then regenerate or intentionally copy from them.

## Quick Start

Plan every target:

```bash
./flywheel/tools/flywheel_export.sh plan all
```

Plan one target:

```bash
./flywheel/tools/flywheel_export.sh plan cursor
```

Use JSON for automation:

```bash
./flywheel/tools/flywheel_export.sh plan all --format json
```

## Commands

Plan one target:

```bash
./flywheel/tools/flywheel_export.sh plan cursor
./flywheel/tools/flywheel_export.sh plan codex
./flywheel/tools/flywheel_export.sh plan claude
```

Plan every known target:

```bash
./flywheel/tools/flywheel_export.sh plan all
./flywheel/tools/flywheel_export.sh plan all --format json
```

## Targets

Supported first-pass targets:

- `cursor`
- `codex`
- `claude`

## Current Behavior

The export planner reports:

- target tool
- planned output paths
- output kind
- source documents
- whether each source exists
- whether the planned output is ready

It does not write or overwrite files.

## Example Output

For `cursor`, the planner currently reports outputs such as:

```text
cursor (pass)
  rule: .cursor/rules/flywheel.mdc
    Cursor rule projection for Flywheel operating rules and command surface.
```

That means Flywheel has enough source material to generate or maintain that target later. It does not mean the file already exists.

## Design Rule

Flywheel docs, prompts, contracts, tools, plugins, hooks, lanes, and observer traces remain canonical.

Tool-specific files should be generated projections or hand-maintained copies with clear provenance. They should not become a second source of truth.

## Current Limits

The first implementation does not yet:

- generate target files
- install Cursor plugins
- install Codex skills
- write Claude settings
- merge with existing tool-specific files
- enforce provenance checks
