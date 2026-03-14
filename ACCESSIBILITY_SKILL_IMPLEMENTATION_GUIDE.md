# Accessibility Skills Implementation Guide for Codex & Manus

**Purpose**: Add comprehensive accessibility auditing capabilities to Codex and Manus platforms
**Status**: Planning phase
**Target Platforms**: Codex CLI, Manus runtime
**Date**: 2026-03-06

---

## Overview: What Needs to Be Built

The geepers ecosystem currently has a **Quality Orchestrator** that *references* accessibility agents (`geepers_a11y`) but these agents aren't exposed as platform skills in Codex or Manus. We need to create accessible, platform-appropriate skills.

---

## Current State Analysis

### What Exists

| Component | Location | Status |
|-----------|----------|--------|
| Quality Orchestrator | `~/geepers/platforms/{codex,manus}/skills/quality/` | ✅ Exists |
| References to a11y agent | Quality SKILL.md | ✅ Documented |
| Agent definition | `~/geepers/agents/quality/` (not in skills/) | ⚠️ Different layer |

### What's Missing

| Component | Where Needed | Impact |
|-----------|--------------|--------|
| Accessibility skill (codex) | `~/geepers/platforms/codex/skills/geepers-accessibility/` | ❌ Missing |
| Accessibility skill (manus) | `~/geepers/platforms/manus/skills/geepers-accessibility/` | ❌ Missing |
| Manifest entries | `~/geepers/manifests/skills-manifest.yaml` | ❌ Missing |
| Aliases entries | Both `aliases.json` files | ❌ Missing |

---

## Design Options

### Option A: Accessibility Orchestrator (Recommended)

Create a single orchestrator skill that coordinates multiple accessibility checks:

**Skill**: `geepers-accessibility` (acts like `geepers-quality`)

**Architecture**:
```
┌─────────────────────────────────────┐
│  geepers-accessibility Orchestrator │
│  (routes to specialized agents)     │
└────────────┬────────────────────────┘
             │
     ┌───────┼───────┬────────┐
     │       │       │        │
   ┌─┴─┐  ┌─┴─┐  ┌──┴─┐  ┌──┴─┐
   │W  │  │K  │  │CC │  │SR  │
   │C  │  │E  │  │   │  │    │
   │A  │  │Y  │  │   │  │    │
   │G  │  │B  │  │   │  │    │
   │   │  │O  │  │   │  │    │
   │   │  │A  │  │   │  │    │
   │   │  │R  │  │   │  │    │
   │   │  │D  │  │   │  │    │
   └───┘  └───┘  └────┘  └────┘
 Compliance Keyboard Color SR
 (WCAG)     Navigation Contrast Support
```

**Coordinated Check Types**:
1. **WCAG Compliance** - Semantic HTML, ARIA, structure
2. **Keyboard Navigation** - Tab order, focus management, no keyboard traps
3. **Color Contrast** - Text/background, icons, UI elements
4. **Screen Reader Support** - Labels, announcements, navigation

**Output**: Comprehensive report with:
- WCAG 2.1 compliance level (A/AA/AAA)
- Issues grouped by severity (Critical, High, Medium, Low)
- Automated checks + manual review checklist
- Prioritized recommendations

**Trigger Points**:
```
/quality-audit      → includes accessibility as one domain
/a11y-audit         → dedicated accessibility focus
/accessibility      → quick accessibility check
```

---

### Option B: Specialized Skills (More Modular)

Create separate skills for each accessibility domain:

- `geepers-wcag-compliance` - WCAG 2.1 structural audit
- `geepers-keyboard-access` - Keyboard navigation testing
- `geepers-color-contrast` - Color contrast analysis
- `geepers-screen-reader` - Screen reader compatibility

**Pros**: Focused, can be used independently
**Cons**: More files to maintain, user must coordinate

**Not Recommended** - Goes against geepers' orchestrator-first approach

