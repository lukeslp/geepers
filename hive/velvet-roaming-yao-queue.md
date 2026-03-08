# Task Queue: GitHub Org Audit & LLM History Showcase

**Generated**: 2026-03-07 17:34
**Total Tasks**: 24
**Quick Wins**: 5
**Blocked**: 3

---

## CRITICAL PATH → Timeline Page Live

```
Timeline Page Deployment:
  1. Research & validate game/repo overlap (no blockers) ──┐
  2. Build timeline page content structure                 │
  3. Build evolution/ static page + D3.js                  ├── Deploy to diachronica.com
  4. Update Caddy routing for /evolution/                  │
  5. Verify page loads + links work ──────────────────────┘
```

**Timeline to "page live"**: 4-5 tasks, ~6-8 hours, can start immediately.

---

## Ready to Build (Priority Order)

### 1. [QW] Cross-Reference Games Content
- **Source**: Plan Step 3a, Wave 1
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Search ~/html/games/ directory to inventory existing games, then compare against ShadowLlama/web/games/llamoria to identify new/unique content. No repo clones needed yet.
- **Files**: ~/html/games/, research only
- **Depends on**: None
- **Assignee**: `@geepers_searcher` (file/directory cross-reference)
- **Time**: ~1 hour
- **Output**: Comparison doc: "Games Already Exist: [list], Games to Evaluate: [list]"

### 2. [QW] Cross-Reference eyegaze Interactives
- **Source**: Plan Step 3b, Wave 1
- **Impact**: 3 | **Effort**: 1 | **Priority**: 5.0
- **Description**: Inventory existing ~/html/eyegaze/ content. Quick check against known eyegaze repo (catfall, starfall, colors, TTS) to spot what's missing.
- **Files**: ~/html/eyegaze/ (local inventory only)
- **Depends on**: None
- **Assignee**: `@geepers_searcher`
- **Time**: ~30 min
- **Output**: "Missing Interactives: [list]" or "Already Complete"

### 3. [QW] Inventory Existing Games Before Evaluation
- **Source**: Plan Step 3a
- **Impact**: 4 | **Effort**: 1 | **Priority**: 5.5
- **Description**: Run `find ~/html/games -type f -name "*.html" -o -name "*.py" | head -20` to list existing game files. Creates baseline for deduplication.
- **Files**: ~/html/games/
- **Depends on**: Task #1 complete (cross-reference), Task #2 complete (eyegaze)
- **Assignee**: Manual bash search
- **Time**: ~15 min
- **Output**: Inventory list for evaluation phase

### 4. [QW] Validate No Leaked API Keys in Public Repos
- **Source**: Plan Step 2, Wave 3
- **Impact**: 5 | **Effort**: 1 | **Priority**: 7.0
- **Description**: Pre-screening before any GitHub cloning: grep for `OPENAI_KEY`, `ANTHROPIC_API`, `VECTARA`, `PINECONE` in 5 candidate repos (Dreamwalker-Master, con_text, jeepers, cursor-rules, llamaherder). Can do via GitHub API, no clone needed.
- **Files**: None (API scan only)
- **Depends on**: None
- **Assignee**: `@geepers_security` or manual `gh api` search
- **Time**: ~45 min
- **Output**: "Safe to Public: [repos]" OR "Remove keys from: [repos]"

### 5. Build LLM Evolution Timeline Page (HTML + Structure)
- **Source**: Plan Step 1, Wave 2
- **Impact**: 5 | **Effort**: 3 | **Priority**: 7.0
- **Description**: Create ~/servers/diachronica/static/evolution/index.html with Swiss Design aesthetic. 8 time periods, each with project name + description + tech + link. Use vanilla JS timeline (no D3.js required for MVP). Dark theme matching diachronica.
- **Files**:
  - `~/servers/diachronica/static/evolution/index.html` (new)
  - `~/servers/diachronica/static/evolution/styles.css` (new)
- **Depends on**: Task #4 (security scan)
- **Assignee**: `@geepers_orchestrator_frontend` OR `@geepers_design`
- **Time**: ~3 hours (MVP: vanilla timeline, no interactivity)
- **Output**: Static HTML page, ready for Caddy routing
- **Notes**:
  - Content can reference private repos (screenshots, archived clones)
  - Links to public repos only point to repos that will be made public
  - Can launch with partial content, add more repos as they're evaluated

