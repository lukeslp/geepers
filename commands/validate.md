---
description: Unified validation - links, data, APIs, configs, citations, services - routes to appropriate specialist
---

# Validate Mode

Run targeted validation checks by routing to the appropriate specialist agent.

## Validation Types

| Mode | Agent | What It Checks |
|------|-------|----------------|
| `links` | @geepers_links | URLs in docs, broken links, resource lists |
| `data` | @geepers_data | Dataset quality, freshness, source accuracy |
| `api` | @geepers_api | REST compliance, endpoint consistency, breaking changes |
| `config` | @geepers_validator | Paths, permissions, integrations, project health |
| `citations` | @geepers_citations | References, fact-checking, source verification |
| `deps` | @geepers_deps | Dependencies, vulnerabilities, licenses |
| `services` | @geepers_canary | Service health, critical system spot-checks |

## Usage

```
/geepers-validate links      # Check URLs in current project
/geepers-validate data       # Audit dataset quality
/geepers-validate api        # Review API design
/geepers-validate config     # Verify paths and configs
/geepers-validate citations  # Fact-check references
/geepers-validate deps       # Dependency audit
/geepers-validate services   # Quick health check
/geepers-validate all        # Run ALL validators in PARALLEL
```

## Parallel Execution

For `/geepers-validate all`, launch these simultaneously:
1. @geepers_links
2. @geepers_data (if datasets present)
3. @geepers_api (if API endpoints present)
4. @geepers_validator
5. @geepers_deps
6. @geepers_canary

## Mode-Specific Details

### Links (`/geepers-validate links`)
- Scans markdown, HTML, and code for URLs
- Tests reachability (HEAD requests)
- Suggests replacements for dead links
- Enriches resource lists with descriptions

### Data (`/geepers-validate data`)
- Checks dataset freshness (when last updated)
- Validates against authoritative sources
- Identifies enrichment opportunities
- Flags inconsistencies and outliers

### API (`/geepers-validate api`)
- REST naming conventions
- Consistent response formats
- Breaking change detection
- Documentation completeness

### Config (`/geepers-validate config`)
- File paths exist and are accessible
- Environment variables set
- Service configurations valid
- Cross-project dependencies resolved

### Citations (`/geepers-validate citations`)
- Academic reference accuracy
- Claim verification against sources
- Link to original sources
- Confidence scoring

### Deps (`/geepers-validate deps`)
- Security vulnerabilities (CVEs)
- Outdated packages
- License compliance
- Upgrade impact analysis

### Services (`/geepers-validate services`)
- Health endpoint checks
- Port availability
- Service responsiveness
- Quick canary tests

## Execute

**Validation type**: $ARGUMENTS

If no arguments:
- Ask what to validate or suggest based on project type

If "all":
- Run all applicable validators in parallel

If specific type:
- Route to appropriate specialist agent
