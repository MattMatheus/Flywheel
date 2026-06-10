---
description: Run the Flywheel PM stage to refine intake and order the queues
---

Run `./fw launch pm --format json`, read the prompt file it points at, and execute the contract: refine intake items until bounded and testable, promote ready work into the active lanes with `./fw move`, and keep queue ordering explicit. Do not implement fixes.

PM priorities from the operator: $ARGUMENTS
