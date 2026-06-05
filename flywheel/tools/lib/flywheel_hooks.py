#!/usr/bin/env python3
"""List, validate, and run configured Flywheel hooks."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from flywheel_config import get_optional, load_config, rel, repo_root


HOOK_EVENTS = (
    "pre_state_move",
    "post_state_move",
    "pre_cycle_close",
    "post_observer",
    "pre_commit",
)


def hooks_dir(root: Path, config: dict[str, Any]) -> Path:
    value = get_optional(config, "hooks.path", "flywheel/hooks")
    if not isinstance(value, str):
        raise RuntimeError("hooks.path must be a string path")
    return root / value


def event_config(config: dict[str, Any]) -> dict[str, Any]:
    value = get_optional(config, "hooks.events", {})
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise RuntimeError("hooks.events must be a mapping")
    return value


def normalize_hook(event: str, index: int, value: Any) -> dict[str, Any]:
    if isinstance(value, str):
        return {
            "event": event,
            "index": index,
            "name": f"{event}_{index + 1}",
            "command": value,
            "required": True,
        }

    if not isinstance(value, dict):
        raise RuntimeError(f"hooks.events.{event}[{index}] must be a command string or mapping")

    name = value.get("name", f"{event}_{index + 1}")
    command = value.get("command")
    required = value.get("required", True)

    if not isinstance(name, str) or not name.strip():
        raise RuntimeError(f"hooks.events.{event}[{index}].name must be a non-empty string")
    if not isinstance(command, str) or not command.strip():
        raise RuntimeError(f"hooks.events.{event}[{index}].command must be a non-empty string")
    if not isinstance(required, bool):
        raise RuntimeError(f"hooks.events.{event}[{index}].required must be true or false")

    return {
        "event": event,
        "index": index,
        "name": name.strip(),
        "command": command.strip(),
        "required": required,
    }


def configured_hooks(config: dict[str, Any]) -> list[dict[str, Any]]:
    events = event_config(config)
    hooks = []
    for event, values in events.items():
        if event not in HOOK_EVENTS:
            continue
        if values is None:
            continue
        if not isinstance(values, list):
            raise RuntimeError(f"hooks.events.{event} must be a list")
        for index, value in enumerate(values):
            hooks.append(normalize_hook(event, index, value))
    return hooks


def validate(root: Path, config: dict[str, Any]) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    try:
        base = hooks_dir(root, config)
    except Exception as exc:
        failures.append(str(exc))
        base = root / "flywheel" / "hooks"

    if not base.exists():
        warnings.append(f"hooks path does not exist: {rel(root, base)}")

    try:
        events = event_config(config)
    except Exception as exc:
        failures.append(str(exc))
        events = {}

    for event in events:
        if event not in HOOK_EVENTS:
            warnings.append(f"unknown hook event: {event}")

    try:
        hooks = configured_hooks(config)
    except Exception as exc:
        failures.append(str(exc))
        hooks = []

    for hook in hooks:
        command = hook["command"]
        first_token = command.split()[0] if command.split() else ""
        candidate = Path(first_token)
        if candidate.is_absolute():
            continue
        if "/" in first_token and not (root / first_token).exists():
            failures.append(f"hook command path is missing for {hook['name']}: {first_token}")

    return failures, warnings


def payload(root: Path) -> dict[str, Any]:
    config = load_config(root)
    failures, warnings = validate(root, config)
    hooks = configured_hooks(config) if not failures else []
    return {
        "flywheel_hooks": {
            "status": "pass" if not failures else "fail",
            "hooks_path": rel(root, hooks_dir(root, config)),
            "events": list(HOOK_EVENTS),
            "hooks": hooks,
            "failures": failures,
            "warnings": warnings,
        }
    }


def run_event(root: Path, event: str, context: dict[str, Any], output_format: str, emit: bool = True) -> dict[str, Any]:
    if event not in HOOK_EVENTS:
        raise RuntimeError(f"unsupported hook event: {event}")

    config = load_config(root)
    hooks = [hook for hook in configured_hooks(config) if hook["event"] == event]
    results = []
    failures = []

    env = os.environ.copy()
    env["FLYWHEEL_HOOK_EVENT"] = event
    env["FLYWHEEL_HOOK_CONTEXT"] = json.dumps(context, sort_keys=True)

    for hook in hooks:
        completed = subprocess.run(
            hook["command"],
            cwd=str(root),
            env=env,
            shell=True,
            text=True,
            capture_output=True,
        )
        result = {
            "name": hook["name"],
            "command": hook["command"],
            "required": hook["required"],
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
        results.append(result)
        if completed.returncode != 0 and hook["required"]:
            failures.append(f"{hook['name']} failed with exit code {completed.returncode}")

    payload = {
        "hook_run": {
            "event": event,
            "status": "pass" if not failures else "fail",
            "hooks_run": results,
            "failures": failures,
        }
    }

    if emit:
        if output_format == "text":
            for result in results:
                print(f"{'PASS' if result['returncode'] == 0 else 'FAIL'}: {result['name']}")
                if result["stdout"]:
                    print(result["stdout"])
                if result["stderr"]:
                    print(result["stderr"])
            if not results:
                print(f"no hooks configured for {event}")
        else:
            print(json.dumps(payload, indent=2))

    if failures:
        raise RuntimeError("; ".join(failures))
    return payload


def print_text(data: dict[str, Any], command: str) -> None:
    hooks = data["flywheel_hooks"]
    if command == "list":
        if not hooks["hooks"]:
            print(f"no hooks configured ({hooks['hooks_path']})")
            return
        for hook in hooks["hooks"]:
            print(f"{hook['event']}: {hook['name']} -> {hook['command']}")
        return

    for failure in hooks["failures"]:
        print(f"FAIL: {failure}")
    for warning in hooks["warnings"]:
        print(f"WARN: {warning}")
    if not hooks["failures"]:
        print("PASS: flywheel hooks")


def parse_context(raw: str) -> dict[str, Any]:
    if not raw:
        return {}
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError("--context must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage Flywheel hooks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("list", "doctor"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--format", choices=("text", "json"), default="text")

    run = subparsers.add_parser("run")
    run.add_argument("event", choices=HOOK_EVENTS)
    run.add_argument("--context", default="")
    run.add_argument("--format", choices=("text", "json"), default="text")

    args = parser.parse_args()
    root = repo_root(Path(__file__))

    try:
        if args.command == "run":
            run_event(root, args.event, parse_context(args.context), args.format)
            return 0

        data = payload(root)
        if args.format == "json":
            print(json.dumps(data, indent=2))
        else:
            print_text(data, args.command)
        return 0 if data["flywheel_hooks"]["status"] == "pass" else 1
    except Exception as exc:
        if getattr(args, "format", "text") == "json":
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