### 6. Add /evolution/ Route to Caddy (diachronica.com block)
- **Source**: Plan Step 1, Wave 3
- **Impact**: 5 | **Effort**: 1 | **Priority**: 7.0
- **Description**: Add `handle_path /evolution/* { root * /home/coolhand/servers/diachronica/static/evolution; file_server }` to Caddy config's diachronica.com block. Reload caddy.
- **Files**: `/etc/caddy/Caddyfile`
- **Depends on**: Task #5 (page created)
- **Assignee**: `@geepers_caddy` (SOLE authority on Caddy)
- **Time**: ~15 min (validation + reload)
- **Output**: Route live, page accessible at https://diachronica.com/evolution/
- **Verification**: `curl https://diachronica.com/evolution/ | head -5` returns HTML

### 7. [BLOCKED] Humanize READMEs for 5 Public Repos
- **Source**: Plan Step 2, Wave 2
- **Impact**: 4 | **Effort**: 2 | **Priority**: 5.5
- **Description**: Strip AI/robot language from READMEs, ensure Luke Steuber credit. Repos: Dreamwalker-Master, con_text, jeepers, cursor-rules, llamaherder.
- **Files**: `READMES.md` in each repo (cloned to ~/projects/_archive/ first)
- **Depends on**: Task #8 (repos cloned)
- **Assignee**: `/humanize` skill + `@geepers_readme`
- **Time**: ~2 hours (5 repos × ~25 min each)
- **Output**: Humanized READMEs committed back to repos
- **Blockers**: Repos must be cloned first

### 8. [BLOCKED] Clone 5 Candidate Public Repos (Shallow)
- **Source**: Plan Step 2 + 6, Wave 2
- **Impact**: 4 | **Effort**: 2 | **Priority**: 6.0
- **Description**: Shallow clones of: Dreamwalker-Master, con_text, jeepers, cursor-rules, llamaherder into ~/projects/_archive/. Then audit READMEs, check for .env files, remove sensitive content.
- **Files**:
  - `~/projects/_archive/Dreamwalker-Master/`
  - `~/projects/_archive/con_text/`
  - `~/projects/_archive/jeepers/`
  - `~/projects/_archive/cursor-rules/`
  - `~/projects/_archive/llamaherder/`
- **Depends on**: Task #4 (security scan passed)
- **Assignee**: Bash (gh repo clone)
- **Time**: ~45 min (clones + basic cleanup)
- **Output**: 5 repos cloned, .env files removed, READMEs audited

### 9. [BLOCKED] Add MIT LICENSEs Where Missing
- **Source**: Plan Step 2, Wave 2
- **Impact**: 3 | **Effort**: 1 | **Priority**: 4.5
- **Description**: Check each of 5 repos for LICENSE file. If missing, add MIT LICENSE with Luke Steuber copyright year.
- **Files**: `LICENSE` in each repo
- **Depends on**: Task #8 (repos cloned)
- **Assignee**: Manual or `@geepers_readme`
- **Time**: ~30 min
- **Output**: All repos have MIT LICENSE

### 10. [BLOCKED] Make 5 Repos Public on GitHub
- **Source**: Plan Step 2, Wave 4
- **Impact**: 5 | **Effort**: 1 | **Priority**: 7.0
- **Description**: `gh repo edit one-impossible-thing/Dreamwalker-Master --visibility public` for each of 5 repos.
- **Files**: None (GitHub API)
- **Depends on**: Task #7 (READMEs humanized), Task #9 (LICENSEs added)
- **Assignee**: Bash (gh command)
- **Time**: ~10 min (5 × 2 min)
- **Output**: 5 repos now public
- **Verification**: `gh repo view one-impossible-thing/Dreamwalker-Master --json visibility`

### 11. Clone ShadowLlama for Game Evaluation
- **Source**: Plan Step 3a, Wave 2
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.0
- **Description**: `gh repo clone one-impossible-thing/ShadowLlama ~/projects/_archive/ShadowLlama --depth 1`. Evaluate mental-roguelike, cyberllama against existing games. Extract playable games if novel.
- **Files**: ~/projects/_archive/ShadowLlama/
- **Depends on**: Task #1 (games cross-ref complete)
- **Assignee**: Bash (clone) + game evaluation (human review)
- **Time**: ~2 hours (clone + evaluation)
- **Output**: "Deploy: [games]" OR "Archive: all variants of existing games"

