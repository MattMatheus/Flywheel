#!/usr/bin/env python3
"""List and validate Flywheel plugins."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from flywheel_config import load_config, rel, repo_root

try:
    import yaml
except ImportError:  # pragma: no cover - operator-facing fallback
    yaml = None


PLUGIN_MANIFEST = "flywheel-plugin.yaml"
CONTRIBUTION_KEYS = ("skills", "hooks", "prompts", "templates", "stage_contract_patches")
PERMISSION_KEYS = ("shell", "network", "writes")


def plugins_dir(root: Path, config: dict[str, Any]) -> Path:
    configured = config.get("plugins", {})
    if isinstance(configured, dict) and isinstance(configured.get("path"), str):
        return root / configured["path"]
    return root / "flywheel" / "plugins"


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is required for Flywheel Python tools")
    with manifest_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise RuntimeError("manifest must contain a mapping")
    return data


def discover_plugins(root: Path, config: dict[str, Any]) -> list[dict[str, Any]]:
    base = plugins_dir(root, config)
    if not base.exists():
        return []

    plugins = []
    for directory in sorted(item for item in base.iterdir() if item.is_dir()):
        manifest_path = directory / PLUGIN_MANIFEST
        plugin = {
            "name": directory.name,
            "path": rel(root, directory),
            "manifest_path": rel(root, manifest_path),
            "manifest": None,
            "errors": [],
            "warnings": [],
        }
        if not manifest_path.is_file():
            plugin["errors"].append(f"missing {PLUGIN_MANIFEST}")
        else:
            try:
                plugin["manifest"] = load_manifest(manifest_path)
            except Exception as exc:
                plugin["errors"].append(f"manifest load failed: {exc}")
        validate_plugin(root, directory, plugin)
        plugins.append(plugin)
    return plugins


def require_string(plugin: dict[str, Any], manifest: dict[str, Any], key: str) -> str:
    value = manifest.get(key)
    if not isinstance(value, str) or not value.strip():
        plugin["errors"].append(f"manifest field '{key}' must be a non-empty string")
        return ""
    return value.strip()


def validate_contributions(directory: Path, plugin: dict[str, Any], manifest: dict[str, Any]) -> None:
    contributions = manifest.get("contributions", {})
    if contributions is None:
        contributions = {}
    if not isinstance(contributions, dict):
        plugin["errors"].append("manifest field 'contributions' must be a mapping")
        return

    for key in contributions:
        if key not in CONTRIBUTION_KEYS:
            plugin["warnings"].append(f"unknown contribution key '{key}'")

    for key in CONTRIBUTION_KEYS:
        value = contributions.get(key)
        if value in (None, False):
            continue
        if isinstance(value, str):
            paths = [value]
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            paths = value
        else:
            plugin["errors"].append(f"contributions.{key} must be a string path or list of string paths")
            continue

        for relative_path in paths:
            if Path(relative_path).is_absolute() or ".." in Path(relative_path).parts:
                plugin["errors"].append(f"contributions.{key} path must stay inside plugin: {relative_path}")
                continue
            if not (directory / relative_path).exists():
                plugin["errors"].append(f"contributions.{key} path is missing: {relative_path}")


def validate_permissions(plugin: dict[str, Any], manifest: dict[str, Any]) -> None:
    permissions = manifest.get("permissions", {})
    if permissions is None:
        permissions = {}
    if not isinstance(permissions, dict):
        plugin["errors"].append("manifest field 'permissions' must be a mapping")
        return

    for key in permissions:
        if key not in PERMISSION_KEYS:
            plugin["warnings"].append(f"unknown permission key '{key}'")

    for key in ("shell", "network"):
        if key in permissions and not isinstance(permissions[key], bool):
            plugin["errors"].append(f"permissions.{key} must be true or false")

    writes = permissions.get("writes", [])
    if writes is None:
        writes = []
    if not isinstance(writes, list) or not all(isinstance(item, str) for item in writes):
        plugin["errors"].append("permissions.writes must be a list of string path globs")


def validate_plugin(root: Path, directory: Path, plugin: dict[str, Any]) -> None:
    manifest = plugin.get("manifest")
    if not isinstance(manifest, dict):
        return

    manifest_name = require_string(plugin, manifest, "name")
    if manifest_name and manifest_name != directory.name:
        plugin["errors"].append("manifest field 'name' must match plugin directory name")

    require_string(plugin, manifest, "description")
    require_string(plugin, manifest, "version")

    if "publisher" in manifest and not isinstance(manifest["publisher"], str):
        plugin["errors"].append("manifest field 'publisher' must be a string")
    if "source" in manifest and not isinstance(manifest["source"], str):
        plugin["errors"].append("manifest field 'source' must be a string")
    if "sha256" in manifest and not isinstance(manifest["sha256"], str):
        plugin["errors"].append("manifest field 'sha256' must be a string")

    validate_contributions(directory, plugin, manifest)
    validate_permissions(plugin, manifest)

    readme = directory / "README.md"
    if not readme.is_file():
        plugin["warnings"].append("missing README.md")


def plugin_summary(plugin: dict[str, Any]) -> dict[str, Any]:
    manifest = plugin.get("manifest") or {}
    contributions = manifest.get("contributions") if isinstance(manifest.get("contributions"), dict) else {}
    permissions = manifest.get("permissions") if isinstance(manifest.get("permissions"), dict) else {}
    return {
        "name": plugin["name"],
        "path": plugin["path"],
        "description": manifest.get("description", ""),
        "version": manifest.get("version", ""),
        "publisher": manifest.get("publisher", ""),
        "source": manifest.get("source", ""),
        "contributions": contributions,
        "permissions": permissions,
        "status": "fail" if plugin["errors"] else "pass",
        "errors": plugin["errors"],
        "warnings": plugin["warnings"],
    }


def payload(root: Path) -> dict[str, Any]:
    config = load_config(root)
    discovered = discover_plugins(root, config)
    failures = [f"{plugin['name']}: {error}" for plugin in discovered for error in plugin["errors"]]
    warnings = [f"{plugin['name']}: {warning}" for plugin in discovered for warning in plugin["warnings"]]
    return {
        "flywheel_plugins": {
            "status": "pass" if not failures else "fail",
            "plugins_path": rel(root, plugins_dir(root, config)),
            "plugins": [plugin_summary(plugin) for plugin in discovered],
            "failures": failures,
            "warnings": warnings,
        }
    }


def print_text(data: dict[str, Any], command: str) -> None:
    plugins = data["flywheel_plugins"]
    if command == "list":
        if not plugins["plugins"]:
            print(f"no plugins installed ({plugins['plugins_path']})")
            return
        for plugin in plugins["plugins"]:
            print(f"{plugin['name']} {plugin['version']} - {plugin['description']}")
        return

    for failure in plugins["failures"]:
        print(f"FAIL: {failure}")
    for warning in plugins["warnings"]:
        print(f"WARN: {warning}")
    if not plugins["failures"]:
        print("PASS: flywheel plugins")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage Flywheel plugins")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("list", "doctor"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--format", choices=("text", "json"), default="text")

    args = parser.parse_args()
    root = repo_root(Path(__file__))
    data = payload(root)

    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        print_text(data, args.command)
    return 0 if data["flywheel_plugins"]["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
