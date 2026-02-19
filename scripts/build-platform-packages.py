#!/usr/bin/env python3
"""Build platform-specific skill packages from canonical manifest."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "skills-manifest.yaml"
PLATFORMS_PATH = ROOT / "manifests" / "platforms.yaml"
ALIASES_PATH = ROOT / "manifests" / "aliases.yaml"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be an object: {path}")
    return data


def rm_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def copy_skill(src: Path, dst: Path) -> None:
    def ignore_filter(_: str, names: List[str]) -> set:
        ignore = set()
        for name in names:
            if name in {".git", "__pycache__", ".DS_Store", ".pytest_cache"}:
                ignore.add(name)
            if name.endswith((".pyc", ".pyo", ".swp", ".swo")):
                ignore.add(name)
        return ignore

    shutil.copytree(src, dst, ignore=ignore_filter)


def selected_skills(manifest: dict, platform_name: str, include_bundles: set) -> List[dict]:
    defaults = manifest.get("defaults", {})
    default_platforms = defaults.get("platforms", [])
    selected = []

    for skill in manifest.get("skills", []):
        bundles = set(skill.get("bundles", []))
        platforms = set(skill.get("platforms", default_platforms))

        if platform_name not in platforms:
            continue
        if include_bundles and not (bundles & include_bundles):
            continue

        selected.append(skill)

    return selected


def generate_platform_metadata(platform: str, output_root: Path, skills: List[dict], aliases: dict) -> None:
    skill_names = [skill["id"] for skill in skills]

    if platform == "claude":
        payload = {
            "name": "geepers-marketplace",
            "owner": {
                "name": "Luke Steuber",
                "email": "luke@dr.eamer.dev"
            },
            "metadata": {
                "description": "Skill package for Claude-compatible clients.",
                "version": "1.0.0",
                "built_at": datetime.now(timezone.utc).isoformat()
            },
            "plugins": [
                {
                    "name": "geepers-skills-package",
                    "description": "Synced from canonical geepers manifest",
                    "source": "./",
                    "strict": False,
                    "skills": [f"./skills/{name}" for name in skill_names]
                }
            ]
        }
        target = output_root / ".claude-plugin" / "marketplace.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    elif platform == "gemini":
        payload = {
            "name": "geepers-gemini-package",
            "version": "1.0.0",
            "description": "Gemini extension package synced from canonical geepers skills.",
            "built_at": datetime.now(timezone.utc).isoformat(),
            "skills": [{"name": name, "path": f"skills/{name}"} for name in skill_names],
            "aliases": aliases.get("skill_aliases", [])
        }
        target = output_root / "gemini-extension.json"
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    elif platform == "manus":
        payload = {
            "name": "geepers-manus-package",
            "version": "1.0.0",
            "runtime": "manus",
            "built_at": datetime.now(timezone.utc).isoformat(),
            "skills": [{"id": name, "path": f"skills/{name}"} for name in skill_names]
        }
        target = output_root / "manus-skills.json"
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    elif platform == "clawhub":
        payload = {
            "name": "geepers-api-skills",
            "legacy_aliases": ["dreamer-api-skills"],
            "version": "1.0.0",
            "distribution": "clawhub",
            "built_at": datetime.now(timezone.utc).isoformat(),
            "skills": [{"id": name, "path": f"skills/{name}"} for name in skill_names]
        }
        target = output_root / "clawhub-package.json"
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    else:  # codex and fallback
        payload = {
            "name": f"geepers-{platform}-package",
            "version": "1.0.0",
            "built_at": datetime.now(timezone.utc).isoformat(),
            "skills": [{"id": name, "path": f"skills/{name}"} for name in skill_names]
        }
        target = output_root / f"{platform}-package.json"
        target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_generated_readme(platform: str, output_root: Path, skill_count: int) -> None:
    content = f"""# {platform.title()} Skill Package

This directory is synced from canonical source in `geepers/manifests/skills-manifest.yaml`.

- Platform: `{platform}`
- Skill count: `{skill_count}`
- Built at: `{datetime.now(timezone.utc).isoformat()}`

Rebuild with:

```bash
python3 scripts/build-platform-packages.py --platform {platform} --clean
```
"""
    (output_root / "README.generated.md").write_text(content, encoding="utf-8")


def build_one(platform_name: str, manifest: dict, platforms_cfg: dict, aliases: dict, clean: bool) -> int:
    platform_cfg = (platforms_cfg.get("platforms") or {}).get(platform_name)
    if not platform_cfg:
        print(f"ERROR: Unknown platform '{platform_name}'")
        return 1

    output_root = ROOT / platform_cfg["output_root"]
    include_bundles = set(platform_cfg.get("include_bundles", []))

    if clean:
        rm_tree(output_root)

    output_root.mkdir(parents=True, exist_ok=True)
    skills_root = output_root / platform_cfg.get("skills_dir", "skills")
    skills_root.mkdir(parents=True, exist_ok=True)

    selected = selected_skills(manifest, platform_name, include_bundles)

    # Copy selected skills
    copied = []
    for skill in selected:
        source = ROOT / skill["source_path"]
        target_name = (skill.get("target_names") or {}).get(platform_name, skill["id"])
        destination = skills_root / target_name
        if destination.exists():
            shutil.rmtree(destination)
        copy_skill(source, destination)
        copied.append(target_name)

    aliases_path = output_root / "aliases.json"
    aliases_path.write_text(json.dumps(aliases, indent=2) + "\n", encoding="utf-8")

    generated_manifest = {
        "platform": platform_name,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "source_manifest": str(MANIFEST_PATH.relative_to(ROOT)),
        "skills": copied,
    }
    (output_root / "manifest.generated.json").write_text(
        json.dumps(generated_manifest, indent=2) + "\n", encoding="utf-8"
    )

    generate_platform_metadata(platform_name, output_root, selected, aliases)
    write_generated_readme(platform_name, output_root, len(copied))

    print(f"Built {platform_name}: {len(copied)} skills -> {output_root}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build platform skill packages from canonical manifest.")
    parser.add_argument(
        "--platform",
        default="all",
        choices=["all", "claude", "codex", "gemini", "manus", "clawhub"],
        help="Platform to build (default: all).",
    )
    parser.add_argument("--clean", action="store_true", help="Delete output directory before building.")
    args = parser.parse_args()

    manifest = load_yaml(MANIFEST_PATH)
    platforms_cfg = load_yaml(PLATFORMS_PATH)
    aliases = load_yaml(ALIASES_PATH)

    if args.platform == "all":
        rc = 0
        for platform in ["claude", "codex", "gemini", "manus", "clawhub"]:
            rc |= build_one(platform, manifest, platforms_cfg, aliases, clean=args.clean)
        return rc

    return build_one(args.platform, manifest, platforms_cfg, aliases, clean=args.clean)


if __name__ == "__main__":
    raise SystemExit(main())
