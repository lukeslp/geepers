---
description: Deliberation engine - gather opinions from CLI tools and agents, debate, vote
---

# Consensus

Deliberation engine that gathers second opinions from multiple sources, has agents argue for and against, and synthesizes a voted recommendation.

## Execute

### Phase 1: Gather Opinions (launch ALL in the SAME message)

#### External CLI Tools (read-only)

Detect installed CLI assistants:
```bash
which codex gemini aider openclaw 2>/dev/null
```

For each found tool, send the question/task in **read-only mode** (analysis and opinion only, NO file writes):
- Frame as: "Analyze this approach and give your opinion. Do not modify any files."
- Capture their response with source attribution

#### Internal Agents (opposing briefs)

Dispatch with explicit roles:
- **@geepers_critic** — Argue AGAINST the current approach. Find every weakness, risk, and failure mode.
- **@geepers_scout** — Argue FOR the current approach. What works, what's good, what would break if we changed it.
- **@geepers_planner** — Pragmatic middle ground. Feasibility analysis, effort estimates, what's realistic.

#### Research

- **@geepers_searcher** — Web search for prior art, community patterns, blog posts about similar decisions
- **@geepers_fetcher** — Fetch any relevant documentation or reference material

### Phase 2: Deliberate

Collate all responses into a structured debate:

For each opinion:
- **Source**: which tool or agent
- **Position**: for / against / neutral
- **Confidence**: high / medium / low
- **Key reasoning**: 1-2 sentence summary of their argument

Identify:
- **Consensus points** — where most sources agree
- **Disagreements** — where sources conflict
- **Unique insights** — points only one source raised

### Phase 3: Vote and Synthesize

Score each position:
- How many sources support it?
- How strong are the arguments?
- How much evidence backs the claims?

Present:
```
Consensus: <majority view>
Confidence: <high | medium | low>

For (<count> sources):
- <key argument 1>
- <key argument 2>

Against (<count> sources):
- <key argument 1>
- <key argument 2>

Notable Dissent:
- <minority view worth considering>

Recommendation: <what to do and why>
```

Flag anything where the vote was close or where a minority argument was particularly compelling.

## Usage Examples

- `/geepers-consensus "should we use tRPC or REST for this API?"`
- `/geepers-consensus "is this refactor worth the risk?"`
- `/geepers-consensus "should we split this into microservices?"`
- `/geepers-consensus` (no args) — deliberate on current task or plan

## Distinction

- `/geepers-consensus` — "What do others think?" (external deliberation)
- `/geepers-thinkagain` — "Start over from scratch mentally" (paradigm shift)
- `/geepers-thinktwice` — "Pause, are you sure?" (caution check)

## Topic

**Question/decision**: $ARGUMENTS

If no arguments, deliberate on the current task or approach.
