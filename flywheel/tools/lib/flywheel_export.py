#!/usr/bin/env python3
"""Plan tool-specific Flywheel context exports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from flywheel_config import rel, repo_root


TARGETS = ("cursor", "codex", "claude")

CANONICAL_SOURCES = (
    "AGENTS.md",
    "flywheel/AGENTS.md",
    "flywheel/HUMANS.md",
    "flywheel/DEVELOPMENT_CYCLE.md",
    "flywheel/tools/README.md",
    "docs/README.md",
    "docs/SYSTEM_OVERVIEW.md",
    "docs/ARCHITECTURE.md",
    "docs/OPERATIONS.md",
    "docs/CONFIGURATION.md",
    "docs/PLUGINS.md",
    "docs/HOOKS.md",
    "docs/LANES.md",
    "docs/EXPERIENCE.md",
    "docs/EVOLUTION.md",
)

TARGET_PLANS: dict[str, list[dict[str, Any]]] = {
    "cursor": [
        {
            "kind": "rule",
            "target_path": ".cursor/rules/flywheel.mdc",
            "sources": ["flywheel/AGENTS.md", "flywheel/DEVELOPMENT_CYCLE.md", "flywheel/tools/README.md"],
            "description": "Cursor rule projection for Flywheel operating rules and command surface.",
        },
        {
            "kind": "plugin",
            "target_path": ".cursor/plugins/flywheel/.cursor-plugin/plugin.json",
            "sources": ["docs/PLUGINS.md", "flywheel/plugins/README.md"],
            "description": "Future Cursor plugin manifest projection for Flywheel extensions.",
        },
    ],
    "codex": [
        {
            "kind": "agent_context",
            "target_path": "AGENTS.md",
            "sources": ["AGENTS.md"],
            "description": "Maintained in-repo: root AGENTS.md is the canonical model-agnostic agent entry point.",
        },
        {
            "kind": "skill",
            "target_path": ".codex/skills/flywheel/SKILL.md",
            "sources": ["docs/SYSTEM_OVERVIEW.md", "docs/OPERATIONS.md", "flywheel/tools/README.md"],
            "description": "Future Codex skill projection for Flywheel operation.",
        },
    ],
    "claude": [
        {
            "kind": "agent_context",
            "target_path": "CLAUDE.md",
            "sources": ["AGENTS.md"],
            "description": "Maintained in-repo: CLAUDE.md is a symlink tracking the canonical root AGENTS.md.",
        },
        {
            "kind": "commands",
            "target_path": ".claude/commands/",
            "sources": ["flywheel/stage_contracts.yaml"],
            "description": "Maintained in-repo: thin per-stage slash commands that delegate to ./fw launch.",
        },
        {
            "kind": "hook_settings",
            "target_path": ".claude/settings.json",
            "sources": ["docs/HOOKS.md", "flywheel/hooks/README.md"],
            "description": "Future Claude hook settings projection from Flywheel hook config.",
        },
    ],
}


def source_status(root: Path, sources: list[str]) -> list[dict[str, Any]]:
    rows = []
    for source in sources:
        path = root / source
        rows.append({"path": source, "exists": path.is_file()})
    return rows


def plan_for(root: Path, target: str) -> dict[str, Any]:
    if target not in TARGETS:
        raise RuntimeError(f"unsupported export target: {target}")

    planned = []
    for item in TARGET_PLANS[target]:
        sources = source_status(root, item["sources"])
        planned.append(
            {
                "kind": item["kind"],
                "target_path": item["target_path"],
                "description": item["description"],
                "sources": sources,
                "ready": all(source["exists"] for source in sources),
            }
        )

    return {
        "target": target,
        "status": "pass" if all(item["ready"] for item in planned) else "warn",
        "writes_files": False,
        "planned_outputs": planned,
    }


def payload(root: Path, target: str) -> dict[str, Any]:
    targets = TARGETS if target == "all" else (target,)
    plans = [plan_for(root, item) for item in targets]
    missing = [
        f"{plan['target']}:{output['target_path']} missing source {source['path']}"
        for plan in plans
        for output in plan["planned_outputs"]
        for source in output["sources"]
        if not source["exists"]
    ]
    return {
        "flywheel_export": {
            "status": "pass" if not missing else "warn",
            "mode": "plan",
            "repo_root": rel(root, root),
            "targets": plans,
            "missing_sources": missing,
            "canonical_sources": source_status(root, list(CANONICAL_SOURCES)),
        }
    }


def print_text(data: dict[str, Any]) -> None:
    export = data["flywheel_export"]
    for plan in export["targets"]:
        print(f"{plan['target']} ({plan['status']})")
        for output in plan["planned_outputs"]:
            print(f"  {output['kind']}: {output['target_path']}")
            print(f"    {output['description']}")
            for source in output["sources"]:
                marker = "ok" if source["exists"] else "missing"
                print(f"    - {marker}: {source['path']}")
    for missing in export["missing_sources"]:
        print(f"WARN: {missing}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan Flywheel exports for coding-agent tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan = subparsers.add_parser("plan")
    plan.add_argument("target", choices=(*TARGETS, "all"))
    plan.add_argument("--format", choices=("text", "json"), default="text")

    args = parser.parse_args()
    root = repo_root(Path(__file__))
    data = payload(root, args.target)

    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        print_text(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
