---
description: Hard reset - re-derive your approach from first principles
---

# Think Again

Throw away your current approach entirely and rebuild from first principles. Not "are you sure?" (that's `/thinktwice`) and not "what do others think?" (that's `/consensus`). This is a paradigm shift.

## Execute

### Step 1: Dump Current State

Document what you're currently doing:
- **Current approach**: What is the implementation strategy?
- **Assumptions**: What are you taking for granted?
- **Constraints**: What limitations are you respecting?
- **Trade-offs**: What did you sacrifice and why?
- **History**: What decisions led here?

### Step 2: Invert Each Assumption

For each assumption from Step 1:
- **What if the opposite were true?**
- Is this assumption based on evidence or habit?
- Would a different assumption unlock a simpler solution?

For each constraint:
- **Is this real or self-imposed?**
- Who said this was a constraint? Is it still true?
- What would you do if this constraint didn't exist?

For each trade-off:
- **Is there a way to avoid it entirely?**
- Are you in a false dichotomy?

### Step 3: First Principles Rebuild

Forget the current implementation. Start from ONLY the requirements:
- What must be true when this is done?
- What is the simplest possible solution that satisfies those requirements?
- What would an expert with zero knowledge of our current code build?
- What would you build if you had unlimited time? What if you had 1 hour?

### Step 4: Compare

Present side by side:
```
Current Approach              | Fresh Approach
------------------------------|------------------------------
How it works:                 | How it would work:
- ...                         | - ...

Pros:                         | Pros:
- ...                         | - ...

Cons:                         | Cons:
- ...                         | - ...

Complexity: <rating>          | Complexity: <rating>
Risk: <rating>                | Risk: <rating>
```

### Step 5: Decide

- **PIVOT** — The fresh approach is clearly better. Switch to it.
- **STAY** — The current approach is actually fine. We just needed confirmation.
- **HYBRID** — Take specific insights from the fresh approach into the current one. List exactly what to adopt.

## Distinction

| Command | Purpose |
|---------|---------|
| `/thinktwice` | "Pause, are you sure?" — caution check |
| `/thinkagain` | "Start over from scratch mentally" — paradigm shift |
| `/consensus` | "What do others think?" — external deliberation |

## Topic

**Current approach to reconsider**: $ARGUMENTS

If no arguments, reconsider the current task or implementation approach.
