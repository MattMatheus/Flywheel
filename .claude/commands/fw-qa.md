---
description: Run the Flywheel QA stage on the story in the QA lane
---

Run `./fw launch qa --format json`. If `status` is `no_stories`, report that and stop.

Otherwise: read the prompt file and story it points at, then execute the contract — validate against acceptance criteria, treat missing evidence as blocking, fill `## QA Verdict`, and move the story with `./fw move <item> qa done` or `./fw move <item> qa active`. Close with `./fw close-cycle --cycle-id <id> --story <path>`.
