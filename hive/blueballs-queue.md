# Task Queue: blueballs (Release Prep)

**Generated**: 2026-03-07
**Project**: Bluesky Network Visualizer
**Goal**: Release as polished joke/fun project on GitHub
**Total Tasks**: 24
**Quick Wins**: 7
**Blocked**: 0

---

## Release Readiness Summary

| Category | Count | Status |
|----------|-------|--------|
| High priority (score >6.5) | 9 | Ready |
| Quick wins (impact ≥3, effort ≤2) | 7 | Ready |
| Content humanization | 5 | Critical path |
| Low-hanging fruit fixes | 4 | Ready |
| Documentation Polish | 3 | Ready |
| Dependency/CI cleanup | 3 | Ready |
| Total Effort | ~17 hours | 2-3 days solo |

---

## Ready to Build (Priority Order)

### 1. [QW] Humanize README.md
- **Source**: README.md (lines 1-166)
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9
- **Description**: Strip formal/technical jargon, add personality. Replace "An interactive tool for exploring" with conversational tone. Update tags from "visualization modes" to casual language. Make it fun—this is a joke project.
- **Files**: `/home/coolhand/projects/blueballs/README.md`
- **Details**:
  - Intro: Make it funny/casual (e.g., "See your Bluesky network in 20 different ways—because one way isn't enough")
  - Section headers: More personality
  - Remove robotic phrasing ("all views read the same JSON")
  - Performance table: Frame as "what your computer can handle"
  - Tech stack: Less corporate, more fun

### 2. [QW] Humanize START_HERE.md
- **Source**: START_HERE.md (lines 1-54)
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9
- **Description**: Friendly, encouraging tone. Make setup feel fun. Replace "What it asks:" with conversational steps. Add humor to the network colors section.
- **Files**: `/home/coolhand/projects/blueballs/START_HERE.md`
- **Estimate**: 15-20 minutes

### 3. [QW] Humanize CLAUDE.md (remove from release)
- **Source**: CLAUDE.md (all)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 8
- **Description**: This is an internal instruction file. Either delete it or move to private docs. Not for public GitHub release.
- **Files**: `/home/coolhand/projects/blueballs/CLAUDE.md`
- **Decision point**: Delete from public repo OR keep as project-internal reference?

### 4. [QW] Humanize CHANGELOG.md
- **Source**: CHANGELOG.md (lines 1-160)
- **Impact**: 4 | **Effort**: 2 | **Priority**: 8
- **Description**: Technical changelog is good but needs personality. Add emojis (✨ features, 🐛 fixes, 📚 docs). Change "Added - 2025-11-13" to "Unreleased" section. Make release notes sound less formal.
- **Files**: `/home/coolhand/projects/blueballs/CHANGELOG.md`
- **Estimate**: 25-30 minutes

### 5. [QW] Create/Polish LICENSE (if not present)
- **Source**: None currently
- **Impact**: 4 | **Effort**: 1 | **Priority**: 8
- **Description**: Add LICENSE file. README mentions MIT, so create `LICENSE` file with standard MIT license header.
- **Files**: `/home/coolhand/projects/blueballs/LICENSE`
- **Details**: Standard MIT with Luke Steuber copyright

### 6. [QW] Clean up root directory cruft
- **Source**: Root-level files
- **Impact**: 3 | **Effort**: 1 | **Priority**: 7
- **Description**: Review and consolidate legacy directories. Move/delete:
  - `archive/` (old experiments - archive/compress or delete)
  - `blueballs-migrating/` (different app - move to separate section or delete)
  - `bluesky_dashboard/` and `bluesky-network-viz/` (legacy duplicates?)
  - Old `index_*.html` visualizers (20+ files - keep only the best ones for demo, move rest to archive)
- **Files**: Root directory cleanup
- **Impact**: Makes repo cleaner for public release

### 7. [QW] Fix .gitignore for release
- **Source**: `.gitignore` (review)
- **Impact**: 3 | **Effort**: 1 | **Priority**: 7
- **Description**: Ensure proper ignores: `.venv/`, `node_modules/`, `.env`, logs, cache dirs. Add patterns for build artifacts.
- **Files**: `/home/coolhand/projects/blueballs/.gitignore`
- **Estimate**: 10 minutes

---

## Critical Path: Content Humanization

