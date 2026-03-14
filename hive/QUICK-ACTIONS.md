# Quick Actions - Post-Session Audit (2026-03-07)

## 🚀 Start Here - Do These First (30 min)

```bash
# 1. Add llamoria to games index
cd /home/coolhand/html/games
# Edit index.html, add card in "Classic" section (copy line 296-300 pattern)
# Insert between line 307-308 (after Star Trek, before Nonograms)

# 2. Scrub xAI key from locAItor
cd /home/coolhand/projects/_archive/llm-history/locAItor
# Edit app.py line 36-39
# CURRENT: XAI_API_KEY = os.getenv('XAI_API_KEY', 'xai-8zAk...')
# CHANGE TO: XAI_API_KEY = os.getenv('XAI_API_KEY')  # Require env var

# 3. Verify llamoria Caddy routing
sudo caddy validate --config /etc/caddy/Caddyfile
# Check for handle_path /games/llamoria/* or /games/* pattern
# If missing, add: handle_path /games/llamoria/* { root * /home/coolhand/html/games/llamoria; file_server }

# 4. Add MIT LICENSE to 4 lukeslp repos
for repo in dreamwalker con-text jeepers-legacy eyegaze; do
  cat > /home/coolhand/LICENSE-TEMPLATE.txt << 'EOF'
MIT License

Copyright (c) 2023-2026 Luke Steuber

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
EOF
  # cp /home/coolhand/LICENSE-TEMPLATE.txt ~/git/lukeslp/$repo/LICENSE
done
```

**Status after Phase 1**: Games updated, keys secured, licenses added (~30 min)

---

## 📋 Phase 2 - Humanization (2 hours)

```bash
# For each of 4 lukeslp repos (dreamwalker, con-text, jeepers-legacy, eyegaze)
# Use /humanize skill to remove "AI-powered", "AI-enhanced", "AI-driven" terminology
# Replace with "language model", specific model names, or descriptive text

# Example:
# WRONG: "AI-powered image generation"
# RIGHT: "Image generation using language models"
# ALSO OK: "Image generation using OpenAI's DALL-E"

# Script:
cd ~/git/lukeslp/{REPO}
# Read current README.md, note AI terminology
# Use /humanize skill
# Review changes
git diff
git add README.md
git commit -m "docs: humanize content, remove AI terminology"
git push
```

---

## 🔒 Critical Security Items (Can Delegate to @geepers_security)

### .env Audit (4-6 hours)
17 committed .env files with exposed secrets. See `/home/coolhand/geepers/recommendations/by-project/projects-wide.md` lines 13-33.

```bash
# Find all committed .env files:
grep -r "\.env" /home/coolhand/projects/.gitignore
find /home/coolhand/projects -name ".env" -type f

# For each:
# 1. Audit for API keys, database passwords, tokens
# 2. Remove from git history: git filter-repo --path .env --invert-paths
# 3. Add to .gitignore
# 4. Rotate exposed credentials on third-party services
# 5. Create .env.example template

# After scrubbing: git push --force-with-lease (if needed)
```

---

## ✅ Quality Checks (1-2 hours, can delegate)

### Timeline Pages - Run /quality-audit skill
```bash
# Check dr.eamer.dev/datavis/evolution/ and diachronica.com/evolution/
# Verify:
# - WCAG 2.1 AA compliance (keyboard nav, screen reader, contrast)
# - Lighthouse score 90+
# - Mobile responsive (test at 375px width)
# - No console errors
```

---

## 📦 Publishing (1 hour, after humanization + licenses)

```bash
# Publish 4 lukeslp repos from private to public
# Via GitHub web UI or gh CLI:
gh repo edit lukeslp/dreamwalker --visibility=public
gh repo edit lukeslp/con-text --visibility=public
gh repo edit lukeslp/jeepers-legacy --visibility=public
gh repo edit lukeslp/eyegaze --visibility=public

# Then update portfolio/documentation links if needed
```

---

## 📝 Task Queue & Full Reference

**Priority task queue**: `/home/coolhand/geepers/hive/post-session-audit-queue.md`
**Full recommendations**: `/home/coolhand/geepers/recommendations/by-project/projects-wide.md`
**Session summary**: `/home/coolhand/geepers/reports/by-date/2026-03-07/post-session-summary.md`

---

## 🎯 Quick Priority

| Do First | Estimate | Value |
|----------|----------|-------|
| Add llamoria to games index | 15min | HIGH |
| Scrub xAI key from locAItor | 15min | CRITICAL |
| Add MIT LICENSE (4 repos) | 30min | HIGH |
| Humanize 4 lukeslp READMEs | 2h | HIGH |
| Quality audit timelines | 1h | MEDIUM |
| Publish 4 repos to public | 1h | HIGH |
| **Security audit on .env files** | 4h | **CRITICAL** |

---

## 💡 Pro Tips

- **Games index edit**: Copy-paste card template from lines 296-300 or 308-312
- **Llamoria verification**: Load https://dr.eamer.dev/games/llamoria/ and test gameplay
- **Humanize skill**: Outputs corrected text; review before committing
- **API key rotation**: After scrubbing locAItor, verify xAI key is regenerated on their console
- **Caddy reload**: `sudo systemctl reload caddy` after config changes
- **Git safety**: Always `git log --oneline -3` before committing (agents may be running in parallel)

---

## 🤖 Delegate These to Agents

```
@geepers_security    → .env audit, key management (4h)
@geepers_readme      → Generate README.md for apis/, clinical/ (2h)
@geepers_docs        → Create CLAUDE.md for linguistic-api (1h)
@geepers_a11y        → Accessibility audit on timelines (1h)
@geepers_perf        → Performance audit on timelines (1h)
/humanize skill      → Clean up 4 lukeslp READMEs (2h)
/quality-audit skill → Full QA on timeline pages (1h)
```

---

**Generated**: 2026-03-07 14:00
**Next step**: Pick an item from "Do First" table and start

