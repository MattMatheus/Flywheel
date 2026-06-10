#!/usr/bin/env python3
"""One-screen Flywheel workflow status: branch, state, lanes, next stories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from flywheel_config import DOMAINS, LANES, get, git_current_branch, git_is_repo, load_config, path, rel, repo_root
from stage_context import select_top_item
from validate_workflow_state import validate


def lane_counts(root: Path, config: dict[str, Any], domain: str) -> dict[str, int]:
    counts = {}
    for lane in LANES:
        lane_dir = path(root, config, f"paths.{domain}.{lane}")
        if lane_dir.is_dir():
            counts[lane] = sum(1 for item in lane_dir.glob("*.md") if item.name != "README.md" and item.is_file())
        else:
            counts[lane] = 0
    return counts


def payload(root: Path) -> dict[str, Any]:
    config = load_config(root)
    required_branch = get(config, "workflow.required_branch")
    current_branch = git_current_branch(root) if git_is_repo(root) else ""

    workflow = validate(root)

    domains = {}
    for domain in DOMAINS:
        active_dir = path(root, config, f"paths.{domain}.active")
        top = select_top_item(active_dir) if active_dir.is_dir() else None
        domains[domain] = {
            "lanes": lane_counts(root, config, domain),
            "next_active_story": rel(root, top) if top else None,
        }

    return {
        "flywheel_status": {
            "branch": {
                "current": current_branch,
                "required": required_branch,
                "ok": current_branch == required_branch,
            },
            "workflow_state": {
                "status": "pass" if not workflow.failures else "fail",
                "failures": workflow.failures,
                "warnings": workflow.warnings,
            },
            "domains": domains,
        }
    }


def print_text(data: dict[str, Any]) -> None:
    status = data["flywheel_status"]
    branch = status["branch"]
    marker = "ok" if branch["ok"] else f"MISMATCH (required: {branch['required']})"
    print(f"branch: {branch['current']} ({marker})")

    state = status["workflow_state"]
    print(f"workflow state: {'PASS' if state['status'] == 'pass' else 'FAIL'}")
    for failure in state["failures"]:
        print(f"  FAIL: {failure}")
    for warning in state["warnings"]:
        print(f"  WARN: {warning}")

    for domain, info in status["domains"].items():
        counts = " | ".join(f"{lane} {count}" for lane, count in info["lanes"].items())
        print(f"{domain}: {counts}")
        if info["next_active_story"]:
            print(f"  next: {info['next_active_story']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Show Flywheel workflow status")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    root = repo_root(Path(__file__))
    data = payload(root)

    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        print_text(data)

    status = data["flywheel_status"]
    healthy = status["branch"]["ok"] and status["workflow_state"]["status"] == "pass"
    return 0 if healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())
