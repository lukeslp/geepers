---
description: Game development workflow - engagement, mechanics, Godot, React games, gamification
---

# Game Mode

Develop and improve games with focus on engagement, mechanics, and player experience.

## Games Orchestrator

Launch @geepers_orchestrator_games to coordinate:

| Agent | Focus |
|-------|-------|
| @geepers_gamedev | Gameplay mechanics, level design, game feel |
| @geepers_game | Gamification, reward systems, engagement loops |
| @geepers_godot | Godot Engine, GDScript, scene architecture |
| @geepers_react | React-based browser games |

## Your Games

```
~/html/games/
├── cube/              # 3D cube game
├── escape-velocity/   # Space game
├── hexsweeper/        # Hex minesweeper
├── micro-*/           # Micro game collection
├── moria/             # Roguelike
├── nonograms/         # Logic puzzles
├── star-trek/         # Star Trek game
├── wumpus/            # Hunt the Wumpus
└── ...many more
```

## Design Principles

**Game Feel:**
- Responsive controls (< 100ms input lag)
- Satisfying feedback (visual, audio, haptic)
- Juice (screen shake, particles, easing)
- Polish the core loop first

**Engagement:**
- Clear goals, immediate feedback
- Difficulty curves (not walls)
- Variable rewards (dopamine hits)
- Session-appropriate length

**Accessibility:**
- Keyboard navigation
- Colorblind modes
- Adjustable difficulty
- Pause/save anywhere

## Workflows

### Improve Game Feel
1. @geepers_gamedev - Analyze current feel
2. Identify friction points
3. Add juice (feedback, polish)
4. Playtest and iterate

### Add Gamification to App
1. @geepers_game - Design engagement mechanics
2. Identify reward opportunities
3. Implement progress systems
4. Balance for retention

### New Game Development
1. @geepers_gamedev - Core mechanic design
2. @geepers_react or @geepers_godot - Implementation
3. @geepers_game - Engagement layer
4. @geepers_a11y - Accessibility review

### Debug Game Issues
1. @geepers_diag - Error patterns
2. @geepers_webperf - Performance bottlenecks
3. @geepers_gamedev - Gameplay issues

## Quick Checks

**Performance:** 60fps target, profile with devtools
**Mobile:** Touch controls, viewport scaling
**Audio:** Mute toggle, volume control
**Save:** LocalStorage for progress

## Execute

**Mode**: $ARGUMENTS

If no arguments:
- Show games overview and guidance

If game name (e.g., "cube", "hexsweeper"):
- Focus on that specific game

If "feel":
- Game feel analysis and improvement

If "engage" or "gamify":
- Gamification design session

If "new":
- Start new game development workflow
