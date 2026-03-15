---
description: Cross-project impact analysis - what breaks if you change X in shared code
---

# Foresight

Before changing shared code, understand the blast radius. Maps dependencies across 55+ services and multiple projects.

## When to Use

- Changing anything in `~/shared/` (llm_providers, orchestration, data_fetching, utils)
- Modifying `service_manager.py`
- Updating a package that multiple services depend on
- Renaming or moving files that might be imported elsewhere
- Changing API contracts (endpoints, response formats, function signatures)

## Execute

### 1. Identify the Change

What are you about to modify?
```
File/module: $ARGUMENTS
```

### 2. Trace Dependents (PARALLEL)

Launch these searches simultaneously:

**Import tracing:**
```bash
# Python imports
grep -r "from <module> import\|import <module>" ~/servers/ ~/html/ ~/projects/ ~/shared/ --include="*.py"

# JavaScript/TypeScript imports
grep -r "require.*<module>\|from.*<module>" ~/html/ ~/projects/ --include="*.js" --include="*.ts" --include="*.tsx"
```

**Service manager references:**
```bash
grep -r "<path_or_module>" ~/service_manager.py
```

**Configuration references:**
```bash
grep -r "<module_or_path>" ~/shared/ ~/servers/ ~/html/ --include="*.json" --include="*.toml" --include="*.yaml" --include="*.cfg"
```

**CLAUDE.md references:**
```bash
grep -r "<module_or_path>" ~/*/CLAUDE.md ~/html/*/CLAUDE.md ~/servers/*/CLAUDE.md ~/projects/*/CLAUDE.md
```

### 3. Build Impact Map

```markdown
## Impact Analysis: <change description>

### Direct Dependents (will break immediately)
| Project | File | Import/Reference | Risk |
|---------|------|-------------------|------|
| coca | app.py:12 | from shared.utils import X | HIGH |
| firehose | api.ts:34 | fetch('/api/shared/X') | HIGH |

### Indirect Dependents (may break)
| Project | Dependency Chain | Risk |
|---------|-----------------|------|
| lessonplanner | → shared.llm_providers → ProviderFactory | MEDIUM |

### Safe (no dependency)
| Project | Reason |
|---------|--------|
| hexsweeper | No shared imports |

### Services to Restart After Change
- coca (port 3034) - systemd
- lessonplanner (port 4108) - sm
- studio (port 5413) - sm
```

### 4. Risk Assessment

| Risk Level | Action |
|------------|--------|
| **LOW** (0-2 dependents, internal) | Proceed with caution |
| **MEDIUM** (3-5 dependents) | Test each dependent after change |
| **HIGH** (6+ dependents or public API) | Create migration plan first |
| **CRITICAL** (shared base class or config) | Checkpoint, change, test ALL |

### 5. Migration Plan (if HIGH/CRITICAL)

1. **Checkpoint**: `git add -A && git commit -m "checkpoint: before <change>"`
2. **Backward compat**: Add alias/shim for old interface
3. **Change**: Make the modification
4. **Test**: Verify each dependent (`sm restart <service>` + health check)
5. **Clean up**: Remove compat shim once all dependents updated
6. **Document**: Update CLAUDE.md files for affected projects

## Common High-Impact Paths

| Path | Dependents | Notes |
|------|------------|-------|
| `~/shared/llm_providers/` | 10+ services | Core LLM interface |
| `~/shared/orchestration/` | 5+ services | DreamCascade/Swarm |
| `~/shared/data_fetching/` | 8+ projects | API clients |
| `~/shared/utils/` | 15+ projects | Widely imported |
| `~/shared/web/sse_helpers.py` | 6+ services | SSE streaming |
| `~/service_manager.py` | ALL services | Service lifecycle |
| `/etc/caddy/Caddyfile` | ALL web routes | Routing |
| `~/shared/config.py` | 10+ services | ConfigManager |

## Supporting Agents

- **@geepers_searcher** - Find all references across codebase
- **@geepers_validator** - Verify config after changes
- **@geepers_canary** - Quick health check after changes
- **@geepers_diag** - Investigate if something breaks

## Cross-References

- After changes: run `/session cp` to save state
- Before deploy: run `/ship` for full safety checks
- If things break: run `/thinktwice` to reconsider approach

## Target

**What you're changing**: $ARGUMENTS

If no arguments, ask what's about to be modified and trace its impact.
