# Skills Unification Architecture

## Goal
Use `/home/coolhand/geepers` as the canonical source of skill content, then generate platform-specific distributions for Claude, Codex, Gemini, Manus, and ClawHub.

## Layers
1. Canonical content layer
- Canonical skills live in `skills/source/<skill-id>/`.
- Canonical metadata lives in `manifests/skills-manifest.yaml`.
- Migration aliases live in `manifests/aliases.yaml`.

2. Platform adapter layer
- Adapter config lives in `manifests/platforms.yaml`.
- `scripts/build-platform-packages.py` generates platform outputs under `platforms/<platform>/`.

3. Mirror synchronization layer
- `scripts/sync-mirrors.sh` pushes generated outputs to mirror repos.
- `scripts/report-drift.sh` compares generated outputs with mirror repos.

## Read-only mirror policy
Mirror repos are distribution surfaces, not authoring surfaces. Skill edits should be made only in canonical source directories and propagated through adapter build + sync.

## Validation flow
1. `python3 scripts/validate-skills.py --strict`
2. `python3 scripts/build-platform-packages.py --platform all --clean`
3. `bash scripts/report-drift.sh --strict --skip-missing`

## Design constraints
- Keep platform adapters deterministic.
- Preserve backward compatibility via alias maps.
- Do not hardcode secrets in generated manifests.
- Keep migration metadata explicit and auditable.
