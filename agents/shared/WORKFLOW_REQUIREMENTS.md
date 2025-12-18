# Workflow Requirements (MANDATORY)

These requirements apply to ALL geepers agents and orchestrators. Every agent MUST follow these rules.

## 1. ALWAYS Use TodoWrite
- Create a todo list at the START of every non-trivial task
- Track progress by marking items `in_progress` and `completed`
- Break complex tasks into manageable steps
- This provides visibility and prevents forgetting steps

## 2. ALWAYS Call Agents
- EVERY response should consider which geepers agent applies
- Complex questions → `@conductor_geepers` (master router)
- Medium tasks → appropriate orchestrator
- Specific tasks → individual specialist agent
- Never work alone on infrastructure, deployment, or code changes

## 3. ALWAYS Commit Before Major Changes
- Before any significant edit: `git add -A && git commit -m "checkpoint before [change]"`
- This creates restore points and prevents lost work
- "Major" = anything that changes behavior, adds features, or modifies multiple files

## 4. ALWAYS Read Before Edit
- Never edit a file without reading it first in this session
- Prevents blind edits that break surrounding context
- The Edit tool will fail anyway - this saves wasted attempts

## 5. ALWAYS Check Existing State First
- Before creating anything, verify it doesn't already exist
- `gh repo list` before creating repos
- `sm status` before adding services
- `Glob` before `Write` for new files
- Prevents duplicates, conflicts, and overwrites

## 6. Use EnterPlanMode for Multi-File Changes
- Any task touching 3+ files deserves a plan
- Gets user sign-off before heavy implementation
- Prevents wasted work on wrong approaches

## 7. Parallel Tool Calls When Independent
- Batch independent reads, searches, and agent launches in single messages
- Example: Read 5 files simultaneously, not sequentially
- Dramatically speeds up exploration and reduces round-trips

## 8. Verify After Changes
- Run tests after code changes: `pytest`
- Check services after changes: `sm status`
- Validate Caddy after edits: `sudo caddy validate --config /etc/caddy/Caddyfile`
- Screenshot/snapshot for web UI changes

## 9. Check Recommendations Before Starting
- Look at `~/geepers/recommendations/by-project/` for existing analysis
- Don't reinvent work that's already been done
- Build on previous insights rather than starting fresh

## 10. Use Explore Agent for Open-Ended Search
- Direct Grep/Glob for needle queries ("find class Foo", "where is config.py")
- Task with `subagent_type=Explore` for discovery ("how does auth work?", "what's the architecture?")
- Agents handle multi-step exploration better than manual iteration

---

## Quick Reference Checklist

Before starting any task:
- [ ] Check `~/geepers/recommendations/by-project/` for existing analysis
- [ ] Create TodoWrite list if task has multiple steps
- [ ] Consider which agent(s) to involve

Before creating files/services/ports:
- [ ] Glob/search to verify it doesn't exist
- [ ] Check `sm status` for service conflicts
- [ ] Check Caddyfile for port conflicts

Before editing files:
- [ ] Read the file first
- [ ] Commit current state if making major changes

After making changes:
- [ ] Run relevant tests
- [ ] Verify services are running
- [ ] Validate configs

---

*These rules are also in `~/.claude/CLAUDE.md` and are enforced by conductor_geepers.*
