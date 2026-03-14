#!/usr/bin/env python3
"""Generate a self-contained HTML reference site for the Geepers ecosystem.

Walks agents/, skills/source/geepers-*/, and commands/ to produce a single
index.html with embedded data, search, tabs, and decision-tree filtering.

Usage:
    python3 scripts/generate-reference.py
"""

import html
import os
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Frontmatter parser (stdlib only, no PyYAML)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> dict[str, str]:
    """Extract YAML frontmatter key: value pairs between --- delimiters."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}
    fm_block = "\n".join(lines[1:end])
    result: dict[str, str] = {}
    for m in re.finditer(r'^(\w[\w_-]*)\s*:\s*(.+)', fm_block, re.MULTILINE):
        key = m.group(1)
        val = m.group(2).strip()
        # Strip surrounding quotes
        if (val.startswith('"') and val.endswith('"')) or \
           (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        result[key] = val
    return result


def first_heading(text: str) -> str | None:
    """Return the first # heading after frontmatter."""
    in_fm = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped == "---":
            in_fm = not in_fm
            continue
        if in_fm:
            continue
        m = re.match(r'^#\s+(.+)', stripped)
        if m:
            return m.group(1).strip()
    return None


# ---------------------------------------------------------------------------
# Collectors
# ---------------------------------------------------------------------------

def collect_agents() -> list[dict]:
    agents_dir = REPO_ROOT / "agents"
    items = []
    if not agents_dir.is_dir():
        return items
    for md_path in sorted(agents_dir.rglob("*.md")):
        # Skip shared/ subdirectory
        rel = md_path.relative_to(agents_dir)
        parts = rel.parts
        if "shared" in parts:
            continue
        # Skip files in the root of agents/ (like AGENT_DOMAINS.md)
        if len(parts) < 2:
            continue
        domain = parts[0]  # subdirectory name = domain
        text = md_path.read_text(errors="replace")
        fm = parse_frontmatter(text)
        if not fm.get("name") and not fm.get("description"):
            continue  # No usable frontmatter
        name = fm.get("name", md_path.stem)
        desc = fm.get("description", "")
        # Clean up escaped newlines and example blocks from description
        desc = desc.replace("\\n", " ").strip()
        # Truncate at first <example> tag if present
        ex_idx = desc.find("<example>")
        if ex_idx > 0:
            desc = desc[:ex_idx].strip()
        model = fm.get("model", "")
        color = fm.get("color", "")
        items.append({
            "type": "agent",
            "name": name,
            "description": desc,
            "category": domain,
            "model": model,
            "color": color,
        })
    return items


def collect_skills() -> list[dict]:
    source_dir = REPO_ROOT / "skills" / "source"
    items = []
    if not source_dir.is_dir():
        return items
    for skill_dir in sorted(source_dir.iterdir()):
        if not skill_dir.is_dir() or not skill_dir.name.startswith("geepers-"):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        text = skill_md.read_text(errors="replace")
        fm = parse_frontmatter(text)
        skill_id = skill_dir.name  # e.g. geepers-checkpoint
        name = fm.get("name", skill_id)
        desc = fm.get("description", "")
        desc = desc.replace("\\n", " ").strip()
        ex_idx = desc.find("<example>")
        if ex_idx > 0:
            desc = desc[:ex_idx].strip()
        items.append({
            "type": "skill",
            "name": name,
            "description": desc,
            "category": "skills",
            "skill_id": skill_id,
        })
    return items


def collect_commands() -> list[dict]:
    cmd_dir = REPO_ROOT / "commands"
    items = []
    if not cmd_dir.is_dir():
        return items
    for md_path in sorted(cmd_dir.glob("*.md")):
        text = md_path.read_text(errors="replace")
        fm = parse_frontmatter(text)
        desc = fm.get("description", "")
        desc = desc.replace("\\n", " ").strip()
        title = first_heading(text) or md_path.stem
        cmd_name = "/" + md_path.stem  # e.g. /geepers-start
        items.append({
            "type": "command",
            "name": cmd_name,
            "title": title,
            "description": desc,
            "category": "commands",
        })
    return items


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def escape_js_string(s: str) -> str:
    """Escape a string for embedding in a JS string literal."""
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "\\'")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "")
    s = s.replace("<", "\\x3c")
    s = s.replace(">", "\\x3e")
    return s