### 8. Humanize backend code comments & docstrings
- **Source**: `backend/app/**/*.py` (services, routes, analytics)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.5
- **Description**: Review docstrings and code comments for robotic language. Replace technical jargon with clearer explanations. Focus on public-facing modules: `bluesky_client.py`, `network_fetcher.py`, main endpoints.
- **Files**:
  - `/home/coolhand/projects/blueballs/backend/app/services/bluesky_client.py`
  - `/home/coolhand/projects/blueballs/backend/app/routes/network.py`
  - `/home/coolhand/projects/blueballs/backend/app/analytics/graph_analysis.py`
- **Estimate**: 1-1.5 hours

### 9. Humanize frontend code comments & component docs
- **Source**: `frontend/src/lib/**/*.{ts,svelte}` (components, stores)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 6.5
- **Description**: Component documentation, store descriptions. Make it friendlier for developers reading the code.
- **Files**:
  - `/home/coolhand/projects/blueballs/frontend/src/lib/components/`
  - `/home/coolhand/projects/blueballs/frontend/src/lib/stores/`
- **Estimate**: 1-1.5 hours

### 10. Run @geepers-readme for polished README
- **Source**: README.md (current) + project structure
- **Impact**: 5 | **Effort**: 1 | **Priority**: 8.5
- **Description**: Use geepers-readme agent to generate professional, engaging README. Use the humanized content as input to ensure personality is preserved. This will produce a polished version with:
  - Compelling hero section
  - Clear feature list
  - Installation steps formatted beautifully
  - Architecture summary
  - Contribution guidelines
  - Links and badges
- **Files**: Output → `/home/coolhand/projects/blueballs/README.md` (replace current)
- **Depends on**: Task #1 humanization complete

### 11. Update package metadata for npm/PyPI (if releasing packages)
- **Source**: `frontend/package.json`, `backend/setup.py` (if exists)
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6
- **Description**: If this will be published to npm or PyPI:
  - Add proper description (no "AI-powered", use "Bluesky network visualization")
  - Add tags/keywords
  - Add repository URL
  - Add author info (Luke Steuber)
  - Add license field
- **Files**:
  - `/home/coolhand/projects/blueballs/frontend/package.json`
  - Backend setup.py (if packaging the backend)

---

## Low-Hanging Fruit Fixes

### 12. [QW] Add missing LICENSE file
- **Source**: README mentions MIT
- **Impact**: 4 | **Effort**: 1 | **Priority**: 8
- **Description**: Create standard MIT license file.
- **Files**: `/home/coolhand/projects/blueballs/LICENSE`

### 13. Add .editorconfig for consistency
- **Source**: None present
- **Impact**: 2 | **Effort**: 1 | **Priority**: 5.5
- **Description**: Standard `.editorconfig` for Python and JS/TS code. Ensures formatting consistency across contributors.
- **Files**: `/home/coolhand/projects/blueballs/.editorconfig`

### 14. Review and update INSTALL.md
- **Source**: `INSTALL.md`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.5
- **Description**: Cross-check with README quick start. Ensure instructions are current and match latest FastAPI/SvelteKit setup.
- **Files**: `/home/coolhand/projects/blueballs/INSTALL.md`

### 15. Add CONTRIBUTING.md (optional but nice for joke project)
- **Source**: None present
- **Impact**: 2 | **Effort**: 2 | **Priority**: 5
- **Description**: Light-hearted contribution guide. "We accept PRs for new visualizations, bug fixes, and terrible network jokes."
- **Files**: `/home/coolhand/projects/blueballs/CONTRIBUTING.md`

---

## Documentation Polish

### 16. Audit docs/ directory for completeness
- **Source**: `docs/` directory
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.5
- **Description**: Review existing docs. Are they all necessary for release? Update dates, ensure links work.
- **Files**: `/home/coolhand/projects/blueballs/docs/`
- **Details**: Check for stale/outdated docs from old firehose project

### 17. Add FAQ section to README or docs/FAQ.md
- **Source**: Common user questions (inferred from docs)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 5.5
- **Description**: Address:
  - "How large a network can I visualize?"
  - "Does it work on mobile?"
  - "Can I use this offline?"
  - "What about privacy?"
- **Files**: `/home/coolhand/projects/blueballs/docs/FAQ.md` (new)

### 18. Create DEPLOYMENT.md (production guide)
- **Source**: CLAUDE.md deployment section, existing setup
- **Impact**: 2 | **Effort**: 2 | **Priority**: 5
- **Description**: How to deploy on a VPS/server. Docker guide. Environment setup. This is post-release documentation.
- **Files**: `/home/coolhand/projects/blueballs/DEPLOYMENT.md` (new)

---

## Dependency & CI/CD Cleanup

