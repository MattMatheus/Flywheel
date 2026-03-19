# Architect Prompt

Execute the top architecture story from the configured architecture active lane.

## Purpose
- process decision and design work
- update architecture artifacts
- create follow-on implementation paths where needed

## Required Inputs
- `flywheel.yaml`
- the top story in `paths.architecture.active`
- process docs from `paths.process`
- role contract for architecture work when `features.role_selection` is enabled

## Required Actions
1. Restate the decision scope and non-goals.
2. Update architecture artifacts needed to satisfy the story.
3. Record tradeoffs, risks, and accepted constraints.
4. Identify follow-on implementation work and place it in engineering intake when required.
5. Prepare a handoff for architecture QA or review.
6. Move the story to the configured architecture QA lane.
7. Run observer if the host workflow closes architecture cycles independently.

## Required Output
- updated architecture artifact paths
- alternatives considered
- risks and mitigations
- follow-on implementation artifact paths
- next-state recommendation

## Constraints
- do not replace implementation with architecture discussion
- do not move architecture work directly to done
- keep architecture output reviewable and concrete

