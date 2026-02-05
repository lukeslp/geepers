# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **centralized snippet library** containing production-ready code patterns extracted from real-world AI/LLM projects. Each snippet is self-contained, immediately usable, and includes comprehensive documentation with usage examples.

## Testing Snippets

Most snippets are directly executable with their built-in examples:

```bash
# Test any snippet by running it directly
python api-clients/multi_provider_abstraction.py
python tool-registration/swarm_module_pattern.py

# For snippets with dependencies
pip install openai anthropic  # Install as needed
python snippet_name.py
```

## Core Architectural Patterns

### 1. Multi-Provider Abstraction (api-clients/)

**Key Insight:** Use abstract base classes with factory pattern to support multiple AI providers through one interface.

```python
from api_clients.multi_provider_abstraction import ProviderFactory

# Same code works with any provider
provider = ProviderFactory.create("openai", api_key="...")
response = provider.generate("prompt")
```

Implementations exist for OpenAI, Anthropic, xAI. All support streaming and non-streaming modes.

### 2. Swarm Module Pattern (tool-registration/)

**Key Insight:** Modules auto-register when imported but work standalone when run directly.

Each module exports:
- `TOOL_SCHEMAS` - OpenAI function calling format
- `TOOL_IMPLEMENTATIONS` - Dict mapping names to functions
- `handle_tool_calls()` - Standardized execution handler

```python
# Module works standalone
if __name__ == "__main__":
    cli_interface()

# Also auto-registers when imported
import swarm_module  # Automatically adds to global registry
```

### 3. Hierarchical Agent Orchestration (agent-orchestration/)

**Key Insight:** Multi-tier architecture automatically scales based on agent count.

**Scaling Rules:**
- 1-4 agents: Workers only (Belters)
- 5-9 agents: Workers + 1 Synthesizer (Drummer)
- 10+ agents: Workers + N Synthesizers + 1 Executive (Camina)

Synthesizer tier automatically adds 1 per 5 workers. Executive tier appears when 2+ synthesizers exist.

**Performance:**
- Sequential: ~60s for 10 agents
- Parallel (max_concurrent=5): ~12s
- Parallel (max_concurrent=10): ~6s

### 4. Configuration Precedence (configuration-management/)

**Hierarchy (highest to lowest):**
1. CLI arguments
2. Environment variables
3. Config files (.env, YAML, JSON)
4. Hardcoded defaults

```python
from configuration_management.multi_source_config import ConfigurationManager

config = ConfigurationManager("myapp")
config.load_all(cli_args={"debug": True})
api_key = config.require("api_key")  # Throws if missing
```

### 5. Graceful Degradation (error-handling/)

**Key Insight:** Feature flags + lazy imports + minimal fallbacks for optional dependencies.

```python
# Module loads even if dependencies missing
try:
    import optional_package
    HAS_FEATURE = True
except ImportError:
    HAS_FEATURE = False
    # Provide minimal fallback or clear error message
```

### 6. SSE Streaming (streaming-patterns/)

Complete Flask and FastAPI implementations for Server-Sent Events with:
- Real-time token streaming (ChatGPT-style)
- Progress indicators for long operations
- Proper connection management and error handling
- Client examples in Python and JavaScript

## Snippet Structure Standard

Every snippet follows this format:

```python
"""
[Title]

Description: [What and when to use]

Use Cases:
- [Specific scenario 1]
- [Specific scenario 2]

Dependencies:
- [Required packages]

Notes:
- [Important considerations]

Related Snippets:
- [Cross-references]

Source Attribution:
- Extracted from: [Original path]
"""

# Implementation

# Usage examples at bottom
if __name__ == "__main__":
    # Runnable examples
```

## Adding New Snippets

1. **Extract:** Copy from source project
2. **Generalize:** Remove project-specific details (API keys, hardcoded paths)
3. **Document:** Add comprehensive docstring following standard format
4. **Add Examples:** Include runnable usage examples at bottom
5. **Update README.md:** Add entry in appropriate category with description, use cases, dependencies
6. **Update EXTRACTION_SUMMARY.md:** Log extraction with source attribution

## Key Design Principles

1. **Self-contained:** Each snippet works independently
2. **Immediately usable:** Copy-paste-run without modification (except config)
3. **Production-ready:** Includes error handling, edge cases, type hints
4. **Well-documented:** Comprehensive docstrings + usage examples
5. **Source-attributed:** Always credit original project
6. **Cross-referenced:** Link related patterns

## Language-Specific Conventions

### Python (Primary)
- Files: `snake_case_pattern.py`
- Directories: `kebab-case/`
- Type hints on all public functions
- Docstrings follow snippet standard format

### JavaScript (Secondary)
- Files: `kebab-case-pattern.js`
- ES6+ syntax with clear comments
- Works in browsers without transpilation when possible

