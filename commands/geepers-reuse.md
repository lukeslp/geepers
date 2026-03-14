---
description: Check for existing code, snippets, and endpoints to avoid duplication - pre-check before building, post-check for integration opportunities
---

# Reuse Check

Before building something new, check what already exists. After building, identify integration opportunities.

## Pre-Check (Before Building)

Search these locations for existing implementations:

### 1. Snippet Library
```
~/geepers/snippets/
```
Check for reusable patterns, utilities, and components.

### 2. Shared Library
```
~/shared/
├── llm_providers/     # 12 LLM provider integrations
├── orchestration/     # Multi-agent patterns (DreamCascade, DreamSwarm)
├── data_fetching/     # 17 API clients (arXiv, Census, GitHub, NASA, etc.)
├── utils/             # File, text, vision, embedding utilities
└── web/               # SSE helpers, web utilities
```

### 3. API Gateway
```
~/servers/api-gateway/
~/html/apis/
```
Check for existing endpoints that provide needed functionality.

### 4. Existing Services
```
sm status              # List all 17+ running services
```
Check if a service already does what you need.

### 5. Project-Specific
```
~/geepers/recommendations/by-project/   # Existing recommendations
~/projects/packages/                     # Reusable packages
```

## Search Strategy

Use @geepers_searcher or these patterns:
```bash
# Find similar functionality
grep -r "function_name\|ClassName\|pattern" ~/shared/ ~/servers/

# Check snippet library
ls ~/geepers/snippets/

# Find API endpoints
grep -r "@app.route\|router\.\|endpoint" ~/servers/ ~/html/
```

## Post-Check (After Building)

After completing work, evaluate:

### Integration Opportunities
1. **Extract to shared** - Is this useful across projects? → Move to `~/shared/`
2. **Create snippet** - Is this a reusable pattern? → Add to `~/geepers/snippets/`
3. **Expose as API** - Should other services access this? → Add to API gateway
4. **Document pattern** - Is this a best practice? → Add to project CLAUDE.md

### Consolidation Candidates
Look for:
- Duplicate implementations across projects
- Similar utilities that could be merged
- Services that could share a common base
- API endpoints with overlapping functionality

## Execute

**Mode**: $ARGUMENTS

If no arguments:
1. Ask what you're about to build
2. Run pre-check for existing solutions
3. Report findings before proceeding

If arguments provided:
- "pre" or "before" → Run pre-check only
- "post" or "after" → Run post-check for integration opportunities
- Description of feature → Search for existing implementations

## Agent Support

- **@geepers_searcher** - Find code patterns and files
- **@geepers_snippets** - Manage snippet library
- **@geepers_integrator** - Merge and consolidate code
- **@geepers_api** - Review API design and endpoints
