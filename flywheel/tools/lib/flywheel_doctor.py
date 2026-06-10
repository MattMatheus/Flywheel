#!/usr/bin/env python3
"""Run local health checks for the Flywheel harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from flywheel_config import get, git_current_branch, git_is_repo, load_config, repo_root
from flywheel_hooks import payload as hook_payload
from flywheel_plugins import payload as plugin_payload
from stage_context import load_stage_contracts
from validate_workflow_state import validate

REQUIRED_FILES = (
    "fw",
    "flywheel.yaml",
    "AGENTS.md",
    "CLAUDE.md",
    "flywheel/README.md",
    "flywheel/AGENTS.md",
    "flywheel/HUMANS.md",
    "flywheel/DEVELOPMENT_CYCLE.md",
    "flywheel/CONFIG_SCHEMA.md",
    "docs/README.md",
    "docs/SYSTEM_OVERVIEW.md",
    "docs/ARCHITECTURE.md",
    "docs/OPERATIONS.md",
    "docs/CONFIGURATION.md",
    "docs/PLUGINS.md",
    "docs/HOOKS.md",
    "docs/LANES.md",
    "docs/EXPERIENCE.md",
    "docs/EXPORTS.md",
    "docs/EVOLUTION.md",
    "flywheel/stage_contracts.yaml",
    "flywheel/tools/README.md",
    "flywheel/tools/launch_stage.sh",
    "flywheel/tools/validate_workflow_state.sh",
    "flywheel/tools/flywheel_state.sh",
    "flywheel/tools/flywheel_approval.sh",
    "flywheel/tools/run_observer_cycle.sh",
    "flywheel/tools/flywheel_plugins.sh",
    "flywheel/tools/flywheel_hooks.sh",
    "flywheel/tools/flywheel_lanes.sh",
    "flywheel/tools/flywheel_experience.sh",
    "flywheel/tools/flywheel_export.sh",
    "flywheel/plugins/README.md",
    "flywheel/hooks/README.md",
    "flywheel/artifacts/experience/README.md",
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Flywheel harness health")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    root = repo_root(Path(__file__))
    failures: list[str] = []
    warnings: list[str] = []

    for required in REQUIRED_FILES:
        if not (root / required).exists():
            failures.append(f"missing required file: {required}")

    try:
        config = load_config(root)
    except Exception as exc:
        config = None
        failures.append(f"config load failed: {exc}")

    if config is not None and git_is_repo(root):
        try:
            required_branch = get(config, "workflow.required_branch")
            current_branch = git_current_branch(root)
            if current_branch != required_branch:
                failures.append(
                    f"branch mismatch: workflow.required_branch is '{required_branch}' "
                    f"but active branch is '{current_branch}'"
                )
        except Exception as exc:
            failures.append(f"branch check failed: {exc}")

    agents_entry = root / "AGENTS.md"
    claude_entry = root / "CLAUDE.md"
    if agents_entry.is_file() and claude_entry.is_file():
        if claude_entry.read_text(encoding="utf-8") != agents_entry.read_text(encoding="utf-8"):
            failures.append("CLAUDE.md has drifted from AGENTS.md; it must track AGENTS.md (symlink preferred)")

    try:
        contracts = load_stage_contracts(root)
        for stage in ("planning", "architect", "engineering", "qa", "pm", "cycle"):
            if stage not in contracts:
                failures.append(f"stage contract missing: {stage}")
    except Exception as exc:
        failures.append(f"stage contracts load failed: {exc}")

    try:
        workflow = validate(root)
        failures.extend(workflow.failures)
        warnings.extend(workflow.warnings)
    except Exception as exc:
        failures.append(f"workflow validation failed: {exc}")

    try:
        plugins = plugin_payload(root)["flywheel_plugins"]
        failures.extend(f"plugin validation failed: {failure}" for failure in plugins["failures"])
        warnings.extend(f"plugin validation warning: {warning}" for warning in plugins["warnings"])
    except Exception as exc:
        failures.append(f"plugin validation failed: {exc}")

    try:
        hooks = hook_payload(root)["flywheel_hooks"]
        failures.extend(f"hook validation failed: {failure}" for failure in hooks["failures"])
        warnings.extend(f"hook validation warning: {warning}" for warning in hooks["warnings"])
    except Exception as exc:
        failures.append(f"hook validation failed: {exc}")

    payload = {
        "flywheel_doctor": {
            "status": "pass" if not failures else "fail",
            "failures": failures,
            "warnings": warnings,
        }
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        for failure in failures:
            print(f"FAIL: {failure}")
        for warning in warnings:
            print(f"WARN: {warning}")
        if not failures:
            print("PASS: flywheel doctor")

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
