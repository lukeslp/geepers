#!/usr/bin/env python3
"""Package all geepers agents as proper Claude Code skills.

Reads agent markdown files from agents/, generates SKILL.md files,
and creates skill source directories in skills/source/.
"""

import os
import re
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
AGENTS_DIR = REPO_ROOT / "agents"
SOURCE_DIR = SCRIPT_DIR / "source"

# Mapping: skill-name -> { type, files, description_override }
# type: "orchestrator" (category with orchestrator + sub-agents)
#       "standalone" (individual agent)
#       "existing" (already has a skill, skip)

SKILL_MAP = {
    # === ORCHESTRATOR CATEGORIES (new) ===
    "conductor": {
        "type": "standalone",
        "files": ["master/geepers_conductor.md"],
    },
    "checkpoint": {
        "type": "orchestrator",
        "orchestrator": "checkpoint/geepers_orchestrator_checkpoint.md",
        "agents": [
            "checkpoint/geepers_scout.md",
            "checkpoint/geepers_repo.md",
            "checkpoint/geepers_status.md",
            "checkpoint/geepers_snippets.md",
        ],
    },
    "corpus": {
        "type": "orchestrator",
        "orchestrator": "corpus/geepers_orchestrator_corpus.md",
        "agents": [
            "corpus/geepers_corpus.md",
            "corpus/geepers_corpus_ux.md",
        ],
    },
    "deploy": {
        "type": "orchestrator",
        "orchestrator": "deploy/geepers_orchestrator_deploy.md",
        "agents": [
            "deploy/geepers_caddy.md",
            "deploy/geepers_services.md",
            "deploy/geepers_validator.md",
        ],
    },
    "frontend": {
        "type": "orchestrator",
        "orchestrator": "frontend/geepers_orchestrator_frontend.md",
        "agents": [
            "frontend/geepers_css.md",
            "frontend/geepers_design.md",
            "frontend/geepers_motion.md",
            "frontend/geepers_typescript.md",
            "frontend/geepers_uxpert.md",
            "frontend/geepers_webperf.md",
        ],
    },
    "fullstack": {
        "type": "orchestrator",
        "orchestrator": "fullstack/geepers_orchestrator_fullstack.md",
        "agents": [
            "fullstack/geepers_db.md",
            "fullstack/geepers_react.md",
        ],
    },
    "games": {
        "type": "orchestrator",
        "orchestrator": "games/geepers_orchestrator_games.md",
        "agents": [
            "games/geepers_game.md",
            "games/geepers_gamedev.md",
            "games/geepers_godot.md",
        ],
    },
    "hive": {
        "type": "orchestrator",
        "orchestrator": "hive/geepers_orchestrator_hive.md",
        "agents": [
            "hive/geepers_builder.md",
            "hive/geepers_integrator.md",
            "hive/geepers_planner.md",
            "hive/geepers_quickwin.md",
            "hive/geepers_refactor.md",
        ],
    },
    "python-dev": {
        "type": "orchestrator",
        "orchestrator": "python/geepers_orchestrator_python.md",
        "agents": [
            "python/geepers_pycli.md",
        ],
    },
    "quality": {
        "type": "orchestrator",
        "orchestrator": "quality/geepers_orchestrator_quality.md",
        "agents": [
            "quality/geepers_a11y.md",
            "quality/geepers_critic.md",
            "quality/geepers_deps.md",
            "quality/geepers_perf.md",
            "quality/geepers_security.md",
            "quality/geepers_testing.md",
        ],
    },
    "research": {
        "type": "orchestrator",
        "orchestrator": "research/geepers_orchestrator_research.md",
        "agents": [
            "research/geepers_citations.md",
            "research/geepers_data.md",
            "research/geepers_diag.md",
            "research/geepers_fetcher.md",
            "research/geepers_links.md",
            "research/geepers_searcher.md",
        ],
    },
    "web-dev": {
        "type": "orchestrator",
        "orchestrator": "web/geepers_orchestrator_web.md",
        "agents": [
            "web/geepers_express.md",
            "web/geepers_flask.md",
        ],
    },
    # === STANDALONE AGENTS (new) ===
    "api-design": {
        "type": "standalone",
        "files": ["standalone/geepers_api.md"],
    },
    "canary": {
        "type": "standalone",
        "files": ["standalone/geepers_canary.md"],
    },
    "dashboard": {
        "type": "standalone",
        "files": ["standalone/geepers_dashboard.md"],
    },
    "docs": {
        "type": "standalone",
        "files": ["standalone/geepers_docs.md"],
    },
    "git-ops": {
        "type": "standalone",
        "files": ["standalone/geepers_git.md"],
    },
    "janitor": {
        "type": "standalone",
        "files": ["standalone/geepers_janitor.md"],
    },
    "scalpel": {
        "type": "standalone",
        "files": ["standalone/geepers_scalpel.md"],
    },
    "todoist": {
        "type": "standalone",
        "files": ["standalone/geepers_todoist.md"],
    },
    "humanize": {
        "type": "standalone",
        "files": ["standalone/geepers_humanizer.md"],
    },
    # === SYSTEM AGENTS (new) ===
    "system-diag": {
        "type": "standalone",
        "files": ["system/geepers_system_diag.md"],
    },
    "system-help": {
        "type": "standalone",
        "files": ["system/geepers_system_help.md"],
    },
    "system-onboard": {
        "type": "standalone",
        "files": ["system/geepers_system_onboard.md"],
    },
    # === DATAVIS individual agents (not in existing datavis skill) ===
    "datavis-agents": {
        "type": "orchestrator",
        "orchestrator": "datavis/geepers_orchestrator_datavis.md",
        "agents": [
            "datavis/geepers_datavis_color.md",
            "datavis/geepers_datavis_data.md",
            "datavis/geepers_datavis_math.md",
            "datavis/geepers_datavis_story.md",
            "datavis/geepers_datavis_viz.md",
        ],
    },
}