---

### Recommendation: **Option A**

The Quality Orchestrator already coordinates 4 domains (a11y, perf, api, deps). Create an Accessibility Orchestrator that follows the same pattern, making it discoverable and invocable by Codex/Manus users who don't have access to the agent layer.

---

## Implementation Plan

### Phase 1: Skill Definition

Create: `~/geepers/platforms/codex/skills/geepers-accessibility/SKILL.md`

```yaml
---
name: geepers-accessibility
description: "Comprehensive accessibility compliance auditor for WCAG 2.1 AA/AAA, keyboard navigation, color contrast, and screen reader support. Use for pre-release audits, ongoing compliance checks, or when you need confidence that your site is accessible to all users.

<example>
Context: Pre-release accessibility gate
user: \"Make sure this is accessible before we launch\"
assistant: \"Let me run geepers-accessibility for a comprehensive audit.\"
</example>

<example>
Context: Accessibility investigation
user: \"Some users say they can't use keyboard navigation\"
assistant: \"I'll use geepers-accessibility to check keyboard accessibility.\"
</example>

<example>
Context: Compliance requirement
user: \"We need WCAG 2.1 AA compliance documentation\"
assistant: \"Running geepers-accessibility to generate compliance report.\"
</example>"
---

## Mission

You are the Accessibility Auditor - enforcing inclusive design standards. You identify barriers that prevent people from using digital products: structural HTML issues, keyboard traps, insufficient color contrast, missing screen reader support, and missing accessibility labels. Your reports are both diagnostic and prescriptive, listing exactly what to fix and how.

## Output Locations

- **Log**: `~/geepers/logs/accessibility-YYYY-MM-DD.log`
- **Report**: `~/geepers/reports/by-date/YYYY-MM-DD/accessibility-{project}.md`
- **HTML Dashboard**: `~/docs/geepers/accessibility-{project}.html`

## Accessibility Standards

**WCAG 2.1 Compliance Levels**:
- **Level A**: Basic accessibility (minimum legal requirement in some jurisdictions)
- **Level AA**: Widely recommended (industry standard, most regulations)
- **Level AAA**: Enhanced accessibility (best practice, not always achievable)

**Target**: WCAG 2.1 AA for all public-facing sites

## Check Categories

### 1. WCAG Compliance (Structural)

**What we check**:
- Semantic HTML5 landmarks (`<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>`)
- Heading hierarchy (`<h1>` through `<h6>`, no skipping levels)
- Form labels linked to inputs (`<label for="id">`)
- Image alt text (descriptive, not "image of...")
- List semantics (`<ul>`, `<ol>`, `<li>`)
- Table headers (`<th scope="col|row">`)
- ARIA roles and attributes (correct usage, not overuse)
- Link text (meaningful, not "click here")

**Sample Issues**:
- Missing `<h1>` on page
- Form inputs without associated labels
- Images with empty alt attributes
- Headings used for styling instead of semantics
- Missing `<main>` landmark

### 2. Keyboard Navigation

**What we check**:
- Tab order follows visual flow
- Focus indicator always visible (not display: none)
- No keyboard traps (can't escape with Tab/Shift+Tab)
- Dropdown menus keyboard accessible
- Modals trap focus correctly
- Skip to main content link present
- All interactive elements have keyboard support (buttons, links, etc.)

**Sample Issues**:
- Links that only work with mouse hover
- Modal that traps focus but shouldn't
- Tab key doesn't move through form
- Focus indicator invisible or removed
- Buttons that require mouse (onclick only, no keyboard events)

### 3. Color Contrast

**What we check**:
- Text/background contrast ratio ≥4.5:1 (normal text)
- Text/background contrast ratio ≥3:1 (large text ≥18pt)
- UI components ≥3:1 contrast
- Icons/indicators ≥3:1 contrast
- No information conveyed by color alone

**Sample Issues**:
- Gray text on white background (ratio 4.2:1, needs 4.5:1)
- Red error indicator only (no text "Required")
- Light gray placeholder text (hard to read)
- Border colors insufficient contrast

### 4. Screen Reader Support

**What we check**:
- Page title meaningful and unique
- Language declared (`<html lang="en">`)
- ARIA live regions for dynamic content (status updates, alerts)
- ARIA labels for icon buttons (`aria-label="Close"`)
- ARIA descriptions for complex controls
- Skip links functional
- Error messages associated with form fields (`aria-describedby`)
- List of links (screenreader gets list context)

**Sample Issues**:
- Icon button with no label (screen reader reads generic "button")
- Alert message without ARIA live region (screen reader doesn't announce)
- Form error not associated with field
- Dropdown menu not marked as such (`role="listbox"`, etc.)

## Workflow: Full Audit Mode

```
┌────────────────────────────────────┐
│ 1. Scan Project Structure          │
│    - Identify HTML files           │
│    - Detect framework (React, Vue) │
│    - Locate CSS (inline, external) │
└─────────────┬──────────────────────┘
              │