### 19. Audit and pin dependencies (critical for release)
- **Source**: `backend/requirements.txt`, `frontend/package.json`
- **Impact**: 5 | **Effort**: 2 | **Priority**: 8.5
- **Description**: Currently requirements use `>=` ranges. For a released project:
  - Audit all versions for security/compatibility
  - Update to latest stable versions
  - Pin exact versions or use specific ranges (e.g., `^3.8.0` for Node packages)
  - Run `npm audit` and `pip-audit` for security issues
  - Create lock files (`package-lock.json`, `requirements.lock`)
- **Files**:
  - `/home/coolhand/projects/blueballs/backend/requirements.txt`
  - `/home/coolhand/projects/blueballs/frontend/package.json`

### 20. Review and update GitHub Actions CI
- **Source**: `.github/workflows/ci.yml`
- **Impact**: 3 | **Effort**: 1 | **Priority**: 6.5
- **Description**: Ensure CI runs on push and PR. Check:
  - Backend: pytest with proper NetworkX flag (`NETWORKX_DISABLE_BACKENDS_DISCOVERY=1`)
  - Frontend: TypeScript lint, build check
  - Python version pins (use 3.11+)
  - Node version pins (use 20+)
- **Files**: `/home/coolhand/projects/blueballs/.github/workflows/ci.yml`

### 21. Add SECURITY.md (vulnerability reporting)
- **Source**: None
- **Impact**: 2 | **Effort**: 1 | **Priority**: 5
- **Description**: Standard template for reporting security issues. Points to responsible disclosure process.
- **Files**: `/home/coolhand/projects/blueballs/SECURITY.md` (new)

---

## Git & Release Preparation

### 22. Clean commit history (git rebase if needed)
- **Source**: Current git log
- **Impact**: 2 | **Effort**: 2 | **Priority**: 5
- **Description**: Check if commit history is clean. If many "WIP" or "tmp" commits, consider squashing before release. Aim for narrative commits with good messages.
- **Files**: Git repository

### 23. Create release branch and tag
- **Source**: Current master
- **Impact**: 3 | **Effort**: 1 | **Priority**: 7.5
- **Description**: Once all prep is done:
  - Ensure working directory is clean
  - Tag with version (e.g., `v1.0.0`)
  - Push to GitHub
- **Files**: Git tags

### 24. Final pre-release checklist
- **Source**: All previous tasks
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9
- **Description**: Before shipping:
  - [ ] All tasks 1-21 complete
  - [ ] Local build & test pass
  - [ ] CI passes on GitHub
  - [ ] README reads naturally
  - [ ] LICENSE present
  - [ ] No secrets in `.gitignore`
  - [ ] VERSION bumped (if using semantic versioning)
  - [ ] CHANGELOG updated with release date
  - [ ] No @geepers_* agent names in docs
  - [ ] No internal tool references (geepers, agents, skills)
- **Files**: Release documentation

---

## Summary: Work Phases

### Phase 1: Humanization (3-4 hours)
- Tasks 1, 2, 4, 8, 9
- Output: Natural, fun-sounding docs and comments
- Blocker: Must complete before @geepers-readme (task 10)

### Phase 2: Content Polish & Documentation (2-3 hours)
- Tasks 3, 5, 10, 12, 14, 16, 17
- Output: Professional README, complete docs, no jargon
- Depends on: Phase 1

### Phase 3: Technical Cleanup (2-3 hours)
- Tasks 6, 7, 13, 19, 20, 21
- Output: Release-ready code, security policy, locked dependencies
- Parallel possible

### Phase 4: Release (1 hour)
- Tasks 22, 23, 24
- Output: Tagged release, pushed to GitHub

**Total**: ~17 hours (2-3 days solo, 1 day with parallel agents)

---

## Recommended Agent Workflow

```bash
# Phase 1: Humanization (run in parallel)
@geepers_humanizer --files README.md,START_HERE.md,CLAUDE.md,CHANGELOG.md,backend/app/services/,frontend/src/lib/

# Phase 2: Polish
@geepers_readme --project blueballs

# Phase 3: Cleanup
# Manual work - tasks 6, 7, 13, 19, 20, 21

# Phase 4: Release
# Manual git workflow
```

---

## Notes

- **Tone**: This is a fun, tongue-in-cheek project. Lean into humor in docs.
- **Blocker**: Task 10 (geepers-readme) depends on completing humanization (tasks 1-2).
- **Risk**: Dependency audit (task 19) may uncover incompatibilities requiring code changes.
- **Skip**: `blueballs-migrating/` contains old firehose sentiment app—decide whether to include or exclude from release.
- **Keep clean**: No agent/skill references in public docs per CLAUDE.md instructions.

---

Generated by @geepers_planner on 2026-03-07