### 12. Clone llamoria for Game Comparison
- **Source**: Plan Step 3a, Wave 2
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
- **Description**: `gh repo clone one-impossible-thing/llamoria ~/projects/_archive/llamoria --depth 1`. Compare against ~/html/games/moria. If different, evaluate for deployment.
- **Files**: ~/projects/_archive/llamoria/
- **Depends on**: Task #1 (games cross-ref), Task #11 (ShadowLlama evaluated)
- **Assignee**: Bash + human review
- **Time**: ~1 hour
- **Output**: Comparison report + deployment decision

### 13. Clone eyegaze Interactives
- **Source**: Plan Step 3b, Wave 2
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.5
- **Description**: `gh repo clone actually-useful-ai/eyegaze ~/projects/_archive/eyegaze --depth 1`. Compare interactives/ against ~/html/eyegaze/. Pull missing ones.
- **Files**: ~/projects/_archive/eyegaze/
- **Depends on**: Task #2 (eyegaze cross-ref)
- **Assignee**: Bash + human review
- **Time**: ~1 hour
- **Output**: "Missing interactives: [list]" → pull into ~/html/eyegaze/

### 14. Clone and Evaluate locAItor
- **Source**: Plan Step 4, Wave 2
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.0
- **Description**: `gh repo clone actually-useful-ai/locAItor ~/projects/_archive/locAItor-eval --depth 1`. Review code, dependencies, API key requirements. Test on free port. Decision: deploy OR extract patterns to SNIPPETS.
- **Files**: ~/projects/_archive/locAItor-eval/
- **Depends on**: Task #4 (security scan)
- **Assignee**: Code review + test deployment
- **Time**: ~2 hours
- **Output**: Deployment decision + README update OR snippet extraction

### 15. Clone bluesky_cleaner and Cross-Reference
- **Source**: Plan Step 5, Wave 1/2
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
- **Description**: Shallow clone of bluesky_cleaner. Compare `follower_ranker.py` + `vibe_check_posts.py` against ~/projects/bluevibes/ functionality. Pull unique patterns.
- **Files**: ~/projects/_archive/bluesky_cleaner/
- **Depends on**: None
- **Assignee**: `@geepers_searcher` or manual review
- **Time**: ~1 hour
- **Output**: "Already in bluevibes" OR "Pull unique patterns: [list]"

### 16. Create ~/projects/_archive/llm-history/ (Canonical Archive)
- **Source**: Plan Step 6, Wave 2
- **Impact**: 3 | **Effort**: 1 | **Priority**: 5.0
- **Description**: Create directory and organize shallow clones of historical repos (con_text, Dreamwalker-Master, jeepers, slp-gpt). Add README explaining archive purpose (source for timeline, not deployed).
- **Files**:
  - `~/projects/_archive/llm-history/README.md` (new)
  - Symlinks/clones: con_text/, Dreamwalker-Master/, jeepers/, slp-gpt/
- **Depends on**: Task #8 (repos cloned)
- **Assignee**: Bash + documentation
- **Time**: ~30 min
- **Output**: Archive organized with metadata

### 17. [QW] Verify Bluevibes Has Equivalents
- **Source**: Plan Step 5
- **Impact**: 2 | **Effort**: 1 | **Priority**: 2.5
- **Description**: Quick grep in ~/projects/bluevibes/ for `follower`, `rank`, `vibe`, `post_analysis` to confirm bluesky_cleaner would be redundant.
- **Files**: ~/projects/bluevibes/
- **Depends on**: None
- **Assignee**: Manual grep
- **Time**: ~20 min
- **Output**: "Redundant" OR "Missing: [features]"