def build_js_data(agents, skills, commands) -> str:
    """Build a JS array literal from collected data."""
    lines = ["const DATA = ["]
    for item in agents + skills + commands:
        name = escape_js_string(item["name"])
        desc = escape_js_string(item.get("description", ""))
        cat = escape_js_string(item.get("category", ""))
        typ = item["type"]
        extra = ""
        if typ == "agent":
            model = escape_js_string(item.get("model", ""))
            color = escape_js_string(item.get("color", ""))
            extra = f', model: "{model}", agentColor: "{color}"'
        elif typ == "skill":
            sid = escape_js_string(item.get("skill_id", ""))
            extra = f', skillId: "{sid}"'
        elif typ == "command":
            title = escape_js_string(item.get("title", ""))
            extra = f', title: "{title}"'
        lines.append(f'  {{type: "{typ}", name: "{name}", description: "{desc}", category: "{cat}"{extra}}},')
    lines.append("];")
    return "\n".join(lines)


def generate_html(agents, skills, commands) -> str:
    js_data = build_js_data(agents, skills, commands)
    agent_count = len(agents)
    skill_count = len(skills)
    cmd_count = len(commands)

    # Use raw strings and careful brace escaping for the HTML template
    html_out = []
    html_out.append('<!DOCTYPE html>')
    html_out.append('<html lang="en">')
    html_out.append('<head>')
    html_out.append('<meta charset="UTF-8">')
    html_out.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_out.append('<title>Geepers Reference</title>')
    html_out.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
    html_out.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    html_out.append('<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Work+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">')
    html_out.append('<style>')
    html_out.append(CSS)
    html_out.append('</style>')
    html_out.append('</head>')
    html_out.append('<body>')
    html_out.append(f'''
<div class="header">
  <h1>Geepers Reference</h1>
  <p class="subtitle">
    <span class="accent">{skill_count}</span> skills,
    <span class="accent">{agent_count}</span> agents,
    <span class="accent">{cmd_count}</span> commands
  </p>
</div>

<div class="search-wrap">
  <input type="text" id="search" placeholder="Search agents, skills, and commands..." autocomplete="off" spellcheck="false">
</div>

<div class="decision-tree">
  <h3>I want to...</h3>
  <div class="dt-buttons">
    <button class="dt-btn" data-filter="swarm,hive,engineering,builder">Build something</button>
    <button class="dt-btn" data-filter="hunt,research,dream-cascade">Search for info</button>
    <button class="dt-btn" data-filter="quality,audit">Review quality</button>
    <button class="dt-btn" data-filter="start,checkpoint,end">Start / end session</button>
    <button class="dt-btn" data-filter="deploy,ship,canary">Deploy safely</button>
    <button class="dt-btn" data-filter="consensus,thinktwice,thinkagain">Get second opinion</button>
    <button class="dt-btn" data-filter="janitor,checkpoint">Clean up</button>
    <button class="dt-btn" data-filter="system-onboard,scout">Understand codebase</button>
  </div>
</div>

<div class="tabs">
  <button class="tab-btn active" data-tab="skill">Skills</button>
  <button class="tab-btn" data-tab="agent">Agents</button>
  <button class="tab-btn" data-tab="command">Commands</button>
</div>

<div class="count-bar" id="countBar"></div>
<div class="grid" id="grid"></div>
''')
    html_out.append('<script>')
    html_out.append(js_data)
    html_out.append(JS)
    html_out.append('</script>')
    html_out.append('</body>')
    html_out.append('</html>')
    return "\n".join(html_out)


CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0a0a0f;
  color: #e0e0e0;
  font-family: 'Work Sans', sans-serif;
  font-weight: 400;
  min-height: 100vh;
  line-height: 1.6;
}
h1, h2, h3 { font-family: 'Libre Baskerville', serif; }
a { color: #4fc3f7; text-decoration: none; }
a:hover { text-decoration: underline; }

.header {
  text-align: center;
  padding: 48px 24px 24px;
}
.header h1 {
  font-size: 2.4rem;
  color: #fff;
  margin-bottom: 8px;
}
.header .subtitle {
  color: #888;
  font-size: 1rem;
  font-weight: 300;
}
.header .accent { color: #4fc3f7; font-weight: 500; }

.search-wrap {
  max-width: 640px;
  margin: 24px auto;
  padding: 0 24px;
}
.search-wrap input {
  width: 100%;
  padding: 14px 20px;
  font-size: 16px;
  font-family: 'Work Sans', sans-serif;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 10px;
  color: #e0e0e0;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.search-wrap input:focus {
  border-color: #4fc3f7;
  box-shadow: 0 0 0 3px rgba(79,195,247,0.15);
}
.search-wrap input::placeholder { color: #666; }

.decision-tree {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 24px;
  text-align: center;
}
.decision-tree h3 {
  color: #888;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 12px;
  font-family: 'Work Sans', sans-serif;
  font-weight: 500;
}
.dt-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}
.dt-btn {
  padding: 8px 16px;
  font-size: 0.85rem;
  font-family: 'Work Sans', sans-serif;
  font-weight: 500;
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  color: #ccc;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.dt-btn:hover { border-color: rgba(79,195,247,0.4); color: #4fc3f7; }
.dt-btn.active { border-color: #4fc3f7; color: #4fc3f7; background: rgba(79,195,247,0.1); }

.tabs {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin: 28px auto 20px;
  max-width: 480px;
  padding: 0 24px;
}
.tab-btn {
  flex: 1;
  padding: 12px 0;
  text-align: center;
  font-family: 'Work Sans', sans-serif;
  font-size: 0.95rem;
  font-weight: 500;
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.08);
  border-bottom: 3px solid transparent;
  color: #888;
  cursor: pointer;
  transition: all 0.2s;
}
.tab-btn:first-child { border-radius: 10px 0 0 10px; }
.tab-btn:last-child { border-radius: 0 10px 10px 0; }
.tab-btn:hover { color: #bbb; }
.tab-btn.active {
  color: #4fc3f7;
  border-bottom-color: #4fc3f7;
  background: rgba(79,195,247,0.06);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px 60px;
}

.card {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 20px;
  transition: border-color 0.2s;
}
.card:hover { border-color: rgba(79,195,247,0.3); }
.card-name {
  font-weight: 600;
  font-size: 1.05rem;
  color: #4fc3f7;
  margin-bottom: 6px;
  word-break: break-word;
}
.card-title {
  font-size: 0.85rem;
  color: #aaa;
  margin-bottom: 6px;
  font-style: italic;
}
.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 10px;
}
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  color: #111;
  white-space: nowrap;
}
.card-desc {
  font-size: 0.9rem;
  color: #bbb;
  line-height: 1.5;
}
.no-results {
  grid-column: 1 / -1;
  text-align: center;
  color: #666;
  padding: 60px 20px;
  font-size: 1.1rem;
}

.count-bar {
  text-align: center;
  color: #555;
  font-size: 0.82rem;
  margin-bottom: 16px;
}

@media (max-width: 640px) {
  .header h1 { font-size: 1.6rem; }
  .grid { grid-template-columns: 1fr; padding: 0 12px 40px; }
  .tabs { flex-direction: column; gap: 6px; }
  .tab-btn { border-radius: 8px !important; border-bottom-width: 2px; }
  .dt-buttons { gap: 6px; }
  .dt-btn { font-size: 0.8rem; padding: 6px 12px; }
}
"""

JS = """
const BADGE_COLORS = {
  checkpoint: "#4fc3f7",
  quality: "#81c784",
  frontend: "#ff8a65",
  research: "#ce93d8",
  deploy: "#ffb74d",
  datavis: "#4dd0e1",
  games: "#e57373",
  standalone: "#90a4ae",
  system: "#a1887f",
  hive: "#fff176",
  master: "#4fc3f7",
  corpus: "#ce93d8",
  fullstack: "#ff8a65",
  web: "#ff8a65",
  python: "#81c784",
  commands: "#b0bec5",
  skills: "#7986cb"
};

let activeTab = "skill";
let searchQuery = "";
let dtFilter = "";
let debounceTimer = null;

function badgeColor(cat) {
  return BADGE_COLORS[cat] || "#90a4ae";
}

function matchesDT(item) {
  if (!dtFilter) return true;
  const terms = dtFilter.split(",");
  const hay = (item.name + " " + item.description + " " + item.category + " " + (item.title || "") + " " + (item.skillId || "")).toLowerCase();
  return terms.some(function(t) { return hay.includes(t.trim()); });
}

function matchesSearch(item) {
  if (!searchQuery) return true;
  const hay = (item.name + " " + item.description + " " + (item.title || "") + " " + item.category + " " + (item.skillId || "")).toLowerCase();
  return hay.includes(searchQuery);
}

function escapeHtml(s) {
  var d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function renderCard(item) {
  var extra = "";
  if (item.type === "command" && item.title) {
    extra = '<div class="card-title">' + escapeHtml(item.title) + '</div>';
  }
  var modelBadge = "";
  if (item.type === "agent" && item.model) {
    modelBadge = '<span class="badge" style="background:rgba(255,255,255,0.12);color:#aaa;font-size:0.7rem;">' + escapeHtml(item.model) + '</span>';
  }
  var bg = badgeColor(item.category);
  return '<div class="card">' +
    '<div class="card-name">' + escapeHtml(item.name) + '</div>' +
    extra +
    '<div class="card-meta">' +
    '<span class="badge" style="background:' + bg + '">' + escapeHtml(item.category) + '</span>' +
    modelBadge +
    '</div>' +
    '<div class="card-desc">' + escapeHtml(item.description) + '</div>' +
    '</div>';
}

function render() {
  var filtered = DATA.filter(function(item) {
    return item.type === activeTab && matchesSearch(item) && matchesDT(item);
  });
  var grid = document.getElementById("grid");
  var countBar = document.getElementById("countBar");
  if (filtered.length === 0) {
    grid.innerHTML = '<div class="no-results">No matches found.</div>';
    countBar.textContent = "0 results";
  } else {
    grid.innerHTML = filtered.map(renderCard).join("");
    var label = activeTab === "skill" ? "skills" : activeTab === "agent" ? "agents" : "commands";
    countBar.textContent = filtered.length + " " + label;
  }
}

// Tabs
document.querySelectorAll(".tab-btn").forEach(function(btn) {
  btn.addEventListener("click", function() {
    document.querySelectorAll(".tab-btn").forEach(function(b) { b.classList.remove("active"); });
    btn.classList.add("active");
    activeTab = btn.dataset.tab;
    render();
  });
});

// Search (debounced)
document.getElementById("search").addEventListener("input", function(e) {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(function() {
    searchQuery = e.target.value.trim().toLowerCase();
    if (searchQuery) {
      dtFilter = "";
      document.querySelectorAll(".dt-btn").forEach(function(b) { b.classList.remove("active"); });
    }
    render();
  }, 150);
});

// Decision tree
document.querySelectorAll(".dt-btn").forEach(function(btn) {
  btn.addEventListener("click", function() {
    var wasActive = btn.classList.contains("active");
    document.querySelectorAll(".dt-btn").forEach(function(b) { b.classList.remove("active"); });
    if (wasActive) {
      dtFilter = "";
    } else {
      btn.classList.add("active");
      dtFilter = btn.dataset.filter;
      document.getElementById("search").value = "";
      searchQuery = "";
      // Switch to the most relevant tab
      var types = ["agent", "skill", "command"];
      for (var ti = 0; ti < types.length; ti++) {
        var t = types[ti];
        var terms = dtFilter.split(",");
        var hasMatch = DATA.some(function(item) {
          if (item.type !== t) return false;
          var hay = (item.name + " " + item.description + " " + item.category + " " + (item.title || "") + " " + (item.skillId || "")).toLowerCase();
          return terms.some(function(term) { return hay.includes(term.trim()); });
        });
        if (hasMatch) {
          activeTab = t;
          document.querySelectorAll(".tab-btn").forEach(function(b) {
            b.classList.toggle("active", b.dataset.tab === t);
          });
          break;
        }
      }
    }
    render();
  });
});

// Initial render
render();
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    agents = collect_agents()
    skills = collect_skills()
    commands = collect_commands()

    print(f"Parsed {len(agents)} agents, {len(skills)} skills, {len(commands)} commands")

    out_dir = REPO_ROOT / "docs" / "reference"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    out_file.write_text(generate_html(agents, skills, commands))

    print(f"Generated docs/reference/index.html")


if __name__ == "__main__":
    main()
