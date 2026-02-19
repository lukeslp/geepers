#!/usr/bin/env python3
"""Validate canonical skill manifests and SKILL frontmatter."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "skills-manifest.yaml"
PLATFORMS_PATH = ROOT / "manifests" / "platforms.yaml"
ALIASES_PATH = ROOT / "manifests" / "aliases.yaml"

NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return data


def parse_frontmatter(skill_md: Path) -> Dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end_idx = None
    for i in range(1, min(len(lines), 120)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}

    raw = "\n".join(lines[1:end_idx])
    parsed = yaml.safe_load(raw) or {}
    if not isinstance(parsed, dict):
        return {}
    return parsed


def detect_alias_cycles(alias_edges: Dict[str, str]) -> List[List[str]]:
    cycles: List[List[str]] = []
    visiting = set()
    visited = set()

    def dfs(node: str, stack: List[str]) -> None:
        if node in visiting:
            if node in stack:
                idx = stack.index(node)
                cycles.append(stack[idx:] + [node])
            return
        if node in visited:
            return

        visiting.add(node)
        stack.append(node)
        nxt = alias_edges.get(node)
        if nxt is not None:
            dfs(nxt, stack)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in alias_edges:
        if node not in visited:
            dfs(node, [])
    return cycles


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate geepers skill manifests and source skills.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors.")
    args = parser.parse_args()

    errors: List[str] = []
    warnings: List[str] = []

    try:
        manifest = load_yaml(MANIFEST_PATH)
        platforms_cfg = load_yaml(PLATFORMS_PATH)
        aliases = load_yaml(ALIASES_PATH)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}")
        return 1

    skills = manifest.get("skills", [])
    defaults = manifest.get("defaults", {})
    default_platforms = defaults.get("platforms", [])
    valid_platforms = set((platforms_cfg.get("platforms") or {}).keys())

    if not isinstance(skills, list) or not skills:
        errors.append("manifests/skills-manifest.yaml must define a non-empty skills list.")
        skills = []

    skill_ids = []

    for entry in skills:
        if not isinstance(entry, dict):
            errors.append(f"Skill entry is not an object: {entry!r}")
            continue

        skill_id = entry.get("id")
        source_path = entry.get("source_path")
        bundles = entry.get("bundles")
        allow_legacy_name = bool(entry.get("allow_legacy_name", False))

        if not isinstance(skill_id, str) or not skill_id:
            errors.append(f"Skill entry missing valid id: {entry}")
            continue

        if not NAME_PATTERN.match(skill_id):
            errors.append(f"Skill id '{skill_id}' must be lowercase kebab-case.")

        skill_ids.append(skill_id)

        if not isinstance(source_path, str) or not source_path:
            errors.append(f"Skill '{skill_id}' missing source_path.")
            continue

        if not isinstance(bundles, list) or not bundles:
            errors.append(f"Skill '{skill_id}' must define at least one bundle.")

        source_dir = ROOT / source_path
        if not source_dir.exists() or not source_dir.is_dir():
            errors.append(f"Skill '{skill_id}' source directory not found: {source_path}")
            continue

        skill_md = source_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"Skill '{skill_id}' missing SKILL.md at {source_path}/SKILL.md")
            continue

        fm = parse_frontmatter(skill_md)
        if not fm:
            errors.append(f"Skill '{skill_id}' has missing/invalid YAML frontmatter in {source_path}/SKILL.md")
        else:
            name = fm.get("name")
            description = fm.get("description")

            if not isinstance(name, str) or not name.strip():
                errors.append(f"Skill '{skill_id}' frontmatter missing 'name'.")
            elif not NAME_PATTERN.match(name):
                msg = f"Skill '{skill_id}' frontmatter name '{name}' is not kebab-case."
                if allow_legacy_name:
                    warnings.append(msg + " (allowed by allow_legacy_name)")
                else:
                    errors.append(msg)

            if isinstance(name, str) and name.strip() and name != skill_id:
                msg = f"Skill '{skill_id}' frontmatter name '{name}' does not match id."
                if allow_legacy_name:
                    warnings.append(msg + " (allowed by allow_legacy_name)")
                else:
                    warnings.append(msg)

            if not isinstance(description, str) or not description.strip():
                errors.append(f"Skill '{skill_id}' frontmatter missing 'description'.")

        platforms = entry.get("platforms", default_platforms)
        if not isinstance(platforms, list) or not platforms:
            errors.append(f"Skill '{skill_id}' has no platforms configured.")
        else:
            for platform in platforms:
                if platform not in valid_platforms:
                    errors.append(
                        f"Skill '{skill_id}' references unknown platform '{platform}'. "
                        f"Known platforms: {sorted(valid_platforms)}"
                    )

    # Duplicate IDs
    seen = set()
    for skill_id in skill_ids:
        if skill_id in seen:
            errors.append(f"Duplicate skill id found: {skill_id}")
        seen.add(skill_id)

    # Validate aliases
    skill_aliases = aliases.get("skill_aliases", [])
    alias_edges: Dict[str, str] = {}

    if not isinstance(skill_aliases, list):
        errors.append("manifests/aliases.yaml skill_aliases must be a list.")
        skill_aliases = []

    for item in skill_aliases:
        if not isinstance(item, dict):
            errors.append(f"Invalid alias item: {item!r}")
            continue
        frm = item.get("from")
        to = item.get("to")
        if not isinstance(frm, str) or not isinstance(to, str):
            errors.append(f"Alias entries must include string from/to: {item!r}")
            continue
        if frm in alias_edges:
            errors.append(f"Duplicate alias source '{frm}' in aliases.yaml")
        alias_edges[frm] = to
        if to not in seen:
            errors.append(f"Alias target '{to}' does not exist in skills-manifest skill ids.")

    for cycle in detect_alias_cycles(alias_edges):
        errors.append(f"Alias cycle detected: {' -> '.join(cycle)}")

    print("Validation summary")
    print(f"- Skills declared: {len(skills)}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"  - {item}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"  - {item}")

    if args.strict and warnings:
        print("\nStrict mode enabled: warnings are treated as failures.")
        return 1

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
