# Flywheel Plugins

Optional Flywheel plugins live in subdirectories here.

Use a plugin when optional workflow behavior should be packaged, named, documented, and validated without becoming part of Flywheel core.

Examples:

- review guidance
- optional hooks
- project-specific prompts
- reusable templates
- tool export material

Each plugin should include a `flywheel-plugin.yaml` manifest:

```yaml
name: example-plugin
description: Short description of what the plugin contributes.
version: 0.1.0
publisher: local
source: ""
sha256: ""
contributions:
  skills: skills
  hooks: hooks
permissions:
  shell: false
  network: false
  writes: []
```

Plugins are extensions to the harness. They should declare their contributions and permissions instead of mutating core Flywheel files directly.

The first plugin implementation validates declarations only. Flywheel does not yet automatically apply plugin hooks, prompts, templates, or stage-contract patches.

Validate installed plugins with:

```bash
./flywheel/tools/flywheel_plugins.sh doctor
```
