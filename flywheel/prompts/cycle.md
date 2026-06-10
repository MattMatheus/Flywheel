# Cycle Prompt

Drain the engineering active queue by alternating the engineering and QA
stages, one story and one commit per cycle.

The authoritative loop, exit gate, and forbidden actions come from
`./fw launch cycle --format json`. This prompt adds the judgment the contract
cannot express.

## Judgment Guidance
- Each iteration is a full engineering stage then a full QA stage on the same
  story. Do not batch several stories into one pass or one commit.
- `./fw close-cycle --cycle-id <id> --story <path>` performs the closure
  mechanics: state validation, observer record, experience index, and the
  single cycle commit.
- A story QA returns to `active` is the next iteration's work — fix it before
  starting new stories.
- Stop conditions are explicit: the active lane is empty (`no_stories`), or an
  item is blocked in a way only the operator can resolve. Say which one ended
  the loop. Never invent work to keep the loop alive.
