---
description: Run the Flywheel engineering stage on the top active story
---

Run `./fw launch engineering --format json`. If `status` is `no_stories`, report that and stop.

Otherwise: read the prompt file and story it points at, then execute the contract — implement the story, satisfy every `exit_gate` item, and avoid every `forbidden_actions` item. Move the story with `./fw move <item> active qa --reason "<summary>"` when the handoff is complete. Do not commit; QA closes the cycle.
