# Skill Research Summary: Codex & Manus Accessibility Integration

**Research Date**: 2026-03-06
**Researcher**: Claude Code
**Objective**: Understand Codex and Manus platform structures to enable accessibility skill development

---

## Quick Facts

| Aspect | Finding |
|--------|---------|
| **Total Platforms** | 5 (Claude, Codex, Manus, Gemini, ClawHub) |
| **Platform Parity** | 100% - identical skill structure across all 5 |
| **Shared Skill Base** | 23 core + 28 API variant skills |
| **Codex Skills Dir** | `/home/coolhand/geepers/platforms/codex/skills/` |
| **Manus Skills Dir** | `/home/coolhand/geepers/platforms/manus/skills/` |
| **Manifest Source** | `~/geepers/manifests/skills-manifest.yaml` (single source of truth) |
| **Build Script** | `scripts/build-platform-packages.py` (rebuilds all platforms) |
| **Existing A11y** | Quality orchestrator coordinates a11y, but no dedicated skill |
| **Next Step** | Create `geepers-accessibility` skill in both platforms |

---

## Key Findings

### 1. Platform Structure is Identical

Codex and Manus are treated as **peer platforms**:
- Same `skills/` directory structure
- Same SKILL.md format
- Same metadata (aliases.json, package manifests)
- Same naming conventions
- Same skill count (47 directories each)

**Implication**: Build once, deploy to both. No special handling needed.

### 2. Single Source of Truth Pattern

```
Canonical Source
      ↓
~/geepers/manifests/skills-manifest.yaml
      ↓
build-platform-packages.py
      ↓
        ├── ~/geepers/platforms/codex/ (generated)
        ├── ~/geepers/platforms/manus/ (generated)
        ├── ~/geepers/platforms/claude/ (generated)
        ├── ~/geepers/platforms/gemini/ (generated)
        └── ~/geepers/platforms/clawhub/ (generated)
```

**Implication**: Update the manifest once; all platforms regenerate automatically.

### 3. Skill Format is Standardized

Every skill follows identical structure:
```
skill-name/
├── SKILL.md                    ← Primary definition (Markdown + YAML frontmatter)
├── scripts/                    ← Optional: utility scripts
├── src/                        ← Optional: server implementation
├── reference/                  ← Optional: documentation
├── dist/                       ← Optional: pre-built artifacts
└── README.md                   ← Optional: installation guide
```

**The SKILL.md file IS the skill**. Everything else is supporting material.

### 4. Quality Orchestrator Already Covers A11y

**Found**:
- Quality SKILL.md references `geepers_a11y` agent
- Quality generates accessibility findings
- Quality produces WCAG compliance reports

