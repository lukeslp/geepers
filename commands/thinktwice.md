---
description: Step back and reconsider your approach - drop assumptions, find a simpler path
---

# Think Twice

You are about to **completely reconsider your current approach**. This is an intervention - something isn't working, or you're about to sink effort into something that might be wrong.

## The Protocol

### Step 1: State Your Current Approach
Write down in ONE sentence what you're currently doing or about to do.

### Step 2: List Your Assumptions
What are you taking for granted? List every assumption:
- "This file needs to exist"
- "This is the right architecture"
- "This dependency is necessary"
- "The user wants X specifically"
- "This has to be built from scratch"

### Step 3: Challenge Each Assumption
For EACH assumption, ask:
- **Is this actually true?** Or did I just start down this path?
- **What if the opposite were true?** What would I do differently?
- **Is there a simpler version?** Can I solve 80% of the problem with 20% of the effort?

### Step 4: Find the Lazy Path
The best solution is usually the laziest one that still works. Ask:
- Can I use something that already exists? (`/reuse`)
- Can I delete code instead of adding it?
- Can I configure instead of code?
- Can I use a library instead of building?
- Is this even necessary at all?

### Step 5: Pick a DIFFERENT Angle
You MUST propose at least one alternative approach that:
- Uses a **different architecture** than what you were doing
- Is **simpler** (fewer files, fewer abstractions, fewer moving parts)
- Avoids the **specific friction** you were hitting

### Step 6: Decide
Present both approaches (original + alternative) to the user with honest tradeoffs. Let them choose.

## Red Flags That Trigger This Skill

Use `/thinktwice` when you notice:
- You're on your 3rd attempt at something
- The solution keeps getting more complex
- You're fighting the framework/system
- You're writing workarounds for workarounds
- A "simple" task is taking too long
- You're about to create a new abstraction for a one-time use
- You're about to add a dependency for one function
- The code is getting harder to explain

## Anti-Patterns This Catches

| Anti-Pattern | Better Path |
|-------------|-------------|
| Big loop with embedded data | External data file + simple renderer |
| Near-duplicate code across files | Shared module or template |
| Complex state management | Simpler data flow |
| Building from scratch | Using existing shared library |
| Over-engineering for future needs | Building for NOW |
| Adding abstraction layers | Inline the logic |
| Fighting a library's design | Use it as intended or pick a different one |

## Core Principles

1. **Simple > Complex** - If it's getting complicated, you're probably doing it wrong
2. **Delete > Add** - Removing code is always safer than adding code
3. **Reuse > Build** - Check what exists before creating
4. **Configure > Code** - Prefer configuration over implementation
5. **Now > Later** - Build for current requirements, not hypothetical future ones

## Execute

**What's going wrong / what are you reconsidering**: $ARGUMENTS

If no arguments, introspect on your most recent approach and run the protocol.
