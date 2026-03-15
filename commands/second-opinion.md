---
description: Get alternative perspectives from 3 LLM providers (Codex, Gemini, Grok) on a task or inquiry
---

# Second Opinion - Multi-LLM Consultation

Get perspectives from **3 different LLM providers** on the same task or question. Useful for:
- Validating approaches before implementation
- Exploring alternative solutions
- Getting diverse technical perspectives
- Fact-checking or research verification

## Providers

| Tool | Provider | Model | Weight | Strength |
|------|----------|-------|--------|----------|
| Codex CLI | OpenAI | gpt-5.2-codex (auto) | **HIGH** | Strongest reasoning, code correctness |
| Gemini CLI | Google | Gemini 3 Pro (auto-routed) | **HIGH** | Large context, multimodal |
| Aider | xAI | grok-3 | NEUTRAL | Fast, creative problem-solving |

### Provider Weighting

When synthesizing, **not all opinions are equal**. Codex and Gemini are the anchors - treat their responses as the primary signal. Grok is a tiebreaker or creative wildcard.

- **HIGH weight** (Codex, Gemini): If both agree, that's the default answer. Disagreement between them is the most interesting signal.
- **NEUTRAL weight** (Grok): Breaks ties, adds creative angles. Carries full weight when it aligns with an anchor.

## SAFETY: READ-ONLY MODE REQUIRED

All tools are for CONSULTATION ONLY - never allow writes.

- **Codex**: ALWAYS use `--sandbox read-only`
- **Gemini**: ALWAYS use `-s` (sandbox mode) - NEVER use `-y` (YOLO auto-approves all writes!)
- **Aider**: ALWAYS use `--no-git --no-auto-commits --exit` (no file changes, exits after response)

## How to Execute

### Step 1: Run ALL 3 in Parallel

Use Bash tool to run ALL commands simultaneously (three parallel Bash calls in ONE message).

**IMPORTANT**: Wrap aider calls with `timeout 90` to prevent hangs.

**For exploratory questions / research:**
```bash
# 1. Codex (OpenAI) - READ-ONLY sandbox
codex exec --sandbox read-only "PROMPT_HERE" 2>&1

# 2. Gemini (Google Gemini 3 Pro) - SANDBOX mode, auto-routes to best model
gemini -s "PROMPT_HERE" 2>&1

# 3. Aider + xAI (Grok 3) - with timeout
source ~/.aider.env && timeout 90 aider --model xai/grok-3 --no-git --no-auto-commits --yes --exit --message "PROMPT_HERE" 2>&1
```

**For code review tasks:**
```bash
# 1. Codex - read-only review
codex exec --sandbox read-only "Review this code for issues: $(cat /path/to/file | head -200)" 2>&1

# 2. Gemini - sandbox review
gemini -s "Review this code for issues: $(cat /path/to/file | head -200)" 2>&1

# 3. Aider + Grok 3
source ~/.aider.env && timeout 90 aider --model xai/grok-3 --no-git --no-auto-commits --yes --exit --message "Review this code for issues: $(cat /path/to/file | head -200)" 2>&1
```

### Step 2: Capture and Compare

After all complete, present results in this format:

```markdown
## Second Opinion Results

### Codex (OpenAI) Says:
[response summary - key points only, not raw output]

### Gemini (Google) Says:
[response summary]

### Grok 3 (xAI) Says:
[response summary]

---

### Synthesis

**Anchor consensus** (Codex + Gemini agree):
- [Highest confidence - this is the default answer unless strongly challenged]

**Anchor split** (Codex vs Gemini disagree):
- [Most interesting signal - detail both positions, note where Grok lands as tiebreaker]

**Wildcard insights** (raised by Grok but missed by anchors):
- [Flag for human review - may be valuable even if anchors didn't mention it]

**Risk / uncertainty:**
- [What could ALL of them be wrong about?]

**Recommended next action:**
- [Concrete step: run this test, check this file, try this approach]
```

## CLI Reference

### Codex CLI (OpenAI)
```bash
# SAFE: Read-only sandbox (ALWAYS use this)
codex exec --sandbox read-only "prompt" 2>&1

# DANGEROUS - DO NOT USE for second-opinion:
# codex exec "prompt"               # Can write files!
```

### Gemini CLI (Google)
```bash
# SAFE: Sandbox mode (ALWAYS use this)
# Auto-routes to Gemini 3 Pro for complex tasks (previewFeatures enabled)
gemini -s "prompt" 2>&1

# DANGEROUS - NEVER USE for second-opinion:
# gemini -y "prompt"                # YOLO mode - auto-approves ALL writes!
```

### Aider + xAI (Grok 3)
```bash
# SAFE: No git, no auto-commits, exits after response, 90s timeout
source ~/.aider.env && timeout 90 aider --model xai/grok-3 --no-git --no-auto-commits --yes --exit --message "prompt" 2>&1
```

## Model Update Notes

Keep these models current. Last verified: 2026-02-12.

| Provider | Model string | How to check |
|----------|-------------|--------------|
| Codex/OpenAI | Auto (gpt-5.2-codex) | `codex --version` - uses latest by default |
| Gemini | Auto-routed (Gemini 3 Pro) | previewFeatures=true in ~/.gemini/settings.json |
| xAI/Grok | `xai/grok-3` | Check xai.com for newer models |

**API keys**: xAI key in `~/.aider.env`, codex/gemini use system env.

**Future providers to watch**: DeepSeek R1 (need API key), Llama via Groq/Together (open-source diversity).

## Example Usage Patterns

### Architecture Decision
```bash
# Run ALL 3 in parallel (THREE Bash calls in ONE message):
codex exec --sandbox read-only "Pros and cons of Redis vs Memcached for session storage in Flask?" 2>&1

gemini -s "Pros and cons of Redis vs Memcached for session storage in Flask?" 2>&1

source ~/.aider.env && timeout 90 aider --model xai/grok-3 --no-git --no-auto-commits --yes --exit --message "Pros and cons of Redis vs Memcached for session storage in Flask?" 2>&1
```

### Code Review
```bash
codex exec --sandbox read-only "Review this code: $(cat ./app.py | head -300)" 2>&1

gemini -s "Review this Flask application for security issues: $(cat ./app.py | head -300)" 2>&1

source ~/.aider.env && timeout 90 aider --model xai/grok-3 --no-git --no-auto-commits --yes --exit --message "Review for bugs and security issues: $(cat ./app.py | head -300)" 2>&1
```

## Important Notes

1. **Always run all 3 in parallel** - three Bash tool calls in a single message
2. **Use exec mode for Codex** - avoids interactive prompts
3. **Use -s for Gemini** - sandbox mode prevents file modifications
4. **Source .aider.env for aider** - loads API key for xAI
5. **Wrap aider calls with `timeout 90`** - prevents hangs from slow API responses
6. **Capture stderr** - use `2>&1` to see any errors
7. **Context limits** - keep file content under ~500 lines for reliable processing
8. **Partial failure is OK** - if 1 provider fails/times out, synthesize from what you got

## Error Handling

If a CLI fails:
- **Codex**: Check `codex login` for auth issues
- **Gemini**: Run `gemini` interactively first to authenticate; may timeout on long prompts
- **Aider/xAI**: Verify `XAI_API_KEY` in `~/.aider.env`

If a provider times out, note it in the synthesis and proceed with available responses.

## Now Execute

Run all 3 CLIs in parallel on the following task/question. Present a comparative analysis using the synthesis format above.

**Query**: $ARGUMENTS
