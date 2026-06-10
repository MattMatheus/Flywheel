---
description: Drain the active engineering queue by alternating engineering and QA
---

Run `./fw launch cycle --format json` and execute the loop it describes: run the engineering stage, then the QA stage, then `./fw close-cycle --cycle-id <id> --story <path>` for one commit per cycle. Repeat until `./fw launch engineering --format json` reports `no_stories`, then stop — do not invent work.