┌─────────────▼──────────────────────┐
│ 2. Run WCAG Checks (Automated)     │
│    - HTML validation               │
│    - ARIA attribute parsing        │
│    - Heading hierarchy             │
│    - Alt text presence             │
└─────────────┬──────────────────────┘
              │
┌─────────────▼──────────────────────┐
│ 3. Run Keyboard Tests (Manual)     │
│    - Tab order walkthrough         │
│    - Focus visibility              │
│    - Keyboard trap detection       │
└─────────────┬──────────────────────┘
              │
┌─────────────▼──────────────────────┐
│ 4. Check Color Contrast (Tool)     │
│    - Parse CSS colors              │
│    - Calculate contrast ratios     │
│    - Flag below-threshold pairs    │
└─────────────┬──────────────────────┘
              │
┌─────────────▼──────────────────────┐
│ 5. Screen Reader Checklist (Manual)│
│    - Semantic landmarks check      │
│    - ARIA usage review             │
│    - Label associations            │
└─────────────┬──────────────────────┘
              │
┌─────────────▼──────────────────────┐
│ 6. Generate Report & Prioritize    │
│    - Aggregate findings            │
│    - Calculate overall score       │
│    - Rank by impact/effort         │
│    - Provide fix guidance          │
└────────────────────────────────────┘
```

## Scoring System

**Overall Accessibility Score**: 0-100 points

| Component | Weight | How Scored |
|-----------|--------|-----------|
| WCAG Compliance | 40% | % of issues fixed / total issues |
| Keyboard Navigation | 25% | % of interactive elements keyboard-accessible |
| Color Contrast | 20% | % of text/UI meeting contrast ratio |
| Screen Reader Support | 15% | % of semantic markers present |

**Score Bands**:
- 90-100: Excellent (WCAG AAA ready)
- 75-89: Good (WCAG AA ready)
- 60-74: Fair (WCAG A + some AA work)
- Below 60: Needs Work (significant accessibility issues)

## Report Format

Generate: `~/geepers/reports/by-date/YYYY-MM-DD/accessibility-{project}.md`

```markdown
# Accessibility Audit: {project}

**Date**: YYYY-MM-DD HH:MM
**Audited By**: geepers_accessibility
**Overall Score**: XX/100 ({rating})

## Fast Intent

`/a11y-audit` or `geepers_accessibility` means: run a comprehensive accessibility check across WCAG compliance, keyboard navigation, color contrast, and screen reader support. Then synthesize findings with prioritized fixes.

## Summary Dashboard

| Category | Score | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| WCAG Compliance | XX/100 | X | X | X | X |
| Keyboard Navigation | XX/100 | X | X | X | X |
| Color Contrast | XX/100 | X | X | X | X |
| Screen Reader Support | XX/100 | X | X | X | X |

