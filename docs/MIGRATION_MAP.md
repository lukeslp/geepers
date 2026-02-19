# Migration Map

## Repository rename
- Canonical public name: `geepers-api-skills`
- Legacy alias: `dreamer-api-skills`

## Environment variable migration
- Preferred: `GEEPERS_API_KEY`
- Legacy alias supported: `DREAMER_API_KEY`

## Skill alias mapping
- `dreamer-corpus` -> `geepers-corpus`
- `dreamer-data` -> `geepers-data`
- `dreamer-etymology` -> `geepers-etymology`
- `dreamer-llm` -> `geepers-llm`
- `dreamer-orchestrate` -> `geepers-orchestrate`

## Transition policy
- New documentation and build artifacts use canonical names.
- Legacy names remain documented as aliases for one release cycle.
- Mirror repositories should consume built artifacts only.