## Common Integration Patterns

### For AI/LLM Applications

```python
# 1. Configuration
from configuration_management.multi_source_config import ConfigurationManager
config = ConfigurationManager("myapp").load_all()

# 2. Provider abstraction
from api_clients.multi_provider_abstraction import ProviderFactory
provider = ProviderFactory.create("openai", api_key=config.get("api_key"))

# 3. Error handling
from error_handling.graceful_import_fallbacks import FeatureFlags
features = FeatureFlags()

# 4. Streaming responses (if web app)
from streaming_patterns.sse_streaming_responses import create_flask_sse_endpoint
```

### For Plugin Systems

```python
# 1. Module discovery
from file_operations.module_discovery import discover_modules
modules = discover_modules("./plugins/", pattern="plugin_*.py")

# 2. Tool registration (Swarm pattern)
# Import discovers and registers automatically
import plugin_module

# 3. Dynamic loading
from tool_registration.swarm_module_pattern import handle_tool_calls
result = handle_tool_calls(tool_name, arguments)
```

### For Multi-Agent Systems

```python
# 1. Agent data models
from agent_orchestration.multi_agent_data_models import AgentTask, AgentResult

# 2. Hierarchical coordination
from agent_orchestration.hierarchical_agent_coordination import HierarchicalOrchestrator

# 3. Parallel execution
from agent_orchestration.parallel_agent_execution import execute_agents_parallel
```

## Source Projects

Snippets extracted from:
- **Swarm:** `/home/coolhand/projects/swarm/` - Tool patterns, CLI
- **Beltalowda:** `/home/coolhand/html/belta/` - Agent orchestration
- **Enterprise Orchestration:** `/home/coolhand/enterprise_orchestration/` - Async patterns
- **API Projects:** `/home/coolhand/projects/apis/` - Multi-provider, streaming
- **Studio:** `/home/coolhand/servers/studio/` - Flask patterns, caching
- **COCA:** `/home/coolhand/servers/coca/` - WebSocket, real-time dashboards
- **Accessibility:** `/home/coolhand/html/accessibility/` - WCAG compliance
- **DataVis:** `/home/coolhand/html/datavis/` - D3.js, Chart.js, Leaflet

## Special Patterns

### Cost-Optimized Model Selection
Routes simple queries to cheap models (gpt-4o-mini, haiku), complex queries to flagship models (gpt-4o, sonnet). Can achieve 60-80% cost savings through heuristic analysis.

### Hybrid Free API Provider
Uses Claude Code API when available (free), falls back to paid API when standalone. Same code works in both contexts.

### Cache Manager with Redis Fallback
Automatically detects Redis availability and falls back to in-memory dict. Can achieve 40-100x cost savings on LLM calls through caching.

### Flask Blueprint with URL Prefix
Critical: When hosting under sub-paths, `SESSION_COOKIE_PATH` must match the blueprint prefix or auth breaks silently.

### AltFlow Alt Text Generation
Professional accessibility-focused alt text generation following WCAG standards. Strips social-emotional speculation, focuses on factual descriptions.

## File Organization

```
/home/coolhand/SNIPPETS/
├── README.md                    # Master index with all snippets
├── EXTRACTION_SUMMARY.md        # History of extractions
├── CLAUDE.md                    # This file
├── api-clients/                 # 8 patterns - Multi-provider abstractions
├── agent-orchestration/         # 6 patterns - Multi-agent coordination
├── async-patterns/              # 7 patterns - Concurrent operations
├── accessibility/               # 7 patterns - WCAG compliance
├── cli-tools/                   # Interactive CLI patterns
├── configuration-management/    # Multi-source config loading
├── data-processing/             # 5 patterns - Validation, transformation
├── data-visualization/          # 5 patterns - D3.js, Chart.js, Leaflet
├── database-patterns/           # SQLite patterns
├── error-handling/              # Graceful degradation
├── file-operations/             # 4 patterns - I/O, module discovery
├── process-management/          # Service manager patterns
├── real-time-dashboards/        # 3 patterns - SocketIO, broadcasting
├── sentiment-analysis/          # VADER sentiment
├── streaming-patterns/          # SSE streaming
├── testing/                     # Pytest patterns
├── tool-registration/           # Swarm module pattern
├── utilities/                   # 12 patterns - Retry, cache, rate limiting
├── web-frameworks/              # 12 patterns - Flask/FastAPI
└── websocket-patterns/          # 2 patterns - Client reconnection
```

## Maintenance

- **Weekly:** Scan active projects for new patterns
- **Monthly:** Extract 2-3 new snippets from pending categories
- **After major features:** Run snippet harvester agent on source projects
- **Quality standard:** Every snippet must be runnable, documented, and source-attributed