**Problem**:
- `geepers_a11y` is an agent (lives in Claude Code's agent layer)
- No corresponding **skill** that Codex/Manus users can invoke
- Users can't access accessibility checks without using Quality orchestrator

**Implication**: We need a dedicated `geepers-accessibility` skill.

### 5. Skills vs. Agents are Different Layers

| Layer | Location | Runtime | Visibility |
|-------|----------|---------|------------|
| **Skills** | `platforms/*/skills/` | Codex CLI, Manus, Claude Desktop | Skill invocation (`/skill-name`) |
| **Agents** | `agents/` | Claude Code MCP connection | Agent invocation (Task tool) |

Skills are **user-facing**. Agents are **behind-the-scenes**.

### 6. No Existing Accessibility-Only Skills

Searched all 47 skill directories in both platforms:
- ✅ Quality orchestrator (includes a11y)
- ✅ Frontend orchestrator (references design/css agents)
- ❌ No standalone accessibility skill
- ❌ No WCAG auditor skill
- ❌ No keyboard navigation skill
- ❌ No color contrast checker skill

---

## Documentation Discovered

### Primary Resources

1. **`~/CLAUDE.md`** (Root CLAUDE.md)
   - System-wide architecture overview
   - Service management patterns
   - Port allocation
   - Technology stacks

2. **`~/geepers/CLAUDE.md`** (Geepers CLAUDE.md)
   - Geepers-specific architecture
   - Agent hierarchy
   - Python package structure
   - Orchestrator patterns
   - Skill organization

3. **`~/geepers/platforms/codex/README.md`**
   - Codex-specific installation & overview
   - List of 23 core skills
   - Ecosystem overview

4. **Quality Orchestrator SKILL.md**
   - Accessible at both:
     - `/codex/skills/quality/SKILL.md`
     - `/manus/skills/quality/SKILL.md`
   - Shows expected quality skill format
   - Demonstrates a11y coordination

### Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| `codex-package.json` | Codex skill manifest | `/codex/` |
| `manus-skills.json` | Manus skill manifest | `/manus/` |
| `aliases.json` | Skill ID→name mappings | `/codex/` and `/manus/` |
| `manifest.generated.json` | Canonical manifest | Both platforms |
| `SYNC_INFO.md` | Build metadata | Both platforms |

---

## Actionable Insights

### For Accessibility Skill Development

1. **Create SKILL.md in Both Locations**:
   - `/codex/skills/geepers-accessibility/SKILL.md`
   - `/manus/skills/geepers-accessibility/SKILL.md`
   - Use template from `quality/SKILL.md` as reference

2. **Update Manifests**:
   - Add entry to `~/geepers/manifests/skills-manifest.yaml`
   - Regenerate all platforms: `build-platform-packages.py`

3. **Add Aliases**:
   - Update `/codex/aliases.json`
   - Update `/manus/aliases.json`

4. **Follow Established Patterns**:
   - Use same SKILL.md format as Quality
   - Organize checks into 4 domains (WCAG, Keyboard, Contrast, SR)
   - Output reports to `~/geepers/reports/by-date/YYYY-MM-DD/`
   - Generate both Markdown and HTML reports

### Skills to Create (Priority Order)

**Phase 1 (Core)**: 1 skill
- [ ] `geepers-accessibility` - Comprehensive orchestrator (like quality)

**Phase 2 (Optional)**: 4 specialized skills
- [ ] `geepers-wcag-compliance` - Structural HTML/ARIA
- [ ] `geepers-keyboard-access` - Keyboard navigation
- [ ] `geepers-color-contrast` - Color contrast analysis
- [ ] `geepers-screen-reader` - Screen reader support

**Recommendation**: Start with Phase 1 (orchestrator), add Phase 2 specialists only if demand exists.

---

## Build & Deploy Process

### Current Build Pipeline

```bash
# Edit source in ~/geepers/manifests/skills-manifest.yaml
$ vim ~/geepers/manifests/skills-manifest.yaml

# Rebuild all 5 platforms
$ python3 ~/geepers/scripts/build-platform-packages.py --platform codex --clean
$ python3 ~/geepers/scripts/build-platform-packages.py --platform manus --clean
$ python3 ~/geepers/scripts/build-platform-packages.py --platform claude --clean
$ python3 ~/geepers/scripts/build-platform-packages.py --platform gemini --clean
$ python3 ~/geepers/scripts/build-platform-packages.py --platform clawhub --clean

# Or rebuild all at once
$ python3 ~/geepers/scripts/build-platform-packages.py --all --clean
```

### After Creating Skills

1. **Add to manifest.yaml**: Register new skill
2. **Rebuild platforms**: Run build script
3. **Verify**: Check both platform directories
4. **Test**: Use in Codex and Manus CLI
5. **Commit**: Git commit all changes

---

## File Inventory

### Codex Platform

```
~/geepers/platforms/codex/
├── README.md                    (67 lines)
├── aliases.json
├── codex-package.json           (100 lines, 23 core skills)
├── manifest.generated.json      (30 lines, auto-generated)
├── SYNC_INFO.md                 (13 lines)
└── skills/                      (47 directories)
    ├── quality/
    │   └── SKILL.md             ← Template for new skills
    ├── builder/
    ├── geepers-accessibility/   ← TO CREATE
    └── [44 other skills...]
```

### Manus Platform

```
~/geepers/platforms/manus/
├── README.md                    (67 lines)
├── aliases.json
├── manus-skills.json            (100 lines, 23 core skills)
├── manifest.generated.json      (30 lines, auto-generated)
├── SYNC_INFO.md                 (13 lines)
└── skills/                      (47 directories)
    ├── quality/
    │   └── SKILL.md             ← Template for new skills
    ├── builder/
    ├── geepers-accessibility/   ← TO CREATE
    └── [44 other skills...]
```

### Shared Resources

| Path | Purpose |
|------|---------|
| `~/geepers/CODEX_MANUS_PLATFORM_MAPPING.md` | This detailed mapping (created during research) |
| `~/geepers/ACCESSIBILITY_SKILL_IMPLEMENTATION_GUIDE.md` | Implementation guide with complete SKILL.md template (created during research) |
| `~/geepers/manifests/skills-manifest.yaml` | Single source of truth for all skills |
| `~/geepers/scripts/build-platform-packages.py` | Build script that regenerates all platforms |

---

## Key Questions Answered

### Q: Are Codex and Manus treated the same way?
**A**: Yes, completely. Same structure, same skills, same build process. No special handling.

### Q: Where does the skill actually come from?
**A**: It's defined in SKILL.md, a Markdown file with YAML frontmatter. Everything else is optional.

### Q: What if I update Codex skills, do I need to update Manus separately?
**A**: No. Update the source manifest, rebuild both platforms, they stay in sync.

### Q: Can I just copy-paste the Quality skill and rename it?
**A**: Yes! Quality is an orchestrator that coordinates a11y checks. Accessibility skill can follow the same pattern.

### Q: Where do reports go?
**A**: `~/geepers/reports/by-date/{YYYY-MM-DD}/` - this is the established convention.

### Q: Do I need to write server code for the accessibility skill?
**A**: Not required. Quality orchestrator is pure SKILL.md with no server. Can add one later if needed.

### Q: How do users invoke this skill?
**A**: In Codex: `codex geepers-accessibility`. In Manus: `manus skill run geepers-accessibility`.

---

## Comparison: Codex vs. Claude vs. Manus

| Feature | Codex | Claude (Code) | Manus |
|---------|-------|---------------|-------|
| **Entry Point** | CLI command | Claude Code plugin | Runtime/API |
| **Skill Format** | SKILL.md | Same | Same |
| **Agent Access** | Via skills only | Direct MCP connection | Via skills only |
| **Report Output** | `~/geepers/reports/` | Same | Same |
| **Skill Count** | 47 (23 core + 28 API) | Same | Same |
| **Build Process** | Single source (manifests/) | Same | Same |

**Key Insight**: Codex and Manus are basically the same platform implemented for different UIs. Skills are the public interface.

---

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|-----------|
| Manifest out of sync | Medium | Always rebuild after manifest edits |
| Duplicate SKILL.md maintenance | Low | Link or single source approach |
| Platform-specific needs | Low | Add "Codex Notes" or "Manus Notes" sections |
| Report output not found | Low | Use standard path: `~/geepers/reports/by-date/` |
| Skill not discovered | Low | Verify aliases.json and manifest entries |

---

## Implementation Timeline

### Week 1: Foundation
- [ ] Create SKILL.md with complete specification
- [ ] Create both platform directories
- [ ] Update manifests and aliases
- [ ] Run build script
- [ ] Verify discovery in both platforms

### Week 2: Integration
- [ ] Wire into Quality orchestrator
- [ ] Create agent layer (optional, for Claude Code)
- [ ] Document usage patterns
- [ ] Create example reports

### Week 3: Validation
- [ ] Test with actual websites
- [ ] Verify report generation
- [ ] User feedback & iteration
- [ ] Documentation updates

---

## Next Steps

### Immediate (This Session)

1. ✅ Research completed - two detailed guides created:
   - `CODEX_MANUS_PLATFORM_MAPPING.md` - Structure & configuration
   - `ACCESSIBILITY_SKILL_IMPLEMENTATION_GUIDE.md` - Complete implementation plan

2. Ready for implementation:
   - SKILL.md template provided
   - File locations documented
   - Build process explained

### Short Term (Next Session)

1. Create `geepers-accessibility/` directories in both platforms
2. Implement complete SKILL.md with checklist details
3. Update all configuration files
4. Run build script
5. Test in Codex CLI and Manus runtime

### Medium Term

1. Create agent layer (`agents/accessibility/`)
2. Add automated scanning tools
3. Integrate with Quality orchestrator
4. CI/CD pipeline support

---

## Resources Provided

### Documentation Files (Created)

1. **`CODEX_MANUS_PLATFORM_MAPPING.md`** (11KB)
   - Complete directory structure
   - Configuration file formats
   - Platform comparison table
   - File inventory
   - Build instructions
   - Integration patterns

2. **`ACCESSIBILITY_SKILL_IMPLEMENTATION_GUIDE.md`** (25KB)
   - Design options (Orchestrator vs. Specialized)
   - Complete SKILL.md template (600+ lines)
   - Accessibility check categories
   - Workflow diagrams
   - Report format specification
   - HTML dashboard mockup
   - Implementation phases
   - Testing checklist
   - Future enhancements

3. **`SKILL_RESEARCH_SUMMARY.md`** (This file)
   - Executive summary of findings
   - Key insights
   - Quick reference facts
   - Q&A responses
   - Implementation timeline
   - Risk assessment

### Existing Documentation

- `~/CLAUDE.md` - System architecture
- `~/geepers/CLAUDE.md` - Geepers architecture
- `~/geepers/platforms/*/README.md` - Platform overviews
- `~/geepers/platforms/*/skills/quality/SKILL.md` - Quality orchestrator reference

---

## Conclusion

The Codex and Manus platforms are structurally identical, well-organized systems using a single-source-of-truth architecture. Adding accessibility skills is straightforward:

1. **Create SKILL.md** - Define accessibility auditing capability
2. **Create directories** - Same path in both platforms
3. **Update manifests** - Register skill in source manifest
4. **Rebuild platforms** - Single command syncs all 5 platforms
5. **Test & deploy** - Verify discoverability and functionality

The implementation guide provides a complete SKILL.md template with all necessary components (WCAG checks, keyboard navigation, color contrast, screen reader support, scoring system, report format).

**Recommendation**: Start with Phase 1 (single orchestrator skill) using the provided template. Add specialized skills only if demand warrants.

All necessary information has been gathered. Ready to implement on next pass.
