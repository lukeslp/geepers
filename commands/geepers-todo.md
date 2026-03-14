---
description: Todoist integration - capture tasks, sync work logs, manage backlog across projects
---

# Todo Mode

Integrate with Todoist for task management across all projects.

## Todoist Agent

@geepers_todoist handles:
- Capturing tasks from work sessions
- Syncing accomplishments to Todoist
- Prioritizing backlog items
- Project-task alignment

## Quick Actions

### Capture from Session
After completing work, capture next steps:
```
/geepers-todo capture
```
Extracts TODOs, open questions, and next steps from the session.

### Daily Wrap-up
```
/geepers-todo wrap
```
Summarizes what was shipped today, updates Todoist with recap.

### Quick Add
```
/geepers-todo add "Task description" --project Work --priority p1
```
Direct task creation with project and priority.

## Workflows

### Session → Todoist Sync
1. @geepers_status - Log accomplishments
2. @geepers_todoist - Push to Todoist
3. Extract open questions as tasks

### Backlog Triage
1. @geepers_planner - Parse existing plans
2. @geepers_todoist - Reconcile with Todoist
3. Prioritize by impact/effort

### Cross-Project Planning
1. Review `~/geepers/recommendations/by-project/`
2. @geepers_todoist - Create tasks from recommendations
3. Align to Todoist projects

## Project Mapping

| Codebase | Todoist Project |
|----------|-----------------|
| ~/html/datavis/ | Work - Datavis |
| ~/html/bluesky/ | Work - Bluesky |
| ~/servers/ | Work - Infrastructure |
| ~/projects/ | Work - Development |

## Integration Points

- **Session start**: Check Todoist for today's tasks
- **Session end**: Capture accomplished work
- **Checkpoint**: Sync progress mid-session
- **Planning**: Pull tasks into work queue

## Execute

**Action**: $ARGUMENTS

If no arguments:
- Show today's tasks from Todoist

If "capture" or "sync":
- Capture session work to Todoist

If "wrap" or "end":
- Daily wrap-up with full sync

If "add <task>":
- Quick task creation

If "backlog":
- Review and prioritize backlog
