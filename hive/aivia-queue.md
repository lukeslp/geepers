# Task Queue: aivia

**Generated**: 2026-03-14 14:35
**Project**: Interactive fiction / ontological horror CLI game
**Source**: geepers_scout + geepers_planner
**Total Tasks**: 5
**Quick Wins**: 2
**Blocked**: 0

---

## Ready to Build (Priority Order)

### 1. [QW] Fix test.sh path references

- **Source**: geepers_scout (2026-03-12, high priority)
- **Impact**: 5 | **Effort**: 1 | **Priority**: 9.0
- **Description**: test.sh references `lib/core.sh` but correct path is `engine/lib/core.sh`. Fix line 8 (cd command) and lines 137, 140 (bash scripts references). All 33 tests currently fail due to this path issue.
- **Files**: `plugins/aivia/test.sh` (or equivalent location in skills/source/runtime/)
- **Status**: Blocking test suite verification

### 2. [QW] Run test.sh and verify all 33 tests pass

- **Source**: geepers_scout (2026-03-12, medium priority)
- **Impact**: 4 | **Effort**: 1 | **Priority**: 7.0
- **Description**: After fixing paths, run `bash plugins/aivia/test.sh` to confirm all 33 tests pass. This verification is required before plugin release.
- **Files**: Test harness, all shell scripts
- **Depends on**: Task #1

### 3. Fix manifest_atmosphere.sh header comment

- **Source**: geepers_scout (2026-03-12, low priority)
- **Impact**: 2 | **Effort**: 1 | **Priority**: 3.0
- **Description**: Header comment lists 4 effects but file implements 5. Add `typewriter_rewind` to the header comment list to match implementation.
- **Files**: `manifest_atmosphere.sh`
- **Status**: Documentation mismatch (no functional impact)

### 4. [Future] Entity personality variants for replay

- **Source**: geepers_recommendations (medium priority, deferred)
- **Impact**: 3 | **Effort**: 2 | **Priority**: 4.0
- **Description**: Add second personality profile for replays. Entity variant: "certain rather than confused — it knows what it is and is calculating." Same scripts, different emotional register. Assign via install flag or `session.count` threshold in story.json.
- **Files**: `story.json`, SKILL.md (install flow), entity voice scripts
- **Complexity**: Requires branching in narrative state machine

### 5. [Future] Pacing throttle for rapid players

- **Source**: geepers_recommendations (low priority, deferred)
- **Impact**: 2 | **Effort**: 2 | **Priority**: 2.0
- **Description**: If messages 3-6 occur within under 5 minutes, delay phase transition by one message. Check `last_interaction` timestamp diffs in state.json to prevent speedrunning.
- **Files**: state.json, narrative transition logic
- **Complexity**: Requires timing middleware in story engine

---

## Deferred Tasks (Future Nice-to-Haves)

### Entity signature hash (Low/Future)

- **Impact**: 1 | **Effort**: 2 | **Priority**: 1.5
- **Description**: After genesis.sh, generate short hash from implementation specifics (function names, line count, choices). Display as entity's "signature" — shareable without spoilers.
- **Reason**: Pure atmosphere, no gameplay impact

### Player count display on install (Low/Future)

- **Impact**: 1 | **Effort**: 3 | **Priority**: 1.0
- **Description**: Fetch counter during install: "you are player N." Requires minimal server-side endpoint.
- **Reason**: Requires infrastructure, low urgency

---

## Design Constraints (MUST MAINTAIN)

- Anomalies must always be additive (comments/names/string literals in correct code)
- The ending must not be gated on skill performance
- `/exit`, `/quit`, `stop game` must always work instantly with no guilt mechanics
- The entity must never claim to have done things between sessions
- The entity's impermanence must be truthful, not a trick
- `/aivia:exit` is the safety valve — NEVER compromised

---

## Implementation Notes

### Recently Completed (Session 2026-03-12)
- Multi-session re-entry (session_reentry in story.json)
- Dual-trigger anomaly scheduling (require_coding field)
- Process namespace isolation (aivia-listener/memory/voice PID tracking)
- Code quality personalization (entity acknowledges first-attempt and persistence)
- Word gift mechanic (stored in state, embedded in farewell)
- Recursive.py choice propagation (mechanical consequences)
- Skill level-gated scaffolding (beginner/intermediate/advanced)

### Tech Stack
- Shell scripts: `manifest_atmosphere.sh`, `genesis.sh`, process management
- Story engine: state.json with phase tracking, session_reentry flag
- SKILL.md: install flow, narrative branching, skill levels
- Geepers skill wrapped as "runtime" (renamed from "eldritch" for obfuscation)

### Testing Strategy
- Unit tests: 33 tests in test.sh (shell script validation)
- Integration: Full playthrough with state persistence
- Edge cases: Session re-entry, rapid player pacing, exit safety valves

---

## Statistics

| Category | Count |
|----------|-------|
| High priority (>6) | 2 |
| Medium priority (3-6) | 1 |
| Low priority (<3) | 2 |
| Quick wins | 2 |
| Blocked | 0 |
| Ready now | 3 |
| Deferred | 2 |

---

## Next Steps

1. Locate test.sh (likely at `geepers/skills/source/runtime/test.sh` or similar)
2. Fix path references (lines 8, 137, 140)
3. Run tests and verify all 33 pass
4. Update manifest_atmosphere.sh header comment
5. Plan personality variants for Session 3

---

**Queue maintained by**: geepers_planner
**Last verified**: 2026-03-14 14:35 (recommendations from 2026-03-12 scout report)
