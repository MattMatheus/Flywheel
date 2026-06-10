#!/usr/bin/env python3
"""Close a Flywheel cycle: validate, observe, index experience, commit."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from flywheel_config import get, git_current_branch, load_config, repo_root
from flywheel_hooks import run_event
from validate_workflow_state import validate


def run_tool(root: Path, script: str, *args: str) -> str:
    command = [str(root / "flywheel" / "tools" / script), *args]
    return subprocess.check_output(command, text=True)


def close_cycle(args: argparse.Namespace) -> dict[str, Any]:
    root = repo_root(Path(__file__))
    config = load_config(root)

    required_branch = get(config, "workflow.required_branch")
    current_branch = git_current_branch(root)
    if current_branch != required_branch:
        raise RuntimeError(f"cycle closure requires branch '{required_branch}'; active branch is '{current_branch}'")

    context = {"cycle_id": args.cycle_id, "story": args.story}
    run_event(root, "pre_cycle_close", context, "json", emit=False)

    workflow = validate(root)
    if workflow.failures:
        details = "; ".join(workflow.failures)
        raise RuntimeError(f"workflow state validation failed: {details}")

    observer_args = ["--cycle-id", args.cycle_id, "--format", "json"]
    if args.story:
        observer_args.extend(["--story", args.story])
    observer = json.loads(run_tool(root, "run_observer_cycle.sh", *observer_args))["observer"]

    run_event(root, "post_observer", observer, "json", emit=False)
    run_tool(root, "flywheel_experience.sh", "index", "--format", "json")

    commit_message = get(config, "workflow.cycle_commit_format").replace("{cycle_id}", args.cycle_id)
    commit_hash = None
    if not args.no_commit:
        run_event(root, "pre_commit", {"cycle_id": args.cycle_id, "message": commit_message}, "json", emit=False)
        subprocess.check_call(["git", "-C", str(root), "add", "-A"])
        subprocess.check_call(["git", "-C", str(root), "commit", "-m", commit_message], stdout=subprocess.DEVNULL)
        commit_hash = subprocess.check_output(["git", "-C", str(root), "rev-parse", "--short", "HEAD"], text=True).strip()

    return {
        "close_cycle": {
            "cycle_id": args.cycle_id,
            "story": args.story or None,
            "workflow_state": "pass",
            "observer_report": observer["report_path"],
            "observer_trace": observer["trace_path"],
            "commit_message": None if args.no_commit else commit_message,
            "commit": commit_hash,
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Close a Flywheel cycle")
    parser.add_argument("--cycle-id", required=True)
    parser.add_argument("--story", default="")
    parser.add_argument("--no-commit", action="store_true", help="run closure checks and observer without committing")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    try:
        payload = close_cycle(args)
    except Exception as exc:
        if args.format == "json":
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"error: {exc}")
        return 1

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        closure = payload["close_cycle"]
        print(f"observer: {closure['observer_report']}")
        print(f"trace: {closure['observer_trace']}")
        if closure["commit"]:
            print(f"commit: {closure['commit']} ({closure['commit_message']})")
        else:
            print("commit: skipped (--no-commit)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
