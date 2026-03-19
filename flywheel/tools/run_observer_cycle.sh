#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/lib/config.sh"

root_dir="$(flywheel_repo_root)"
observer_dir="$(flywheel_path paths.artifacts.observer)"
template_path="$(flywheel_template_path observer_report)"

cycle_id=""
story_path=""
out_path=""

usage() {
  cat <<USAGE
usage: flywheel/tools/run_observer_cycle.sh --cycle-id <id> [--story <path>] [--output <path>]
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cycle-id)
      cycle_id="${2:-}"
      shift 2
      ;;
    --story)
      story_path="${2:-}"
      shift 2
      ;;
    --output)
      out_path="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown arg '$1'" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$cycle_id" ]]; then
  echo "error: --cycle-id is required" >&2
  exit 1
fi

mkdir -p "$observer_dir"

if [[ -z "$out_path" ]]; then
  report_name="$(flywheel_artifact_name observer_report_pattern cycle_id "$cycle_id")"
  out_path="$observer_dir/$report_name"
fi

branch="$(git -C "$root_dir" branch --show-current)"
generated_at="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

tmp_staged="$(mktemp)"
tmp_unstaged="$(mktemp)"
tmp_untracked="$(mktemp)"
trap 'rm -f "$tmp_staged" "$tmp_unstaged" "$tmp_untracked"' EXIT

git -C "$root_dir" diff --cached --name-status > "$tmp_staged"
git -C "$root_dir" diff --name-status > "$tmp_unstaged"
git -C "$root_dir" ls-files --others --exclude-standard | sed 's/^/A\t/' > "$tmp_untracked"

combined_status="$(cat "$tmp_staged" "$tmp_unstaged" "$tmp_untracked" | awk 'NF' | sort -u || true)"

{
  sed "s/<cycle-id>/${cycle_id}/g" "$template_path"
  echo
  sed -n '/## Metadata/,$p' "$template_path" >/dev/null 2>&1 || true
} >/dev/null 2>&1

{
  echo "# Observer Report: $cycle_id"
  echo
  echo "## Metadata"
  echo "- \`cycle_id\`: $cycle_id"
  echo "- \`generated_at_utc\`: $generated_at"
  echo "- \`branch\`: $branch"
  if [[ -n "$story_path" ]]; then
    echo "- \`story_path\`: ${story_path#"$root_dir"/}"
  else
    echo "- \`story_path\`:"
  fi
  echo
  echo "## Diff Inventory"
  if [[ -n "$combined_status" ]]; then
    while IFS= read -r row; do
      [[ -z "$row" ]] && continue
      echo "- $row"
    done <<< "$combined_status"
  else
    echo "- no tracked or untracked file deltas detected"
  fi
  echo
  echo "## Workflow Sync Checks"
  echo "- [ ] Entry docs updated if workflow behavior changed."
  echo "- [ ] Prompts updated if stage behavior changed."
  echo "- [ ] Process docs updated if contracts or gates changed."
  echo "- [ ] Queue order and state remain synchronized."
  echo
  echo "## Handoff Summary"
  echo "- What changed:"
  echo "- Why it changed:"
  echo "- Validation evidence:"
  echo "- Open risks:"
  echo
  echo "## State Promotions"
  echo "- Durable decisions to promote:"
  echo "- Reusable patterns to promote:"
  echo "- Follow-up work to capture:"
  echo
  echo "## Release Impact"
  echo "- Release scope:"
  echo "- Additional release actions:"
} > "$out_path"

printf 'wrote: %s\n' "${out_path#"$root_dir"/}"
