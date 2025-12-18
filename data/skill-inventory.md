# Server Capabilities Inventory for Claude Code Skills

**Generated**: 2025-12-18
**Purpose**: Comprehensive inventory of tools, CLIs, libraries, and capabilities that could be exposed as Claude Code skills
**Author**: Luke Steuber

---

## Table of Contents

1. [MCP Server Tools](#1-mcp-server-tools)
2. [LLM Provider Tools](#2-llm-provider-tools)
3. [Data Source Tools](#3-data-source-tools)
4. [Orchestration Patterns](#4-orchestration-patterns)
5. [Custom CLIs](#5-custom-clis)
6. [Service Management](#6-service-management)
7. [System Utilities](#7-system-utilities)
8. [Python Libraries](#8-python-libraries)
9. [Development Tools](#9-development-tools)
10. [Deployment Workflows](#10-deployment-workflows)

---

## 1. MCP Server Tools

**Location**: `/home/coolhand/shared/mcp/`
**Server Port**: 5060
**Start Command**: `python /home/coolhand/shared/mcp/unified_server.py`

### Core MCP Tools

| Tool Name | What It Does | Invocation | Skill Use Case |
|-----------|--------------|------------|----------------|
| `dream_orchestrate_research` | Execute Dream Cascade hierarchical research workflow | MCP tool call | Multi-tier research agent system for comprehensive analysis |
| `dream_orchestrate_search` | Execute Dream Swarm multi-agent search | MCP tool call | Parallel search across multiple domains |
| `dreamwalker_status` | Check workflow status | MCP tool call | Monitor long-running agent workflows |
| `dreamwalker_cancel` | Cancel running workflow | MCP tool call | Abort in-progress orchestrations |
| `dreamwalker_patterns` | List available orchestrator patterns | MCP tool call | Discover orchestration capabilities |
| `dreamwalker_list_tools` | List registered tools | MCP tool call | Tool discovery and introspection |
| `dreamwalker_execute_tool` | Execute registered tool | MCP tool call | Dynamic tool execution |

**Skill Opportunity**: `@dreamwalker_research` - Launch multi-agent research with streaming progress

### MCP Resources

| Resource URI | What It Does | Skill Use Case |
|--------------|--------------|----------------|
| `orchestrator://{pattern}/info` | Get orchestrator metadata | Query available orchestration patterns |
| `orchestrator://{task_id}/status` | Get workflow status | Check progress of running tasks |
| `orchestrator://{task_id}/results` | Get workflow results | Retrieve completed research |

### Streaming Capabilities

- **SSE Endpoint**: `/stream/{task_id}`
- **Use Case**: Real-time progress updates for long-running workflows
- **Skill Integration**: Live progress bars, incremental results display

---

## 2. LLM Provider Tools

**Location**: `/home/coolhand/shared/llm_providers/`
**Factory**: `ProviderFactory`

### Supported Providers (12 total)

| Provider | Capabilities | Invocation | Skill Use Case |
|----------|--------------|------------|----------------|
| **OpenAI** | Chat, Vision, Image Gen (DALL-E), Embeddings | `ProviderFactory.get_provider('openai')` | GPT-4 chat, DALL-E 3 image generation |
| **Anthropic** | Chat, Vision | `ProviderFactory.get_provider('anthropic')` | Claude 3.5 Sonnet reasoning |
| **xAI** | Chat, Vision, Image Gen (Aurora) | `ProviderFactory.get_provider('xai')` | Grok-3 chat, Aurora image gen |
| **Mistral** | Chat, Vision (Pixtral), Embeddings | `ProviderFactory.get_provider('mistral')` | Pixtral vision analysis |
| **Cohere** | Chat, Embeddings | `ProviderFactory.get_provider('cohere')` | Semantic search, embeddings |
| **Gemini** | Chat, Vision, Embeddings | `ProviderFactory.get_provider('gemini')` | Google Gemini 2.0 Flash/Pro |
| **Perplexity** | Chat, Vision | `ProviderFactory.get_provider('perplexity')` | Sonar Pro search-augmented chat |
| **Groq** | Chat (fast inference) | `ProviderFactory.get_provider('groq')` | Ultra-fast chat completions |
| **HuggingFace** | Chat, Vision, Image Gen, Embeddings | `ProviderFactory.get_provider('huggingface')` | Stable Diffusion, various models |
| **Manus** | Chat, Vision (agent profiles) | `ProviderFactory.get_provider('manus')` | Specialized agent personas |
| **ElevenLabs** | Text-to-Speech | `ProviderFactory.get_provider('elevenlabs')` | High-quality voice synthesis |
| **Ollama** | Chat, Vision, Embeddings (local) | `ProviderFactory.get_provider('ollama')` | Local LLM inference (Llama, Llava) |

**Skill Opportunities**:
- `@llm_chat` - Multi-provider chat interface
- `@llm_vision` - Vision analysis across providers
- `@llm_image_gen` - Image generation (DALL-E, Aurora, Stable Diffusion)
- `@llm_embed` - Text embeddings for semantic search

### Complexity Router

**Location**: `/home/coolhand/shared/llm_providers/complexity_router.py`

Automatically selects provider based on task complexity:
- **Simple**: Groq (fast, cheap)
- **Medium**: xAI (balanced)
- **Complex**: Anthropic (best quality)

**Skill Use Case**: Cost-optimized LLM routing

---

## 3. Data Source Tools

**Location**: `/home/coolhand/shared/data_fetching/`
**Factory**: `ClientFactory`

### Available Data Clients (17 total)

| Client | What It Does | Invocation | Skill Use Case |
|--------|--------------|------------|----------------|
| **ArxivClient** | Search academic papers | `ClientFactory.create_client('arxiv')` | Research paper search |
| **SemanticScholarClient** | Research papers with citations | `ClientFactory.create_client('semantic_scholar')` | Citation analysis |
| **PubMedClient** | Medical/biomedical literature | `ClientFactory.create_client('pubmed')` | Medical research |
| **ArchiveClient** | Wayback Machine snapshots | `ClientFactory.create_client('archive')` | Historical web content |
| **MultiArchiveClient** | Multi-provider archives | Direct import | Archive.is, Memento, 12ft |
| **CensusClient** | US Census Bureau data | `ClientFactory.create_client('census')` | Demographic data |
| **FECClient** | Federal Election Commission | `ClientFactory.create_client('fec')` | Campaign finance |
| **JudiciaryClient** | Court records | `ClientFactory.create_client('judiciary')` | Legal data |
| **GitHubClient** | Repository/user data | `ClientFactory.create_client('github')` | Code search |
| **NASAClient** | Space imagery, data | `ClientFactory.create_client('nasa')` | APOD, Mars photos |
| **NewsClient** | News articles | `ClientFactory.create_client('news')` | Current events |
| **WikipediaClient** | Wikipedia articles | `ClientFactory.create_client('wikipedia')` | Encyclopedia lookup |
| **WeatherClient** | Weather forecasts | `ClientFactory.create_client('weather')` | Current weather |
| **OpenLibraryClient** | Book metadata | `ClientFactory.create_client('openlibrary')` | Book search |
| **YouTubeClient** | Video metadata | `ClientFactory.create_client('youtube')` | Video search |
| **FinanceClient** | Stock/financial data | `ClientFactory.create_client('finance')` | Alpha Vantage data |
| **MALClient** | Anime/manga data | `ClientFactory.create_client('mal')` | MyAnimeList |
| **WolframAlphaClient** | Computational queries | `ClientFactory.create_client('wolfram')` | Math, facts, conversions |

**Skill Opportunities**:
- `@research_papers` - Academic paper search (Arxiv, Semantic Scholar, PubMed)
- `@data_census` - Census demographic data
- `@data_weather` - Weather forecasts
- `@data_github` - Repository search
- `@data_nasa` - NASA imagery and data
- `@wolfram_query` - Computational knowledge

---

## 4. Orchestration Patterns

**Location**: `/home/coolhand/shared/orchestration/`

### Available Orchestrators

| Orchestrator | Pattern | Use Case | Invocation |
|--------------|---------|----------|------------|
| **DreamCascadeOrchestrator** | 3-tier hierarchical | Comprehensive research | `DreamCascadeOrchestrator(config, provider)` |
| **DreamSwarmOrchestrator** | Multi-domain parallel | Multi-source search | `DreamSwarmOrchestrator(config, provider)` |
| **SequentialOrchestrator** | Staged execution | Step-by-step workflows | `SequentialOrchestrator(stages, provider)` |
| **ConditionalOrchestrator** | Runtime branching | Decision-based workflows | `ConditionalOrchestrator(conditions, provider)` |
| **IterativeOrchestrator** | Looped refinement | Iterative improvement | `IterativeOrchestrator(config, provider)` |
| **AccessibilityOrchestrator** | A11y audits | Accessibility analysis | `AccessibilityOrchestrator(config, provider)` |

### Dream Cascade (3-tier)

**Tiers**:
1. **Belter** (Workers): Parallel research agents
2. **Drummer** (Mid-level): Synthesis agents
3. **Camina** (Executive): Final synthesis

**Configuration**:
```python
config = DreamCascadeConfig(
    num_agents=8,           # Belter count
    enable_drummer=True,    # Mid-level synthesis
    enable_camina=True,     # Executive synthesis
    generate_documents=True,
    document_formats=['markdown', 'pdf']
)
```

**Skill Use Case**: `@orchestrate_research` - Launch hierarchical research

### Dream Swarm (Multi-domain)

**Agent Types**: text, image, video, news, academic, social, product, technical, general

**Skill Use Case**: `@orchestrate_search` - Parallel multi-source search

---

## 5. Custom CLIs

**Location**: Various

### Todoist CLI

**Location**: `/home/coolhand/shared/cli/todoist/todoist_cli.py`
**Symlink**: `/home/coolhand/bin/todoist`

| Command | What It Does | Skill Use Case |
|---------|--------------|----------------|
| `todoist tasks` | List all tasks | Task management |
| `todoist add "Task"` | Add task | Create todos |
| `todoist complete <id>` | Mark complete | Update task status |
| `todoist projects` | List projects | Project listing |
| `todoist update <id>` | Update task | Modify tasks |

**Skill Opportunity**: `@todoist` - Todoist task management

### Service Manager CLI

**Location**: `/home/coolhand/service_manager.py`
**Alias**: `sm`

| Command | What It Does | Skill Use Case |
|---------|--------------|----------------|
| `sm status` | View all services | Service monitoring |
| `sm start <service>` | Start service | Service control |
| `sm stop <service>` | Stop service | Service management |
| `sm restart <service>` | Restart service | Service lifecycle |
| `sm logs <service>` | View logs | Debugging |

**Managed Services**:
- wordblocks (8847), lessonplanner (4108), clinical (1266), altproxy (1131)
- storyblocks (8000), dashboard (9999), goatcounter (6038)
- mcp-orchestrator (5060), swarm (5001), beltalowda (5009)

**Skill Opportunity**: `@service_manager` - Service lifecycle management

### Provider Ping CLI

**Location**: `/home/coolhand/shared/cli/ping_providers.py`

| Command | What It Does | Skill Use Case |
|---------|--------------|----------------|
| `ping_providers.py --all` | Test all providers | Health check |
| `ping_providers.py --provider xai` | Test specific provider | Connectivity test |
| `ping_providers.py --list` | List providers | Discovery |

**Skill Opportunity**: `@health_check_llm` - LLM provider health monitoring

### MCP Start Script

**Location**: `/home/coolhand/start-mcp-server`

Starts MCP server in STDIO mode for Claude Code integration.

**Skill Use Case**: Already integrated with Claude Code

---

## 6. Service Management

### Systemd Services

| Service | Port | What It Does | Control |
|---------|------|--------------|---------|
| `caddy.service` | 80, 443 | Web server/reverse proxy | `sudo systemctl restart caddy` |
| `coca-api.service` | 3034 | Corpus linguistics API | `sudo systemctl status coca-api` |
| `clinical.service` | 1266 | Clinical reference | `sudo systemctl restart clinical` |
| `litemarshal` | 5050 | Bluesky management | `sudo systemctl status litemarshal` |

**Skill Opportunity**: `@systemd` - Systemd service management (requires sudo)

### Service Manager Services

Managed by `/home/coolhand/service_manager.py`:
- All services listed in Section 5 above

**Skill Opportunity**: `@services` - Non-sudo service management

---

## 7. System Utilities

### Maintenance Scripts

**Location**: `/home/coolhand/scripts/`

| Script | What It Does | Skill Use Case |
|--------|--------------|----------------|
| `archive_maintenance.sh` | Archive lifecycle management | Backup automation |
| `safe_cleanup.sh` | Safe cleanup with guards | Disk space management |
| `backup_redundancy.sh` | Create redundant backups | Backup verification |
| `validate_claude_md.py` | Validate CLAUDE.md files | Documentation QA |
| `low-hanging-fruit-scanner.py` | Code quality scanner | Code improvement suggestions |
| `repectomy.py` | Repository cleanup | Repo hygiene |

**Skill Opportunities**:
- `@maintenance` - Run maintenance tasks
- `@validate_docs` - Check CLAUDE.md consistency
- `@code_quality` - Scan for improvements

### Development Tools

| Tool | Version | What It Does | Invocation |
|------|---------|--------------|------------|
| **pytest** | Latest | Test runner | `pytest` |
| **ruff** | Latest | Python linter | `ruff check .` |
| **black** | Latest | Code formatter | `black .` |
| **sqlite3** | System | Database CLI | `sqlite3 <db>` |
| **gh** | 2.74.2 | GitHub CLI | `gh repo list` |

**Skill Opportunities**:
- `@test` - Run tests
- `@lint` - Lint code
- `@format` - Format code
- `@gh` - GitHub operations

---

## 8. Python Libraries

**Location**: `/home/coolhand/shared/`

### Core Modules

| Module | Purpose | Key Classes | Import |
|--------|---------|-------------|--------|
| **llm_providers** | 12 AI provider adapters | `ProviderFactory`, `BaseLLMProvider` | `from llm_providers import ProviderFactory` |
| **orchestration** | Multi-agent workflows | `DreamCascadeOrchestrator` | `from orchestration import DreamCascadeOrchestrator` |
| **data_fetching** | 17 data source clients | `ClientFactory` | `from data_fetching import ClientFactory` |
| **mcp** | MCP server (port 5060) | `UnifiedMCPServer` | `from mcp import UnifiedMCPServer` |
| **document_generation** | PDF/DOCX/Markdown | `DocumentGenerator` | `from document_generation import DocumentGenerator` |
| **tools** | Tool registry | `ToolRegistry`, `ToolModuleBase` | `from tools import get_registry` |
| **utils** | Vision, embeddings, async | Various utilities | `from utils import vision, embeddings` |
| **observability** | Cost tracking, metrics | `CostTracker`, `MetricsCollector` | `from observability import CostTracker` |
| **config** | Configuration management | `ConfigManager` | `from config import ConfigManager` |

### Utils Submodules

| Utility | What It Does | Import |
|---------|--------------|--------|
| **vision.py** | Vision API wrappers | `from utils.vision import analyze_image` |
| **embeddings.py** | Text embeddings | `from utils.embeddings import get_embeddings` |
| **async_adapter.py** | Async helpers | `from utils.async_adapter import run_async` |
| **citation.py** | Citation management | `from utils.citation import format_citation` |
| **document_parsers.py** | PDF, DOCX, etc. parsing | `from utils.document_parsers import parse_pdf` |
| **format_converter.py** | Format conversion | `from utils.format_converter import md_to_pdf` |
| **rate_limiter.py** | API rate limiting | `from utils.rate_limiter import RateLimiter` |
| **retry_logic.py** | Retry with backoff | `from utils.retry_logic import retry` |
| **text_processing.py** | Text utilities | `from utils.text_processing import clean_text` |
| **multi_search.py** | Multi-source search | `from utils.multi_search import MultiSearch` |
| **tts.py** | Text-to-speech | `from utils.tts import synthesize_speech` |

**Skill Opportunities**:
- `@vision_analyze` - Vision API wrapper
- `@document_parse` - Parse PDF/DOCX
- `@format_convert` - Convert between formats
- `@rate_limit` - API rate limiting

---

## 9. Development Tools

### Testing Infrastructure

**Location**: `/home/coolhand/shared/tests/`

| Component | What It Does | Invocation |
|-----------|--------------|------------|
| **pytest** | Test runner | `pytest` |
| **Coverage** | Code coverage | `pytest --cov` |
| **Test markers** | Test categorization | `pytest -m unit` |
| **Fixtures** | Test setup | `@pytest.fixture` |

**Test Markers**:
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.api` - API tests
- `@pytest.mark.slow` - Slow tests

**Skill Opportunity**: `@test_suite` - Run categorized tests

### Code Quality

| Tool | Purpose | Command |
|------|---------|---------|
| **ruff** | Linting | `ruff check .` |
| **black** | Formatting | `black .` |
| **isort** | Import sorting | `isort .` |

**Skill Opportunity**: `@code_format` - Format and lint codebase

### GitHub CLI

**Version**: 2.74.2

| Command | What It Does | Skill Use Case |
|---------|--------------|----------------|
| `gh repo list` | List repositories | Repo discovery |
| `gh pr create` | Create pull request | PR automation |
| `gh issue list` | List issues | Issue tracking |
| `gh workflow run` | Trigger workflow | CI/CD automation |

**Skill Opportunity**: `@gh_ops` - GitHub operations

---

## 10. Deployment Workflows

### Caddy Configuration

**Config**: `/etc/caddy/Caddyfile`
**Control**: `sudo systemctl reload caddy`

**Routing Patterns**:
- `handle_path /prefix/*` - Strips prefix
- `handle /prefix/*` - Keeps prefix

**Managed Routes**:
- `/planner/*` → localhost:4108
- `/clinical/*` → localhost:1266
- `/alt/*` → localhost:1131
- `/skymarshal/*` → localhost:5050
- `/storyblocks/*` → localhost:8000
- And 20+ more routes

**Skill Opportunity**: `@caddy_config` - Manage reverse proxy routes (CRITICAL: Must use @geepers_caddy agent)

### Service Deployment Pattern

**Workflow**:
1. Update code
2. Run tests (`pytest`)
3. Lint/format (`ruff`, `black`)
4. Restart service (`sm restart <service>`)
5. Verify health endpoint
6. Update Caddy if routes changed
7. Git commit

**Skill Opportunity**: `@deploy` - End-to-end deployment workflow

### Port Allocation

**Available Ranges**:
- Development: 5010-5019
- Testing: 5050-5059

**Reserved Ports**:
- 5060: MCP server
- 5080: Dreamwalker UI
- 5001: Swarm
- 5009: Beltalowda

**Skill Opportunity**: `@port_check` - Verify port availability

---

## Summary: Top Skill Opportunities

Based on this inventory, here are the highest-value skills to expose:

### Tier 1: Core Capabilities

1. **@dreamwalker** - Multi-agent research orchestration
2. **@llm_multi** - Multi-provider LLM interface
3. **@data_fetch** - Multi-source data retrieval
4. **@service_manage** - Service lifecycle management

### Tier 2: Specialized Tools

5. **@research_academic** - Academic paper search (Arxiv, PubMed, Semantic Scholar)
6. **@vision_analyze** - Multi-provider vision analysis
7. **@document_convert** - Format conversion (PDF, DOCX, Markdown)
8. **@test_suite** - Categorized test execution

### Tier 3: Development Workflows

9. **@deploy_service** - End-to-end deployment
10. **@code_quality** - Lint, format, validate
11. **@gh_automation** - GitHub operations
12. **@health_monitor** - System health checks

### Tier 4: Specialized APIs

13. **@census_data** - US Census data queries
14. **@nasa_imagery** - NASA space imagery
15. **@wolfram_compute** - Computational knowledge
16. **@weather_forecast** - Weather data

---

## Integration Patterns

### 1. MCP Tool Exposure

```python
# Expose as MCP tool
{
  "name": "skill_name",
  "description": "What it does",
  "inputSchema": {
    "type": "object",
    "properties": {...}
  }
}
```

### 2. Direct Python Import

```python
import sys
sys.path.insert(0, '/home/coolhand/shared')
from llm_providers import ProviderFactory
from orchestration import DreamCascadeOrchestrator
```

### 3. CLI Wrapper

```bash
#!/bin/bash
python /home/coolhand/shared/cli/tool.py "$@"
```

### 4. Service Endpoint

```python
# Flask endpoint
@app.route('/api/skill', methods=['POST'])
def skill_endpoint():
    # Invoke capability
    return jsonify(result)
```

---

## Next Steps

1. **Prioritize Skills**: Determine which capabilities to expose first
2. **Design Skill Interface**: Define input/output schemas
3. **Implement Wrappers**: Create skill wrappers for each capability
4. **Test Integration**: Verify skills work with Claude Code
5. **Document Skills**: Create usage docs for each skill
6. **Monitor Usage**: Track which skills are most valuable

---

**Inventory Complete**: 100+ tools, 12 LLM providers, 17 data sources, 6 orchestrators, 30+ utilities cataloged

**Author**: Luke Steuber
**Date**: 2025-12-18
