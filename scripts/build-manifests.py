#!/usr/bin/env python3
"""Generate platform manifests from the shared skills/ directory.

Scans skills/*/SKILL.md to build the skill list, then generates:
  - manus-skills.json     (Manus platform)
  - codex-package.json    (Codex/OpenAI platform)
  - clawhub-package.json  (Clawhub/OpenClaw platform)

Also updates .claude-plugin/marketplace.json with the current skill list.

Usage:
    python3 scripts/build-manifests.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = REPO_ROOT / "skills"
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"


def get_version():
    """Read version from plugin.json."""
    data = json.loads(PLUGIN_JSON.read_text())
    return data.get("version", "1.0.0")


def discover_skills():
    """Find all skill directories that contain SKILL.md."""
    skills = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            skills.append({
                "id": f"geepers-{skill_dir.name}",
                "path": f"skills/{skill_dir.name}",
            })
    return skills


def build_manus(skills, version):
    """Generate manus-skills.json."""
    return {
        "name": "geepers-manus-package",
        "version": version,
        "runtime": "manus",
        "built_at": datetime.now(timezone.utc).isoformat(),
        "skills": skills,
    }


def build_codex(skills, version):
    """Generate codex-package.json."""
    return {
        "name": "geepers-codex-package",
        "version": version,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "skills": skills,
    }


def build_clawhub(skills, version):
    """Generate clawhub-package.json."""
    return {
        "name": "geepers-clawhub-package",
        "version": version,
        "distribution": "clawhub",
        "legacy_aliases": ["dreamer-api-skills"],
        "built_at": datetime.now(timezone.utc).isoformat(),
        "skills": skills,
    }


def update_marketplace(skills):
    """Update .claude-plugin/marketplace.json with current skill list."""
    data = json.loads(MARKETPLACE_JSON.read_text())

    # Add skill listing to the first plugin entry
    if data.get("plugins"):
        data["plugins"][0]["skills"] = [s["id"] for s in skills]
        data["plugins"][0]["skill_count"] = len(skills)

    MARKETPLACE_JSON.write_text(json.dumps(data, indent=2) + "\n")
    return data


def write_manifest(filename, data):
    """Write a JSON manifest to repo root."""
    path = REPO_ROOT / filename
    path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"  {filename}: {len(data['skills'])} skills")


def main():
    version = get_version()
    skills = discover_skills()
    print(f"Geepers v{version} — {len(skills)} skills discovered\n")

    if not skills:
        print("No skills found. Check that skills/*/SKILL.md exists.")
        sys.exit(1)

    print("Generating platform manifests:")
    write_manifest("manus-skills.json", build_manus(skills, version))
    write_manifest("codex-package.json", build_codex(skills, version))
    write_manifest("clawhub-package.json", build_clawhub(skills, version))

    print("\nUpdating marketplace.json:")
    update_marketplace(skills)
    print(f"  {len(skills)} skills listed")

    print("\nDone.")


if __name__ == "__main__":
    main()