def parse_agent_md(filepath):
    """Parse an agent markdown file, returning frontmatter dict and body."""
    content = filepath.read_text()

    # Parse YAML frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---\n?(.*)', content, re.DOTALL)
    if not fm_match:
        return {}, content

    fm_text = fm_match.group(1)
    body = fm_match.group(2)

    frontmatter = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            frontmatter[key] = val

    return frontmatter, body


def clean_description(desc):
    """Extract just the first sentence/clause of description, removing examples."""
    # Remove escaped newlines and everything after
    desc = desc.split('\\n')[0]
    # Remove example blocks
    desc = re.sub(r'<example>.*?</example>', '', desc, flags=re.DOTALL)
    # Clean up
    desc = desc.strip().rstrip('.')
    return desc + '.'


def generate_skill_md(name, frontmatter, body):
    """Generate a SKILL.md from agent frontmatter and body."""
    desc = clean_description(frontmatter.get('description', f'{name} agent skill.'))
    agent_name = frontmatter.get('name', name)

    skill_md = f"""---
name: {agent_name}
description: "{desc}"
---

{body.strip()}
"""
    return skill_md


def generate_orchestrator_skill_md(skill_name, orch_fm, orch_body, agent_files):
    """Generate a SKILL.md for an orchestrator category with sub-agent reference."""
    desc = clean_description(orch_fm.get('description', f'{skill_name} orchestrator skill.'))
    orch_name = orch_fm.get('name', skill_name)

    # Build agent reference section
    agent_ref_lines = ["\n## Included Agent Definitions\n"]
    agent_ref_lines.append("The following agent files are included in this skill's `agents/` directory:\n")
    for af in agent_files:
        af_path = AGENTS_DIR / af
        if af_path.exists():
            af_fm, _ = parse_agent_md(af_path)
            af_name = af_fm.get('name', af_path.stem)
            af_desc = clean_description(af_fm.get('description', ''))
            agent_ref_lines.append(f"- **{af_name}**: {af_desc}")

    agent_ref = "\n".join(agent_ref_lines)

    skill_md = f"""---
name: {orch_name}
description: "{desc}"
---

{orch_body.strip()}
{agent_ref}
"""
    return skill_md


def package_skill(skill_name, config):
    """Create a skill source directory with SKILL.md and agent files."""
    skill_dir = SOURCE_DIR / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    if config["type"] == "standalone":
        # Single agent -> SKILL.md
        agent_file = AGENTS_DIR / config["files"][0]
        if not agent_file.exists():
            print(f"  SKIP {skill_name}: {agent_file} not found")
            return False

        fm, body = parse_agent_md(agent_file)
        skill_md = generate_skill_md(skill_name, fm, body)
        (skill_dir / "SKILL.md").write_text(skill_md)

    elif config["type"] == "orchestrator":
        # Orchestrator + sub-agents
        orch_file = AGENTS_DIR / config["orchestrator"]
        if not orch_file.exists():
            print(f"  SKIP {skill_name}: {orch_file} not found")
            return False

        orch_fm, orch_body = parse_agent_md(orch_file)
        agent_files = config.get("agents", [])

        skill_md = generate_orchestrator_skill_md(
            skill_name, orch_fm, orch_body, agent_files
        )
        (skill_dir / "SKILL.md").write_text(skill_md)

        # Copy agent .md files into agents/ subdir for reference
        agents_subdir = skill_dir / "agents"
        agents_subdir.mkdir(exist_ok=True)
        for af in agent_files:
            src = AGENTS_DIR / af
            if src.exists():
                dst = agents_subdir / src.name
                shutil.copy2(src, dst)

    print(f"  OK {skill_name}/SKILL.md")
    return True


def main():
    print(f"Agents dir: {AGENTS_DIR}")
    print(f"Skills source dir: {SOURCE_DIR}")
    print(f"\nPackaging {len(SKILL_MAP)} skills...\n")

    created = 0
    skipped = 0

    for skill_name, config in sorted(SKILL_MAP.items()):
        if package_skill(skill_name, config):
            created += 1
        else:
            skipped += 1

    print(f"\nDone: {created} created, {skipped} skipped")
    print(f"\nTotal skill source dirs: {len(list(SOURCE_DIR.iterdir()))}")


if __name__ == "__main__":
    main()
