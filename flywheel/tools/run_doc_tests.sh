#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/lib/config.sh"

root_dir="$(flywheel_repo_root)"

check_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    echo "PASS: $path"
  else
    echo "FAIL: missing $path" >&2
    return 1
  fi
}

check_dir() {
  local path="$1"
  if [[ -d "$path" ]]; then
    echo "PASS: $path"
  else
    echo "FAIL: missing $path" >&2
    return 1
  fi
}

check_file "$root_dir/flywheel.yaml"
check_file "$root_dir/fw"
check_file "$root_dir/AGENTS.md"
check_file "$root_dir/CLAUDE.md"

if cmp -s "$root_dir/AGENTS.md" "$root_dir/CLAUDE.md"; then
  echo "PASS: CLAUDE.md tracks AGENTS.md"
else
  echo "FAIL: CLAUDE.md has drifted from AGENTS.md" >&2
  exit 1
fi

for stage_command in fw-planning fw-architect fw-pm fw-engineering fw-qa fw-cycle fw-status; do
  check_file "$root_dir/.claude/commands/${stage_command}.md"
done
check_file "$root_dir/flywheel/CONFIG_SCHEMA.md"
check_file "$root_dir/flywheel/README.md"
check_file "$root_dir/flywheel/HUMANS.md"
check_file "$root_dir/flywheel/AGENTS.md"
check_file "$root_dir/flywheel/DEVELOPMENT_CYCLE.md"
check_file "$root_dir/docs/README.md"
check_file "$root_dir/docs/SYSTEM_OVERVIEW.md"
check_file "$root_dir/docs/ARCHITECTURE.md"
check_file "$root_dir/docs/OPERATIONS.md"
check_file "$root_dir/docs/CONFIGURATION.md"
check_file "$root_dir/docs/PLUGINS.md"
check_file "$root_dir/docs/HOOKS.md"
check_file "$root_dir/docs/LANES.md"
check_file "$root_dir/docs/EXPERIENCE.md"
check_file "$root_dir/docs/EXPORTS.md"
check_file "$root_dir/docs/EVOLUTION.md"
check_file "$root_dir/flywheel/stage_contracts.yaml"
check_file "$root_dir/flywheel/tools/README.md"
check_file "$root_dir/flywheel/examples/STORY_LIFECYCLE_EXAMPLE.md"

check_dir "$(flywheel_path paths.prompts)"
check_dir "$(flywheel_path paths.roles)"
check_dir "$(flywheel_path paths.process)"
check_dir "$(flywheel_path paths.templates)"
check_dir "$(flywheel_path paths.artifacts.planning)"
check_dir "$(flywheel_path paths.artifacts.observer)"
check_dir "$(flywheel_path experience.path)"
check_dir "$(flywheel_path plugins.path)"
check_dir "$(flywheel_path hooks.path)"
check_dir "$(flywheel_path paths.engineering.active)"
check_dir "$(flywheel_path paths.architecture.active)"

check_file "$(flywheel_template_path story)"
check_file "$(flywheel_template_path bug)"
check_file "$(flywheel_template_path architecture_story)"
check_file "$(flywheel_template_path observer_report)"

check_file "$root_dir/flywheel/tools/launch_stage.sh"
check_file "$root_dir/flywheel/tools/flywheel_status.sh"
check_file "$root_dir/flywheel/tools/close_cycle.sh"
check_file "$root_dir/flywheel/tools/seed_demo_story.sh"
check_file "$root_dir/flywheel/tools/lib/flywheel_status.py"
check_file "$root_dir/flywheel/tools/lib/close_cycle.py"
check_file "$root_dir/flywheel/tools/artifact_workflow.sh"
check_file "$root_dir/flywheel/tools/artifact_workflow_commands.sh"
check_file "$root_dir/flywheel/tools/flywheel_doctor.sh"
check_file "$root_dir/flywheel/tools/flywheel_plugins.sh"
check_file "$root_dir/flywheel/tools/flywheel_hooks.sh"
check_file "$root_dir/flywheel/tools/flywheel_lanes.sh"
check_file "$root_dir/flywheel/tools/flywheel_experience.sh"
check_file "$root_dir/flywheel/tools/flywheel_export.sh"
check_file "$root_dir/flywheel/tools/flywheel_approval.sh"
check_file "$root_dir/flywheel/tools/flywheel_state.sh"
check_file "$root_dir/flywheel/tools/run_observer_cycle.sh"
check_file "$root_dir/flywheel/tools/validate_intake_items.sh"
check_file "$root_dir/flywheel/tools/validate_workflow_state.sh"
check_file "$root_dir/flywheel/tools/lib/flywheel_config.py"
check_file "$root_dir/flywheel/tools/lib/flywheel_approval.py"
check_file "$root_dir/flywheel/tools/lib/flywheel_doctor.py"
check_file "$root_dir/flywheel/tools/lib/flywheel_plugins.py"
check_file "$root_dir/flywheel/tools/lib/flywheel_hooks.py"
check_file "$root_dir/flywheel/tools/lib/flywheel_lanes.py"
check_file "$root_dir/flywheel/tools/lib/flywheel_experience.py"
check_file "$root_dir/flywheel/tools/lib/flywheel_export.py"
check_file "$root_dir/flywheel/tools/lib/flywheel_state.py"
check_file "$root_dir/flywheel/tools/lib/run_observer_cycle.py"
check_file "$root_dir/flywheel/tools/lib/stage_context.py"
check_file "$root_dir/flywheel/tools/lib/validate_workflow_state.py"

"$root_dir/flywheel/tools/validate_intake_items.sh"
"$root_dir/flywheel/tools/validate_workflow_state.sh"
"$root_dir/flywheel/tools/flywheel_plugins.sh" doctor
"$root_dir/flywheel/tools/flywheel_hooks.sh" doctor
"$root_dir/flywheel/tools/flywheel_lanes.sh" --format json >/dev/null
"$root_dir/flywheel/tools/flywheel_status.sh" --format json >/dev/null
"$root_dir/flywheel/tools/flywheel_experience.sh" summarize --format json >/dev/null
"$root_dir/flywheel/tools/flywheel_export.sh" plan all --format json >/dev/null
"$root_dir/fw" commands >/dev/null
"$root_dir/flywheel/tools/flywheel_doctor.sh"

echo "Result: PASS"