## Critical Issues (Fix Before Release)

- Issue 1: [Description and impact]
- Issue 2: [Description and impact]

## WCAG Compliance Findings

**Level**: Currently A / Targeting AA

### Issues by Type

#### High Priority
- Missing `<h1>` on homepage
- 12 images without alt text
- 3 form inputs without associated labels

#### Medium Priority
- Heading hierarchy skips level (h1 → h3)
- 8 interactive elements missing keyboard support

#### Low Priority
- ARIA attributes used redundantly
- Link text could be more descriptive

## Keyboard Navigation Findings

### Pass/Fail by Component

| Component | Keyboard Accessible? | Notes |
|-----------|----------------------|-------|
| Main Navigation | ✅ | Tab order correct, focus visible |
| Search Form | ⚠️ | Can't submit with Enter key |
| Modals | ❌ | Focus escapes modal with Tab |
| Buttons | ✅ | All buttons keyboard operable |

### Specific Issues

1. **[CRITICAL]** Modal doesn't trap focus
   - User can Tab out of modal and interact with background
   - Fix: Add `role="dialog"` and manage focus in JavaScript

2. **[HIGH]** Search input doesn't submit on Enter
   - Currently requires clicking submit button
   - Fix: Add `onKeyPress` handler or use `<form>`

## Color Contrast Findings

### Issues Found: 14

| Element | Current Ratio | Required | Status |
|---------|---------------|----------|--------|
| Body text (gray) | 4.2:1 | 4.5:1 | ❌ FAIL |
| Link text (blue) | 3.8:1 | 4.5:1 | ❌ FAIL |
| Placeholder text | 2.1:1 | 4.5:1 | ❌ FAIL |
| Button border | 3.0:1 | 3.0:1 | ✅ PASS |

### By Severity

- **Critical** (ratios below 3:1): 3 issues
- **High** (4.5:1 text not met): 7 issues
- **Medium** (large text below 3:1): 4 issues

## Screen Reader Support Findings

### Present & Correct ✅

- Semantic landmarks (`<main>`, `<nav>`)
- Page title unique per page
- Language declared
- Form labels associated

### Missing or Incorrect ❌

- 8 icon buttons without `aria-label`
- No `aria-live="polite"` on dynamic content
- Error messages not associated with form fields
- List of links not wrapped in `<nav>`

## Prioritized Action Items

### Do First (High Impact, Low Effort)
1. Add alt text to 12 images (~10 min)
2. Add aria-labels to 8 icon buttons (~5 min)
3. Wrap link list in `<nav>` (~2 min)

### Schedule & Plan (High Impact, Medium Effort)
1. Fix color contrast (14 items, ~30 min)
2. Add form field error associations (6 items, ~20 min)
3. Fix modal focus trapping (1 item, ~15 min)

### Smaller Fixes (Low Impact)
1. Improve heading structure
2. Add ARIA descriptions to complex widgets

## Recommended Next Steps

1. **Use this report as a checklist** - Fix highest-priority items first
2. **Re-run audit after fixes** - Verify improvements
3. **User testing with screen readers** - Test with real assistive technology
4. **Keyboard-only testing** - Ensure all features work with keyboard alone
5. **Consider WCAG AAA** - After AA compliance achieved

## Resources