### 18. [QW] Verify herd-ai Sync with llamaherder
- **Source**: Plan Step 7, Wave 4
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
- **Description**: Compare ~/packages/working/herd/ against actually-useful-ai/llamaherder. Check version numbers, feature parity, last sync date.
- **Files**:
  - ~/packages/working/herd/
  - actually-useful-ai/llamaherder (cloned in Task #8)
- **Depends on**: Task #8 (llamaherder cloned)
- **Assignee**: Manual review or git diff
- **Time**: ~30 min
- **Output**: "In sync", "Update needed", OR "Archive historical"

### 19. Extract Unique Patterns to ~/SNIPPETS/
- **Source**: Plan Step 7, Wave 4
- **Impact**: 2 | **Effort**: 2 | **Priority**: 3.0
- **Description**: After all evaluations, extract interesting code patterns from cloned repos. Examples: prompt engineering from con_text, agent dispatch from jeepers, adversarial patterns from durandal.
- **Files**: ~/SNIPPETS/
- **Depends on**: Tasks #8, #11, #12, #13, #14, #15 (repos evaluated)
- **Assignee**: `@geepers_searcher` or manual curation
- **Time**: ~1.5 hours
- **Output**: 5-10 new snippet files organized by domain

### 20. Verify No Regressions in Existing Services
- **Source**: Plan Verification
- **Impact**: 5 | **Effort**: 1 | **Priority**: 6.5
- **Description**: After all deployments, run `sm status` to confirm no services broke. Quick health check on 3-5 critical services (swarm, diachronica, lessonplanner).
- **Files**: None (service checks)
- **Depends on**: Task #6 (Caddy reloaded), any deployments
- **Assignee**: Manual `sm` commands
- **Time**: ~15 min
- **Output**: "All services healthy" OR "Fix: [services]"

### 21. Final Verification: Timeline Page
- **Source**: Plan Verification
- **Impact**: 4 | **Effort**: 1 | **Priority**: 6.5
- **Description**: Visit https://diachronica.com/evolution/ in browser. Check: page loads, styling correct, all links work, text is readable. Screenshot for documentation.
- **Files**: None (verification only)
- **Depends on**: Task #6 (Caddy route live)
- **Assignee**: Manual browser testing
- **Time**: ~15 min
- **Output**: "Page live and verified" + screenshot

### 22. Final Verification: Public Repos
- **Source**: Plan Verification
- **Impact**: 4 | **Effort**: 1 | **Priority**: 6.0
- **Description**: Visit GitHub profiles for 5 public repos. Confirm visibility=public, READMEs display correctly, no .env leaks, MIT LICENSE present.
- **Files**: None (GitHub verification)
- **Depends on**: Task #10 (made public)
- **Assignee**: Manual GitHub browsing
- **Time**: ~15 min
- **Output**: "All repos public and clean"

### 23. Final Verification: Games Deployed
- **Source**: Plan Verification
- **Impact**: 3 | **Effort**: 1 | **Priority**: 5.0
- **Description**: If games deployed (Task #11, #12, #13), verify at dr.eamer.dev/games/. Check new entries appear, games are playable.
- **Files**: ~/html/games/
- **Depends on**: Task #11, #12, #13 (games evaluated)
- **Assignee**: Manual testing
- **Time**: ~15 min
- **Output**: "Games live and playable" OR "Skipped (no new games)"

### 24. Session Checkpoint Commit
- **Source**: Plan Verification, Wave 4
- **Impact**: 2 | **Effort**: 1 | **Priority**: 6.0
- **Description**: Commit all changes (new pages, Caddy routes, cloned repos in _archive/, SNIPPETS). Write summary: "Completed LLM history showcase and timeline page."
- **Files**: Various (git add -A after verification)
- **Depends on**: Task #20, #21, #22 (all verifications passed)
- **Assignee**: Bash (git commit) + `@geepers_orchestrator_checkpoint`
- **Time**: ~20 min
- **Output**: Commit logged, session archived

---

## Execution Roadmap

### Phase 1: Research (Start IMMEDIATELY) — 2-3 hours
**Run in parallel:**
- Task #1: Cross-ref games (1h)
- Task #2: Cross-ref eyegaze (30m)
- Task #4: Security scan repos (45m)
- Task #17: Verify bluevibes (20m)

→ **Output**: Deduplication baseline + security clearance to proceed with clones

### Phase 2: Timeline Page Build (Parallel with Phase 1) — 4-5 hours
**Run in parallel:**
- Task #5: Build timeline HTML (3h) — starts immediately
- Task #8: Clone repos (45m) — starts after Task #4

→ **Output**: Static HTML page, ready for Caddy

### Phase 3: Caddy Deployment (Sequential after Phase 2) — 15 min
- Task #6: Add /evolution/ route (15m)

→ **Output**: Page LIVE at diachronica.com/evolution/

### Phase 4: README Polish + Public Repos (Parallel, dependent on Phase 3) — 2.5 hours
**Run in parallel:**
- Task #7: Humanize READMEs (2h)
- Task #9: Add LICENSEs (30m)

→ **Output**: Repos ready to be public

### Phase 5: Make Repos Public (Sequential after Phase 4) — 10 min
- Task #10: Public visibility toggle (10m)

→ **Output**: 5 repos now public, discoverable

### Phase 6: Game Evaluation (Parallel, independent) — 4-5 hours
**Run in parallel:**
- Task #11: Evaluate ShadowLlama (2h)
- Task #12: Compare llamoria (1h)
- Task #13: Pull eyegaze interactives (1h)
- Task #14: Evaluate locAItor (2h)
- Task #15: Cross-ref bluesky_cleaner (1h)

→ **Output**: Deployment decisions, new games/tools identified

### Phase 7: Archive & Extract (Parallel with Phase 6) — 2.5 hours
**Run in parallel:**
- Task #16: Create llm-history/ (30m)
- Task #18: Verify herd-ai sync (30m)
- Task #19: Extract SNIPPETS (1.5h)

→ **Output**: Archive organized, code patterns captured

### Phase 8: Final Verification (Sequential) — 1 hour
**Run in order:**
- Task #20: Service health (15m)
- Task #21: Timeline page (15m)
- Task #22: Public repos (15m)
- Task #23: Games (15m, if applicable)

→ **Output**: All systems verified

### Phase 9: Commit + Session End — 20 min
- Task #24: Checkpoint (20m)

---

## Critical Path Summary

**Fastest route to "timeline page live":**

```
Start Here (in parallel):
├─ Task #1: Games cross-ref (1h)
├─ Task #2: Eyegaze cross-ref (30m)
├─ Task #4: Security scan (45m)
└─ Task #5: Build timeline HTML (3h) ◄── LONGEST

Then (sequential):
├─ Task #8: Clone repos (45m) [waits on #4]
└─ Task #6: Caddy route (15m) [waits on #5]

RESULT: Timeline page live after ~4 hours (not sequential, parallel)
```

---

## Blocked Tasks

### Task #7: Humanize READMEs
- **Blocked by**: Task #8 (repos must be cloned first)
- **Reason**: Can't humanize READMEs if repos aren't available locally

### Task #9: Add LICENSEs
- **Blocked by**: Task #8 (same as above)
- **Reason**: Need repo access to add license files

### Task #10: Make Repos Public
- **Blocked by**: Tasks #7 + #9 (cleanup must complete first)
- **Reason**: Can't ship public repos with poor READMEs or missing LICENSEs

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>6) | 7 |
| Medium priority (3-6) | 13 |
| Low priority (<3) | 4 |
| Quick wins (QW) | 5 |
| Blocked | 3 |
| **Total** | **24** |

| Phase | Duration | Parallelizable |
|-------|----------|---|
| Phase 1: Research | 2-3h | ✅ 4 parallel tasks |
| Phase 2: Timeline | 4-5h | ✅ 2 parallel tracks |
| Phase 3: Deploy | 15m | Sequential |
| Phase 4: Polish | 2.5h | ✅ 2 parallel |
| Phase 5: Public | 10m | Sequential |
| Phase 6: Games | 4-5h | ✅ 5 parallel |
| Phase 7: Archive | 2.5h | ✅ 3 parallel |
| Phase 8: Verify | 1h | Sequential |
| Phase 9: Commit | 20m | Sequential |
| **Total** | **~17-19h** | Best case: 5-6h with full parallelization |

---

## Next Steps

1. **Read this queue** — understand critical path
2. **Start Phase 1 immediately** — launch `/session-start` skill
3. **Run Tasks #1, #2, #4, #17 in parallel** — research phase
4. **Launch Task #5 alongside research** — timeline page build
5. **After Phase 3 complete** — share diachronica.com/evolution/ URL with user for verification
6. **Continue with phases 4-9** based on outcomes

---

## Agent Assignments

| Task | Recommended Agent |
|------|------------------|
| #1, #2, #17 | `@geepers_searcher` |
| #4 | `@geepers_security` |
| #5 | `@geepers_orchestrator_frontend` |
| #6 | `@geepers_caddy` (SOLE authority) |
| #7 | `/humanize` skill + `@geepers_readme` |
| #8, #11-15 | Bash (clone) + manual review |
| #10, #24 | Bash + `@geepers_orchestrator_checkpoint` |
| #19 | `@geepers_searcher` |
| #20-23 | Manual verification |

