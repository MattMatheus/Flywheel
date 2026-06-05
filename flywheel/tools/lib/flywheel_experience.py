#!/usr/bin/env python3
"""Index observer traces into a lightweight experience store."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from flywheel_config import load_config, path, rel, repo_root


def experience_dir(root: Path, config: dict[str, Any]) -> Path:
    configured = config.get("experience", {})
    if isinstance(configured, dict) and isinstance(configured.get("path"), str):
        return root / configured["path"]
    return root / "flywheel" / "artifacts" / "experience"


def observer_dir(root: Path, config: dict[str, Any]) -> Path:
    return path(root, config, "paths.artifacts.observer")


def trace_files(root: Path, config: dict[str, Any]) -> list[Path]:
    directory = observer_dir(root, config)
    if not directory.is_dir():
        return []
    return sorted(file_path for file_path in directory.glob("*.json") if file_path.is_file())


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def trace_record(root: Path, trace_path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return None, f"{rel(root, trace_path)}: {exc}"

    if not isinstance(trace, dict):
        return None, f"{rel(root, trace_path)}: trace must be a JSON object"

    validation = as_dict(trace.get("validation"))
    changes = as_dict(trace.get("changes_made"))
    risks = as_dict(trace.get("warnings_and_risks"))
    action = as_dict(trace.get("action_record"))
    next_step = as_dict(trace.get("next_step"))

    return (
        {
            "cycle_id": trace.get("cycle_id", ""),
            "generated_at_utc": trace.get("generated_at_utc", ""),
            "branch": trace.get("branch", ""),
            "story_path": trace.get("story_path", ""),
            "trace_path": rel(root, trace_path),
            "stage_event_count": len(as_list(trace.get("stage_trace"))),
            "diff_count": len(as_list(trace.get("diff_inventory"))),
            "files_changed_count": len(as_list(changes.get("files_changed"))),
            "state_transition_count": len(as_list(changes.get("state_transitions"))),
            "validation_checks_run_count": len(as_list(validation.get("checks_run"))),
            "validation_results_count": len(as_list(validation.get("results"))),
            "validation_checks_not_run_count": len(as_list(validation.get("checks_not_run"))),
            "risk_count": len(as_list(risks.get("unresolved_risks"))),
            "warning_count": len(as_list(risks.get("warnings"))),
            "highest_action_class": action.get("highest_action_class", ""),
            "approval_required": action.get("approval_required", ""),
            "approval_reference": action.get("approval_reference", ""),
            "recommended_next_state": next_step.get("recommended_next_state", ""),
            "follow_up_count": len(as_list(next_step.get("follow_up_work"))),
        },
        None,
    )


def build_index(root: Path, config: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    records = []
    warnings = []
    for trace_path in trace_files(root, config):
        record, warning = trace_record(root, trace_path)
        if warning:
            warnings.append(warning)
        if record:
            records.append(record)
    return records, warnings


def summary(records: list[dict[str, Any]], warnings: list[str]) -> dict[str, Any]:
    action_classes = Counter(record.get("highest_action_class", "") or "unspecified" for record in records)
    next_states = Counter(record.get("recommended_next_state", "") or "unspecified" for record in records)
    return {
        "trace_count": len(records),
        "warning_count": len(warnings),
        "total_diff_count": sum(record["diff_count"] for record in records),
        "total_validation_checks_run": sum(record["validation_checks_run_count"] for record in records),
        "total_validation_checks_not_run": sum(record["validation_checks_not_run_count"] for record in records),
        "total_risks": sum(record["risk_count"] for record in records),
        "total_follow_ups": sum(record["follow_up_count"] for record in records),
        "action_classes": dict(sorted(action_classes.items())),
        "recommended_next_states": dict(sorted(next_states.items())),
    }


def write_index(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    records, warnings = build_index(root, config)
    directory = experience_dir(root, config)
    directory.mkdir(parents=True, exist_ok=True)

    index_path = directory / "index.jsonl"
    summary_path = directory / "stage-metrics.json"
    lessons_path = directory / "lessons.md"

    index_path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    summary_payload = summary(records, warnings)
    summary_path.write_text(json.dumps(summary_payload, indent=2) + "\n", encoding="utf-8")
    lessons_path.write_text(lessons_markdown(summary_payload, warnings), encoding="utf-8")

    return {
        "experience_index": {
            "status": "pass" if not warnings else "warn",
            "experience_path": rel(root, directory),
            "index_path": rel(root, index_path),
            "summary_path": rel(root, summary_path),
            "lessons_path": rel(root, lessons_path),
            "records_indexed": len(records),
            "warnings": warnings,
            "summary": summary_payload,
        }
    }


def lessons_markdown(summary_payload: dict[str, Any], warnings: list[str]) -> str:
    lines = [
        "# Flywheel Experience Lessons",
        "",
        "Generated from observer JSON traces.",
        "",
        "## Summary",
        f"- `trace_count`: {summary_payload['trace_count']}",
        f"- `total_validation_checks_run`: {summary_payload['total_validation_checks_run']}",
        f"- `total_validation_checks_not_run`: {summary_payload['total_validation_checks_not_run']}",
        f"- `total_risks`: {summary_payload['total_risks']}",
        f"- `total_follow_ups`: {summary_payload['total_follow_ups']}",
        "",
        "## Notes",
    ]
    if summary_payload["trace_count"] == 0:
        lines.append("- No observer traces have been indexed yet.")
    else:
        lines.append("- Review repeated risks, skipped validation, and follow-up counts before changing workflow behavior.")

    if warnings:
        lines.extend(["", "## Warnings"])
        lines.extend(f"- {warning}" for warning in warnings)

    return "\n".join(lines).rstrip() + "\n"


def print_text(payload: dict[str, Any]) -> None:
    index = payload["experience_index"]
    print(f"indexed traces: {index['records_indexed']}")
    print(f"wrote: {index['index_path']}")
    print(f"wrote: {index['summary_path']}")
    print(f"wrote: {index['lessons_path']}")
    for warning in index["warnings"]:
        print(f"WARN: {warning}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage Flywheel experience indexes")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("index", "summarize"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--format", choices=("text", "json"), default="text")

    args = parser.parse_args()
    root = repo_root(Path(__file__))
    config = load_config(root)
    payload = write_index(root, config)

    if args.command == "summarize":
        payload = {"experience_summary": payload["experience_index"]["summary"]}

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    elif args.command == "summarize":
        summary_payload = payload["experience_summary"]
        print(f"trace_count: {summary_payload['trace_count']}")
        print(f"total_validation_checks_run: {summary_payload['total_validation_checks_run']}")
        print(f"total_risks: {summary_payload['total_risks']}")
        print(f"total_follow_ups: {summary_payload['total_follow_ups']}")
    else:
        print_text(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
