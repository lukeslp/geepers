# Task Queue: Post-Session Audit & Remaining Work

**Generated**: 2026-03-07 14:00
**Total Tasks**: 18
**Quick Wins**: 8
**Blocked**: 0
**Critical/Security**: 3

---

## Ready to Build (Priority Order)

### 1. [QW] Add llamoria to games index
- **Source**: Session notes + manual inspection
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9.0
- **Description**: Games index at `/html/games/index.html` has 15 listed games but is missing the newly deployed llamoria (Moria roguelike) at `/games/llamoria/`. Add card in "Classic" section between Star Trek and Nonograms.
- **Files**: `/home/coolhand/html/games/index.html` (line 308-312 region)
- **Status**: Ready now
- **Tags**: frontend, games, content-update

### 2. [QW] Scrub hardcoded xAI API key from locAItor
- **Source**: Session notes + code inspection
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9.0
- **Description**: `/home/coolhand/projects/_archive/llm-history/locAItor/app.py` line 36-37 contains hardcoded xAI API key `REDACTED`. Must be removed/rotated before any public use. Replace with `os.getenv('XAI_API_KEY')` fallback pattern.
- **Files**: `/home/coolhand/projects/_archive/llm-history/locAItor/app.py` (lines 36-39)
- **Depends on**: None
- **Status**: Ready now
- **Tags**: security, api-key, cleanup
- **Note**: Project is in _archive but patterns extracted to ~/SNIPPETS/. Confirm key is rotated on xAI side.

### 3. [QW] Humanize 4 lukeslp public repos (README pass)
- **Source**: Session notes (dreamwalker, con-text, jeepers-legacy, eyegaze)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Apply `/humanize` skill to all 4 lukeslp repos to remove "AI-powered", "LLM-enhanced" etc terminology. Replace with "language model", specific model names. Verify no agent/skill references in public docs.
- **Repos**: lukeslp/dreamwalker, lukeslp/con-text, lukeslp/jeepers-legacy, lukeslp/eyegaze
- **Depends on**: None
- **Status**: Ready now
- **Tags**: content, documentation, humanize
- **Estimate breakdown**: 30min per repo reading current docs + running humanize skill + review/commit = 2h total

### 4. [QW] Add MIT LICENSE files to 4 lukeslp public repos
- **Source**: Session notes (incomplete)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 8.0
- **Description**: Create MIT LICENSE file in each lukeslp repo root (dreamwalker, con-text, jeepers-legacy, eyegaze) if missing. Use standard MIT template with "Luke Steuber" copyright, 2023-2026 years.
- **Files**: `{repo}/LICENSE` (each)
- **Depends on**: None
- **Status**: Ready now
- **Tags**: legal, compliance, documentation
- **Note**: Cross-check which repos actually lack LICENSE (may already have some)

### 5. [QW] Create task queue from projects-wide recommendations
- **Source**: `/home/coolhand/geepers/recommendations/by-project/projects-wide.md` (HIGH priority section)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Extract and prioritize high-priority items from projects-wide recommendations:
  - Create missing .gitignore files (linguistic-api, clinical)
  - Create missing README.md files (apis/, renamers/, clinical/)
  - Create missing CLAUDE.md files (linguistic-api/)
  - Audit 17 committed .env files for secrets exposure
- **Files**: Multiple (see projects-wide.md lines 9-90)
- **Depends on**: Reading projects-wide.md in full
- **Status**: Ready after reading reference doc
- **Tags**: documentation, security, infrastructure

### 6. [QW] Verify llamoria Caddy routing + add to service_manager.py
- **Source**: Session deployment notes
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Confirm llamoria is properly routed via Caddy at `/games/llamoria/`. Verify in `/etc/caddy/Caddyfile`. If missing, add static file handler. Consider adding to service_manager.py health endpoints (currently no health check for static games).
- **Files**:
  - `/etc/caddy/Caddyfile` (routing check)
  - `/home/coolhand/service_manager.py` (optional: add game services entry)
  - `/home/coolhand/html/games/llamoria/index.html` (verify load)
- **Depends on**: None
- **Status**: Ready now
- **Tags**: infrastructure, deployment, games