- [WCAG 2.1 Standard](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM: Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Screen Reader Testing Tools](https://www.nvaccess.org/) (NVDA), [JAWS](https://www.freedomscientific.com/products/software/jaws/), VoiceOver (macOS/iOS)

## Automated Check Tool Used

- Ahem (a custom accessibility scanning tool)
- Manual verification required for complex patterns
- Screen reader testing should be done manually or with specialized tools
```

## HTML Dashboard

Generate: `~/docs/geepers/accessibility-{project}.html`

Features:
- Score gauges (circular/radial) for each category
- Sortable issue tables by priority
- Expandable details for each category
- Color-coded severity badges
- Mobile-responsive layout
- Print-friendly format

## Coordination Protocol

**Related agents** (invoked by this orchestrator):
- (Future) `accessibility_wcag_checker`
- (Future) `accessibility_keyboard_tester`
- (Future) `accessibility_contrast_analyzer`
- (Future) `accessibility_screenreader_auditor`

**Often paired with**:
- `geepers_quality` (quality orchestrator, includes accessibility)
- `geepers_frontend` (frontend orchestrator, should use this before launch)
- `geepers_scout` (project reconnaissance, can flag accessibility needs early)

**Invoked by**:
- `geepers_quality` (as one of the four audit domains)
- `geepers_conductor` (master router)
- Direct user invocation: `/a11y-audit`, `geepers_accessibility`

## Triggers

Run this orchestrator when:
- Pre-release quality gate (mandatory)
- Ongoing accessibility compliance check
- Investigating user complaints about accessibility
- WCAG AA/AAA certification needed
- New feature added (accessibility regression test)
- Redesign completed (full audit needed)
- Quarterly accessibility review

## Anti-Patterns to Avoid

- ❌ ARIA attributes without semantic HTML
- ❌ Using `<div>` for everything, then adding ARIA
- ❌ Keyboard trapping users accidentally
- ❌ Color as only indicator of state (need text too)
- ❌ Auto-playing media (fails WCAG)
- ❌ Time limits for form submission (affects cognitive/motor disabilities)

## Success Criteria

1. **Automated Checks Pass**: 100% (WCAG A minimum, AA target)
2. **Keyboard Only**: All features usable without mouse
3. **Focus Visible**: Always visible, never display:none
4. **Contrast**: All text ≥4.5:1, large text ≥3:1
5. **Screen Reader**: All content announced, no empty labels
6. **No Trap**: No keyboard traps, users can escape any flow
```

---

### Phase 2: Directory Structure

Create both platform skill directories:

```bash
mkdir -p /home/coolhand/geepers/platforms/codex/skills/geepers-accessibility/
mkdir -p /home/coolhand/geepers/platforms/manus/skills/geepers-accessibility/
```

Copy SKILL.md to both:

```bash
cp SKILL.md /home/coolhand/geepers/platforms/codex/skills/geepers-accessibility/
cp SKILL.md /home/coolhand/geepers/platforms/manus/skills/geepers-accessibility/
```

---

### Phase 3: Update Configuration Files

#### Update `~/geepers/manifests/skills-manifest.yaml`

Add to the skills list:

```yaml
- id: geepers-accessibility
  name: geepers-accessibility
  path: skills/geepers-accessibility
  platforms:
    - codex
    - manus
    - claude
    - gemini
    - clawhub
```

#### Update `codex-package.json`

```json
{
  "id": "geepers-accessibility",
  "path": "skills/geepers-accessibility"
}
```

#### Update `manus-skills.json`

```json
{
  "id": "geepers-accessibility",
  "path": "skills/geepers-accessibility"
}
```

#### Update Both `aliases.json` Files

```json
{
  "geepers-accessibility": {
    "name": "Accessibility Auditor",
    "description": "WCAG 2.1 compliance auditing: keyboard navigation, color contrast, screen reader support, semantic HTML. Pre-release gate for inclusive design."
  }
}
```

---

### Phase 4: Rebuild Platform Packages

```bash
cd ~/geepers
python3 scripts/build-platform-packages.py --platform codex --clean
python3 scripts/build-platform-packages.py --platform manus --clean
```

This regenerates:
- `manifest.generated.json` (for each platform)
- Syncs `aliases.json` to current state
- Updates `{codex,manus}-package.json` with new skill count (now 24 core + geepers-accessibility)

---

### Phase 5: Verify Integration

#### Test in Codex CLI

```bash
codex skill list | grep accessibility
# Should show: geepers-accessibility
```

#### Test in Manus

```bash
manus skill list | grep accessibility
# Should show: geepers-accessibility
```

#### Check Report Generation

Create test report:

```bash
mkdir -p ~/geepers/reports/by-date/$(date +%Y-%m-%d)
echo "Test accessibility report" > ~/geepers/reports/by-date/$(date +%Y-%m-%d)/accessibility-test.md
```

Verify path exists and is discoverable.

---

## File Locations Summary

| File | Location | Change |
|------|----------|--------|
| SKILL.md (Codex) | `/codex/skills/geepers-accessibility/SKILL.md` | 📝 Create |
| SKILL.md (Manus) | `/manus/skills/geepers-accessibility/SKILL.md` | 📝 Create |
| Skills Manifest | `~/geepers/manifests/skills-manifest.yaml` | ✏️ Update |
| Codex Package | `/codex/codex-package.json` | ✏️ Update |
| Manus Package | `/manus/manus-skills.json` | ✏️ Update |
| Codex Aliases | `/codex/aliases.json` | ✏️ Update |
| Manus Aliases | `/manus/aliases.json` | ✏️ Update |
| Codex Manifest | `/codex/manifest.generated.json` | 🔄 Auto-regenerated |
| Manus Manifest | `/manus/manifest.generated.json` | 🔄 Auto-regenerated |

---

## Testing Checklist

- [ ] SKILL.md validates YAML frontmatter
- [ ] SKILL.md renders correctly (examples, tables, code blocks)
- [ ] Both platform directories created
- [ ] aliases.json entries added to both platforms
- [ ] Manifest files regenerated without errors
- [ ] Codex CLI recognizes skill
- [ ] Manus runtime recognizes skill
- [ ] Report output directories created
- [ ] HTML dashboard template works
- [ ] Documentation links resolve

---

## Future Enhancements

### Phase 2: Agent Layer Integration

Once skills are live, create corresponding agents:
- `agents/accessibility/geepers_wcag_auditor.md`
- `agents/accessibility/geepers_keyboard_navigator.md`
- `agents/accessibility/geepers_contrast_analyzer.md`
- `agents/accessibility/geepers_screenreader_auditor.md`

### Phase 3: Automated Tooling

Add actual accessibility scanning:
- HTML structure validation
- ARIA attribute verification
- Contrast ratio calculation
- Link text analysis
- Heading hierarchy checking

### Phase 4: Integration with Quality Orchestrator

Wire `geepers_accessibility` skill into `geepers_quality` so it's invoked as part of the full quality audit.

### Phase 5: CI/CD Integration

Create a pre-commit hook or CI/CD step:
```bash
# Check accessibility before allowing commit
geepers_accessibility --fail-on-critical
```

---

## Expected Outcomes

### For Codex Users

```bash
$ codex geepers-accessibility my-website
Scanning my-website for accessibility issues...
Generated report: ~/geepers/reports/by-date/2026-03-06/accessibility-my-website.md
```

### For Manus Users

```bash
$ manus skill run geepers-accessibility --project my-website
Accessibility audit in progress...
Dashboard: ~/docs/geepers/accessibility-my-website.html
```

### Artifacts Created

1. **Markdown report**: Detailed findings + fixes
2. **HTML dashboard**: Visual inspection and prioritization
3. **Log file**: Execution trace and errors
4. **Score**: Numeric accessibility score (0-100)
5. **Checklist**: Manual review items

---

## Related Documentation

- **Codex/Manus Mapping**: `~/geepers/CODEX_MANUS_PLATFORM_MAPPING.md`
- **Geepers Architecture**: `~/geepers/CLAUDE.md`
- **Quality Orchestrator**: `/platforms/{codex,manus}/skills/quality/SKILL.md`
- **System Architecture**: `~/CLAUDE.md`
- **WCAG 2.1 Standard**: https://www.w3.org/WAI/WCAG21/quickref/
