# Repository Guidelines

## Project Structure & Module Organization
`geepers` combines a Python package and a skills ecosystem.
- `geepers/`: Python package (orchestrators, MCP stdio servers, naming, utilities).
- `skills/source/<skill-name>/SKILL.md`: canonical skill definitions.
- `agents/`: markdown agent definitions used by plugin packaging.
- `.claude-plugin/marketplace.json`: plugin marketplace manifest.
- `scripts/`, `reports/`, `status/`: operational tooling and generated artifacts.

## Build, Test, and Development Commands
Use package and skill checks together.

```bash
# Install package for local development
python3 -m pip install -e .

# Build-check Python code
python3 -m compileall geepers

# Validate skill files are present
find skills/source -mindepth 2 -maxdepth 2 -name SKILL.md | sort

# Verify frontmatter keys in source skills
rg -n "^(name|description):" skills/source/*/SKILL.md
```

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indentation, explicit function names.
- Skills/agents: concise Markdown with actionable triggers and examples.
- Skill names should remain lowercase kebab-case and match folder names.
- Keep routing/orchestration terms consistent across `skills/source/`, `agents/`, and docs.

## Testing Guidelines
- No single test suite is enforced here; run targeted validation for changed areas.
- For package changes, run compile checks and smoke-test key entry points after editable install.
- For skill changes, validate frontmatter and run at least one manual invocation path.

## Commit & Pull Request Guidelines
Current history uses operational prefixes (`session checkpoint:`) plus semantic prefixes (`sync:`, `feat:`).
- Follow the existing style for continuity.
- Keep commits focused (package logic vs. skill content vs. docs).
- PRs should state scope, validation steps, and any migration impact for skill names/routes.

## Security & Configuration Tips
- Never commit secrets (tokens, private keys, credentials files).
- Exclude generated logs/reports/temp output unless intentionally versioned.
- Review package metadata (`pyproject.toml`) when adding dependencies or CLI entry points.
