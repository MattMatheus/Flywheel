#!/usr/bin/env python3
"""Display configured Flywheel workflow lanes."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from flywheel_config import DOMAINS, LANES, load_config, path, rel, repo_root

METADATA_RE = re.compile(r"^\s*-\s*`(?P<key>[^`]+)`:\s*(?P<value>.*)$")
QUEUE_ITEM_RE = re.compile(r"^\s*\d+\.\s*`([^`]+)`.*$")
FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)


def metadata(file_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        for line in file_path.read_text(encoding="utf-8").splitlines():
            match = METADATA_RE.match(line)
            if match:
                values[match.group("key")] = match.group("value").strip()
    except UnicodeDecodeError:
        values["__decode_error__"] = "true"
    return values


def frontmatter(file_path: Path) -> dict[str, str]:
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"__decode_error__": "true"}
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}

    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def title(file_path: Path) -> str:
    try:
        for line in file_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    except UnicodeDecodeError:
        return ""
    return ""


def queue_order(lane_dir: Path) -> list[str]:
    readme = lane_dir / "README.md"
    if not readme.is_file():
        return []

    ordered = []
    for line in readme.read_text(encoding="utf-8").splitlines():
        match = QUEUE_ITEM_RE.match(line)
        if match:
            ordered.append(Path(match.group(1)).name)
    return ordered


def lane_items(root: Path, lane_dir: Path) -> list[dict[str, Any]]:
    files = {item.name: item for item in sorted(lane_dir.glob("*.md")) if item.name != "README.md" and item.is_file()}
    ordered_names = [name for name in queue_order(lane_dir) if name in files]
    remaining_names = [name for name in sorted(files) if name not in ordered_names]
    names = ordered_names + remaining_names

    items = []
    for index, name in enumerate(names, 1):
        file_path = files[name]
        values = metadata(file_path)
        fm = frontmatter(file_path)
        items.append(
            {
                "order": index,
                "path": rel(root, file_path),
                "filename": file_path.name,
                "id": values.get("id") or fm.get("id") or file_path.stem,
                "kind": fm.get("kind", ""),
                "status": values.get("status") or fm.get("status", ""),
                "ready": fm.get("ready", ""),
                "title": title(file_path),
                "metadata": values,
                "frontmatter": fm,
            }
        )
    return items


def payload(root: Path) -> dict[str, Any]:
    config = load_config(root)
    domains = []
    total_items = 0

    for domain in DOMAINS:
        lanes = []
        for lane in LANES:
            lane_dir = path(root, config, f"paths.{domain}.{lane}")
            items = lane_items(root, lane_dir) if lane_dir.is_dir() else []
            total_items += len(items)
            lanes.append(
                {
                    "name": lane,
                    "path": rel(root, lane_dir),
                    "exists": lane_dir.is_dir(),
                    "item_count": len(items),
                    "items": items,
                }
            )
        domains.append({"name": domain, "lanes": lanes})

    return {
        "flywheel_lanes": {
            "status": "pass",
            "total_items": total_items,
            "domains": domains,
        }
    }


def print_text(data: dict[str, Any]) -> None:
    lanes = data["flywheel_lanes"]
    for domain in lanes["domains"]:
        print(domain["name"])
        for lane in domain["lanes"]:
            count = lane["item_count"]
            print(f"  {lane['name']} ({count})")
            for item in lane["items"]:
                label = item["id"] or item["filename"]
                title_text = f" - {item['title']}" if item["title"] and item["title"] != label else ""
                print(f"    {item['order']}. {label}{title_text}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Show configured Flywheel lanes")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    root = repo_root(Path(__file__))
    data = payload(root)
    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        print_text(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