### 7. [QW] Quality audit on new timeline pages (a11y, perf)
- **Source**: Session notes + geepers ecosystem
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.5
- **Description**: Run `/quality-audit` skill (or @geepers_a11y + @geepers_perf in parallel) on:
  - dr.eamer.dev/datavis/evolution/ (LLM timeline)
  - diachronica.com/evolution/ (etymology timeline)
  Check WCAG 2.1 AA compliance, Lighthouse scores (target 90+ perf), font sizing, color contrast, keyboard navigation.
- **Status**: Ready now (skill-delegated)
- **Tags**: quality, accessibility, performance, timeline
- **Estimate**: 30min per page with agent assistance = 1h

### 8. [QW] Publish lukeslp repos from private to public
- **Source**: Session notes (4 repos moved but not yet public)
- **Impact**: 4 | **Effort**: 2 | **Priority**: 5.5
- **Description**: Change GitHub visibility for 4 lukeslp repos from private to public:
  - dreamwalker
  - con-text
  - jeepers-legacy
  - eyegaze
  **Prerequisites**: Must complete items #3 (humanize) and #4 (add LICENSE) first.
- **Status**: Blocked until #3, #4 complete
- **Tags**: github, publishing, release
- **Note**: May require updating documentation/portfolio links after making public

---

## Medium Priority (4.5-5.5)

### 9. Security audit on projects/ — .env exposure
- **Source**: projects-wide.md high-priority security section
- **Impact**: 5 | **Effort**: 3 | **Priority**: 5.0
- **Description**: Audit all 17 committed .env files for exposed secrets (API keys, database passwords, tokens). Create .env.example templates for each. Remove files from git history using git filter-repo with --blob-callback for sensitive patterns. Regenerate/rotate any exposed credentials on third-party services.
- **Files**: 17 .env files (see projects-wide.md lines 13-33)
- **Depends on**: Manual secret inventory
- **Status**: Ready now (security agent recommended)
- **Tags**: security, critical, git-history
- **Estimate**: 4h (inventory 1h + filter-repo 2h + rotation coordination 1h)

### 10. Fix httpx version conflicts project-wide
- **Source**: projects-wide.md + known constraint
- **Impact**: 4 | **Effort**: 2 | **Priority**: 4.5
- **Description**: Run systematic `pip install 'httpx<0.28.0'` across all projects using atproto (Bluesky). Verify no regression. Update all requirements.txt files. Reference: `/home/coolhand/projects/HTTPX_VERSION_CONSTRAINT.md` for full context.
- **Files**: requirements.txt in beltalowda, linguistic-api, raccoon_mode, storyblocks, wordblocks
- **Depends on**: None
- **Status**: Ready now
- **Tags**: dependencies, python, infrastructure
- **Estimate**: 1.5h

### 11. Install missing system/Python dependencies
- **Source**: projects-wide.md lines 48-52
- **Impact**: 3 | **Effort**: 1 | **Priority**: 4.0
- **Description**: Install missing dependencies blocking Python projects:
  - typeguard (required by inflect 7.5.0)
  - pycairo (required by pygobject 3.42.1)
  Run: `pip install typeguard pycairo` globally or in affected venvs.
- **Status**: Ready now
- **Tags**: dependencies, python, system

### 12. Create missing documentation (README, CLAUDE.md)
- **Source**: projects-wide.md lines 79-89
- **Impact**: 2 | **Effort**: 2 | **Priority**: 4.0
- **Description**: Create missing documentation:
  - `/home/coolhand/projects/apis/README.md` (227MB project)
  - `/home/coolhand/projects/renamers/README.md`
  - `/home/coolhand/projects/clinical/README.md` (clarify relationship to /servers/clinical/)
  - `/home/coolhand/projects/linguistic-api/CLAUDE.md` (PRODUCTION SERVICE)
  Use @geepers_readme + @geepers_docs agents in parallel.
- **Status**: Ready now (agent-recommended)
- **Tags**: documentation, infrastructure
- **Estimate**: 3h with agents

### 13. Organize packages/ directory (archive/incomplete review)
- **Source**: projects-wide.md lines 98-103
- **Impact**: 2 | **Effort**: 2 | **Priority**: 3.5
- **Description**: Review and restructure `/home/coolhand/projects/packages/`:
  - Move archived/ to _archive/ (standardization)
  - Audit incomplete/ for removal candidates
  - Consolidate working/ projects with active status
  - Update .gitignore for cleanup
- **Status**: Ready after scope clarification
- **Tags**: organization, cleanup, infrastructure

---

## Lower Priority (3.0-3.5)

