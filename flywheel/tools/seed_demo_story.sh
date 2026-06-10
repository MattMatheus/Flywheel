#!/usr/bin/env bash
set -euo pipefail

# Seed a sample story into engineering intake so a fresh harness can exercise
# the full lifecycle: pm -> engineering -> qa -> close-cycle.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/lib/config.sh"

intake_dir="$(flywheel_path paths.engineering.intake)"
today="$(date +%Y%m%d)"
story_id="STORY-${today}-demo-walkthrough"
story_path="${intake_dir}/${story_id}.md"

if [[ -f "$story_path" ]]; then
  echo "demo story already exists: $story_path" >&2
  exit 1
fi

cat > "$story_path" <<EOF
---
kind: story
id: ${story_id}
status: intake
owner_role: engineering
source: direct
success_metric: one full cycle closes with an observer record and one commit
release_scope: n/a
ready: false
---

# Story: Demo walkthrough of the Flywheel lifecycle

## Metadata
- \`id\`: ${story_id}
- \`owner_role\`: engineering
- \`status\`: intake
- \`source\`: direct
- \`decision_refs\`: []
- \`success_metric\`: one full cycle closes with an observer record and one commit
- \`release_scope\`: n/a

## Problem Statement
- A fresh harness has an empty backlog, so operators cannot see the lifecycle work end-to-end.

## Scope
- In: add a single line noting the demo run to \`flywheel/artifacts/planning/DEMO_LOG.md\`.
- Out: any change to harness tools, prompts, or configuration.

## Assumptions
- The harness passes \`./fw doctor\`.

## Acceptance Criteria
1. \`flywheel/artifacts/planning/DEMO_LOG.md\` exists and contains one dated demo entry.
2. The story reaches \`done\` only through the qa lane.
3. The cycle closes via \`./fw close-cycle\` with an observer record and one commit.

## Validation
- Required checks: \`./fw validate\`
- Additional checks: \`./fw status\`

## Dependencies
- none

## Risks
- none

## Open Questions
- none

## Next Step
- Run the pm stage to promote this story into the active lane.

## Engineering Handoff
- \`change_summary\`:
- \`validation_evidence\`:
- \`qa_focus\`:
- \`open_risks\`:

## QA Verdict
- \`verdict\`:
- \`evidence_quality\`:
- \`defects\`:
- \`state_transition\`:
EOF

# Register the story in the root backlog summary so ./fw validate stays green.
backlog_readme="$(flywheel_repo_root)/flywheel/backlog/README.md"
if [[ -f "$backlog_readme" ]]; then
  story_ref="flywheel/backlog/engineering/intake/${story_id}.md"
  python3 - "$backlog_readme" "$story_ref" <<'PY'
import sys
from pathlib import Path

readme = Path(sys.argv[1])
ref = sys.argv[2]
empty = "No candidate engineering or architecture intake items."
lines = readme.read_text(encoding="utf-8").splitlines()
entry = f"- `{ref}`"
if entry not in lines:
    for index, line in enumerate(lines):
        if line.strip() == empty:
            lines[index] = entry
            break
    else:
        lines.append(entry)
readme.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
PY
fi

echo "seeded: $story_path"
echo "next: ./fw launch pm   (promote it), then ./fw launch cycle (drain it)"
