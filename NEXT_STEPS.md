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

Language cleanup is complete in the canonical repo:
- removed "generated ..." framing in scripts, docs, and platform metadata
- replaced mirror guard wording with "synced mirror"
- `README.generated.md` replaced by `README.md` (humanized) + `SYNC_INFO.md` (build metadata)
- build script now copies humanized README templates from `scripts/platform-readmes/` on every build

## Immediate Follow-Up

1. Push latest canonical commits to the GitHub remote.
2. Run `sync-mirrors.sh` to propagate updated platform packages to all mirror repos.
3. Keep `geepers` as the only authoring source for shared skill content.
4. Continue enforcing read-only mirror policy in every mirror repo.

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
