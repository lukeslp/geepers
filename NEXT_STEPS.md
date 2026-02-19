# Next Steps

## Current Status

Platform mirrors are now aligned on the same 23-skill set:
- Claude mirror: `geepers-skills`
- Codex/GPT mirror: `geepers-gpt`
- Gemini mirror: `geepers-gemini`
- Manus mirror: `geepers-manus`
- OpenClaw/ClawHub mirror: `geepers-api-skills`

The build/sync pipeline is active from canonical source in `geepers`:
- `python3 scripts/build-platform-packages.py --platform all --clean`
- `bash scripts/sync-mirrors.sh --platform all --delete --skip-build`
- `bash scripts/report-drift.sh --platform all --skip-missing`

Language cleanup is in progress across mirrors:
- removed "generated ..." framing in top-level docs and metadata
- replaced mirror guard wording with "synced mirror"

## Immediate Follow-Up

1. Commit and push the current wording/metadata cleanup in all affected repos.
2. Keep `geepers` as the only authoring source for shared skill content.
3. Continue enforcing read-only mirror policy in every mirror repo.
4. Confirm top-level README style remains consistent after future sync runs.

## Future Tasks

1. Add a lightweight lint check that fails PRs when banned wording appears in top-level docs.
2. Add a `docs-sync` helper script to update mirror README/AGENTS files in one step.
3. Add an automated release checklist for all platform mirrors.
4. Add a quarterly audit for alias mappings and migration notes.

## Command Reference

```bash
# Validate + rebuild all platform packages
python3 scripts/validate-skills.py --strict
python3 scripts/build-platform-packages.py --platform all --clean

# Sync all mirrors and verify parity
bash scripts/sync-mirrors.sh --platform all --delete --skip-build
bash scripts/report-drift.sh --platform all --skip-missing
```
