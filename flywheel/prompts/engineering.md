# Engineering Prompt

Implement the top story in the engineering active lane and hand it to QA.

The authoritative checklist, exit gate, and forbidden actions come from
`./fw launch engineering --format json`. This prompt adds the judgment the
contract cannot express.

## Judgment Guidance
- Restate the story in your own words before touching code; if your restatement
  and the acceptance criteria disagree, stop and flag it instead of guessing.
- Implement the smallest change that satisfies the acceptance criteria. Scope
  creep discovered mid-story becomes a new intake item, not extra diff.
- Validation evidence means command output, not assertions. If a check cannot
  run, record which one and why — that record is QA input, not a footnote.
- Classify your actions (`read`, `local write`, `risky write`, `sensitive or
  production`) and get explicit human approval before the last two.

## Handoff Quality Bar
`## Engineering Handoff` on the story must let QA proceed without re-deriving
context: what changed, the evidence it works, the risks you did not close, and
where QA should focus first. A handoff QA has to investigate is a failed
handoff.

Move the story with `./fw move <item> active qa --reason "<summary>"`.
Do not commit — QA closes the cycle.
