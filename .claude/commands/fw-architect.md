---
description: Run the Flywheel architect stage on the top architecture story
---

Run `./fw launch architect --format json`. If `status` is `no_stories`, report that and stop.

Otherwise: read the prompt file and story it points at, then execute the contract — produce a concrete, reviewable decision with alternatives and tradeoffs, file follow-on engineering intake when needed, and move the story to architecture QA with `./fw move <item> active qa --domain architecture`.