### 14. Cleanup broken symlinks project-wide
- **Source**: projects-wide.md lines 72-75
- **Impact**: 1 | **Effort**: 1 | **Priority**: 2.5
- **Description**: Find and verify 17 broken symlinks. Delete only after confirming they're safe. Mostly in archived areas.
- **Status**: Ready now
- **Tags**: cleanup, git-safety

### 15. Review and prune apis/SUGGESTIONS.md
- **Source**: projects-wide.md lines 92-97
- **Impact**: 1 | **Effort**: 2 | **Priority**: 2.5
- **Description**: 75KB SUGGESTIONS.md file. Implement high-value items, archive stale suggestions, remove duplicates.
- **Status**: Ready (manual review)
- **Tags**: documentation, cleanup

### 16. Clean up inbox/ and storage/ directories
- **Source**: projects-wide.md lines 104-110
- **Impact**: 1 | **Effort**: 2 | **Priority**: 2.0
- **Description**: inbox/ (5.8MB), storage/ (4.9MB). Move active projects to proper directories, archive or delete stale content.
- **Status**: Ready after scope review
- **Tags**: cleanup, organization

### 17. Locator patterns extraction & documentation
- **Source**: Session notes (locAItor in _archive/)
- **Impact**: 2 | **Effort**: 2 | **Priority**: 2.0
- **Description**: locAItor (Flask image forensics + grok-vision) has useful patterns for image metadata extraction and socioeconomic inference. Extract reusable patterns to ~/SNIPPETS/by-category/image-analysis-patterns.md after API key scrub. Document for future projects.
- **Status**: Blocked until #2 (API key scrub) complete
- **Tags**: snippets, documentation, archival

### 18. Run test coverage analysis project-wide
- **Source**: projects-wide.md lines 117-122
- **Impact**: 1 | **Effort**: 3 | **Priority**: 1.5
- **Description**: Run `pytest --cov` across all 243 test files. Target 80%+ coverage for critical paths. Generate report. Low priority (informational).
- **Status**: Ready anytime
- **Tags**: testing, quality, reporting

---

## Statistics

| Category | Count |
|----------|-------|
| **Ready to build** | 8 |
| **Medium priority** | 6 |
| **Lower priority** | 4 |
| **Quick wins (QW)** | 8 |
| **Blocked** | 0 |
| **Security critical** | 3 (#2, #9 key management) |
| **Agent-delegated** | 5 |

---

## Execution Path (Recommended Sequence)

**Phase 1 - Fast Wins (30min)**
1. Add llamoria to games index (#1)
2. Scrub xAI key from locAItor (#2)
3. Verify Caddy routing for llamoria (#6)

**Phase 2 - Documentation & Compliance (2-3h)**
4. Humanize 4 lukeslp repos (#3) — use `/humanize` skill
5. Add MIT LICENSE files (#4)
6. Create missing README/CLAUDE.md (#12) — delegate to agents

**Phase 3 - Quality & Verification (1.5h)**
7. Run quality audit on timelines (#7) — use `/quality-audit` skill
8. Verify games index visually (regression test)

**Phase 4 - Publishing (1h)**
9. Publish 4 lukeslp repos to public (#8) — after #3, #4 complete

**Phase 5 - Security & Infrastructure (4-6h, can run in background)**
10. Security audit on .env files (#9) — @geepers_security
11. Fix httpx conflicts (#10)
12. Organize packages/ directory (#13)

---

## Notes

- **No blocking dependencies** between quick wins — can execute items 1-8 in any order
- **Items #9, #10 are large** but can run in background via agents
- **Games index deployment** is successful; just needs manual index update
- **Timeline pages** deployed and live; quality audit is verification step
- **lukeslp repos** are ready for public release once humanized and licensed
- **See also**: `/home/coolhand/geepers/recommendations/by-project/projects-wide.md` for full context on items 5, 9-16

---

## Geepers Integration

**Agents recommended for delegation**:
- `@geepers_security` — items #2, #9 (key management, audit)
- `@geepers_readme` + `@geepers_docs` — item #12 (documentation)
- `@geepers_a11y` + `@geepers_perf` — item #7 (quality audit)
- `/quality-audit` skill — item #7 (full spectrum audit)
- `/humanize` skill — item #3 (content cleanup)

**Skills for complex workflows**:
- `/session-start` — begin next session with this queue
- `/quality-audit` — parallel a11y, perf, security, deps checks
