# Code Snippets Library

A comprehensive, well-organized collection of reusable code patterns, API integrations, and solved problems extracted from the AI development ecosystem. These snippets accelerate development by providing battle-tested, production-ready patterns.

**Last Updated:** 2025-12-15
**Total Snippets:** 66+
**Languages:** Python, JavaScript, Markdown (documentation)
**Focus:** AI/LLM Integration, MCP Protocol, Tool Development, API Patterns, Agent Orchestration, Workflow Orchestration, Data Visualization, Data Processing, Async/Concurrent Operations, Real-Time Dashboards, WebSocket Streaming, Sentiment Analysis, Vision AI, Document Parsing, Embeddings, Timezone Handling, Audio/Video Processing, Cache Management, Flask Blueprints, Accessibility, Cost Optimization, Model Selection, Markdown Parsing, Claude Code Integration, Social Media APIs, Academic Tools, File Deduplication, News Aggregation, Web Scraping, Location Services, LangGraph Agents, Cryptography, Academic Research APIs, Vision API Client

---

## Table of Contents

- [Quick Start](#quick-start)
- [Snippet Categories](#snippet-categories)
- [Usage Guidelines](#usage-guidelines)
- [Contributing](#contributing)
- [Source Attribution](#source-attribution)

---

## Quick Start

### Installation

Most snippets are self-contained Python files. Copy the snippet you need and adjust imports/configuration as needed.

```bash
# Example: Using the multi-provider abstraction
cp ~/SNIPPETS/api-clients/multi_provider_abstraction.py myproject/
cd myproject/
pip install openai  # Install required dependencies
python multi_provider_abstraction.py  # See usage example
```

### Common Dependencies

```bash
# Core dependencies for most snippets
pip install openai anthropic requests pyyaml python-dotenv

# Optional enhanced features
pip install rich pytest pytest-asyncio

# For web framework patterns
pip install fastapi flask uvicorn
```

---

## Snippet Categories

### API Clients

**Location:** `/home/coolhand/SNIPPETS/api-clients/`

Multi-provider API abstractions for building provider-agnostic applications.

#### `multi_provider_abstraction.py`
- **Description:** Comprehensive pattern for creating unified interfaces across multiple AI providers (OpenAI, Anthropic, xAI, etc.)
- **Use Cases:**
  - Building multi-LLM applications
  - Implementing fallback mechanisms
  - A/B testing different providers
  - Switching providers without code changes
- **Key Features:**
  - Abstract base class pattern
  - Provider factory for instantiation
  - Streaming and non-streaming support
  - Standardized error handling
- **Dependencies:** `openai`, `typing`, `logging`
- **Source:** `/home/coolhand/projects/apis/api_v2/providers/`

#### `base_provider_pattern.py` *(existing)*
- **Description:** Base provider pattern with image processing capabilities
- **Source:** Previously extracted

#### `xai_vision_api_integration.py`
- **Description:** Complete pattern for integrating xAI's Grok Vision API for image/video analysis with base64 encoding and video frame extraction
- **Use Cases:**
  - AI-powered image analysis and description generation
  - Video frame extraction and analysis
  - Alt-text generation for accessibility
  - Filename suggestion from visual content
  - Multi-modal AI applications with vision
- **Key Features:**
  - Works with any OpenAI-compatible vision API (xAI, OpenAI, Azure)
  - Supports both image and video analysis
  - Graceful fallback when optional dependencies unavailable
  - Base64 encoding for API submission
  - Proper MIME type detection
  - Environment variable support for API keys
- **Dependencies:** `openai`, optional: `PIL/Pillow`, `opencv-python`
- **Source:** `/home/coolhand/shared/utils/vision.py`

#### `provider_adapter_pattern.py` ⭐ NEW
- **Description:** Adapter pattern for wrapping shared library providers with application-specific functionality
- **Use Cases:**
  - Adding conversation history to stateless LLM APIs
  - Wrapping shared library providers with app-specific methods
  - Standardizing interfaces across different providers
  - Adding local functionality (encoding, validation) to remote services
- **Key Features:**
  - Base adapter class with common methods
  - Provider-specific adapters (Anthropic, OpenAI, xAI, etc.)
  - Conversation history management
  - Factory pattern for graceful initialization
  - Image encoding utilities
  - Delegation to shared library for core functionality
- **Dependencies:** `typing`, shared library providers
- **Source:** `/home/coolhand/servers/studio/providers/studio_adapters.py`

#### `cost_optimized_model_selection.py` ⭐ NEW
- **Description:** Intelligent model selection based on query complexity analysis for cost optimization (60-80% savings)
- **Use Cases:**
  - Cost optimization for high-volume chatbot services
  - API budget management across query types
  - Balancing quality vs. cost in multi-tenant applications
  - Dynamic model routing based on query characteristics
  - A/B testing different model tiers
- **Key Features:**
  - Pattern-based heuristic analysis (no ML required)
  - Routes simple queries to cheaper models (gpt-4o-mini, haiku)
  - Routes complex queries to flagship models (gpt-4o, sonnet)
  - Supports all major LLM providers with tier definitions
  - Extensible indicator patterns for domain-specific tuning
  - Override complexity for manual control
- **Dependencies:** `re`, `typing`
- **Source:** `/home/coolhand/shared/llm_providers/factory.py` (impossibleLlama Coze agent pattern)

#### `lazy_loading_provider_factory.py` ⭐ NEW
- **Description:** Singleton factory for LLM providers with lazy initialization and caching
- **Use Cases:**
  - Multi-provider applications that don't use all providers simultaneously
  - Systems with optional provider support (install only what you need)
  - Testing environments where some providers may not be configured
  - Dynamic provider switching based on availability
  - Memory-constrained environments
- **Key Features:**
  - Providers loaded on-demand (first access)
  - Singleton instances cached after creation
  - Graceful handling of missing optional providers
  - Thread-safe singleton implementation
  - Clear cache for testing/reinitialization
  - Provider availability checking
- **Dependencies:** `typing`
- **Source:** `/home/coolhand/shared/llm_providers/factory.py`

#### `hybrid_free_api_provider.py` ⭐ NEW
- **Description:** Hybrid provider pattern that uses free service when available (Claude Code), falls back to paid API
- **Use Cases:**
  - Development tools that work both locally and in Claude Code
  - Cost-free prototyping in supported environments
  - Educational projects with API key fallback
  - Testing workflows that auto-switch contexts
  - Multi-environment orchestrators
- **Key Features:**
  - Zero API costs when running in Claude Code
  - Transparent fallback to API when standalone
  - Same code works in both contexts
  - Environment variable detection
  - Can extend to other hybrid contexts (VS Code, Cursor)
- **Dependencies:** `os`, `typing`
- **Source:** `/home/coolhand/shared/llm_providers/claude_code_provider.py`

#### `wolfram_alpha_client.py` ⭐ NEW
- **Description:** Wolfram Alpha computational knowledge engine client with JSON/XML parsing and multiple output formats
- **Use Cases:**
  - Mathematical calculations and symbolic computation
  - Scientific data queries (physics, chemistry, astronomy)
  - Unit conversions and comparisons
  - Knowledge base lookups for AI agents
  - Educational tools requiring computational answers
- **Key Features:**
  - Both JSON and XML API support
  - Multiple output formats (plaintext, image, mathml)
  - Pod-based result structure with subpods
  - Structured response parsing
  - Convenience functions for common operations
- **Dependencies:** `requests`
- **Source:** `/home/coolhand/inbox/apis/llamni/utils/wolfram_alpha.py`

#### `location_services_client.py` ⭐ NEW
- **Description:** Unified client for location-based APIs including geocoding (MapQuest), walkability scores (WalkScore), and air quality data (WAQI)
- **Use Cases:**
  - Property evaluation and real estate tools
  - Location-based recommendations
  - Environmental monitoring dashboards
  - Address geocoding and coordinate lookup
  - Urban planning and livability analysis
- **Key Features:**
  - MapQuest geocoding (address to coordinates)
  - WalkScore/Transit Score/Bike Score integration
  - Air Quality Index with pollutant breakdown
  - Unified `LocationServices` class for complete analysis
  - Interpretation helpers for AQI and Walk Score values
- **Dependencies:** `requests`
- **Source:** `/home/coolhand/inbox/apis/api-schema/tools/property/`

#### `jina_web_scraper.py` ⭐ NEW
- **Description:** Web scraping client using Jina Reader API (r.jina.ai) to extract clean, markdown-formatted text content from web pages
- **Use Cases:**
  - Web content extraction for RAG pipelines
  - Clean text extraction for LLM context
  - Research and data gathering automation
  - Content archiving and analysis
  - Bypassing JavaScript-rendered pages
- **Key Features:**
  - Converts web pages to clean markdown
  - Removes ads, navigation, and boilerplate
  - Handles JavaScript-rendered pages
  - Optional image alt-text generation
  - URL cleaning to reduce token count
  - Configurable caching control
- **Dependencies:** `requests`
- **Source:** `/home/coolhand/inbox/scratchpad/tools_collection/chat_apis/`

#### `bbc_news_client.py` ⭐ NEW
- **Description:** BBC News RSS feed client with support for multiple categories and full article content extraction
- **Use Cases:**
  - News aggregation and monitoring
  - Current events tracking for AI agents
  - Research and content gathering
  - Building news digest applications
  - Media monitoring systems
- **Key Features:**
  - 20+ news categories (world, tech, business, etc.)
  - Structured data with title, description, link, date
  - Media thumbnail extraction
  - Full article content extraction (with BeautifulSoup)
  - LLM-friendly formatting helper
- **Dependencies:** `requests`, optional: `beautifulsoup4`
- **Source:** `/home/coolhand/inbox/scratchpad/to_strip/bbc_news.py`

#### `arxiv_client.py` ⭐ NEW
- **Description:** Client for searching and retrieving academic papers from arXiv.org with dataclass-based paper representation
- **Use Cases:**
  - Academic research paper discovery
  - Literature review automation
  - Citation and reference gathering
  - Research trend analysis
  - AI agent knowledge base enrichment
- **Key Features:**
  - Search by query, author, or category
  - Structured ArxivPaper dataclass with all metadata
  - Batch paper retrieval by IDs
  - Paper formatting for display
  - LLM-friendly output helpers
- **Dependencies:** `arxiv`
- **Source:** `/home/coolhand/shared/data_fetching/arxiv_client.py`

#### `wikipedia_client.py` ⭐ NEW
- **Description:** Wikipedia API client supporting article search, summaries, full content, and random articles across 300+ languages
- **Use Cases:**
  - Knowledge base enrichment for AI agents
  - Reference and fact-checking tools
  - Multilingual content retrieval
  - Educational applications
  - Building encyclopedic search features
- **Key Features:**
  - Multi-language support (en, es, fr, de, ja, etc.)
  - Article search with descriptions
  - Summary and full content retrieval
  - Random article fetching
  - Categories and internal links extraction
- **Dependencies:** `requests`
- **Source:** `/home/coolhand/shared/data_fetching/wikipedia_client.py`

---

### Social Media Clients

**Location:** `/home/coolhand/SNIPPETS/social-media-clients/`

Clients for social media platform APIs with authentication, caching, and rate limiting.

#### `bluesky_at_protocol_client.py` ⭐ NEW
- **Description:** Complete Bluesky AT Protocol client with authentication, following/followers management, profile batch fetching, SQLite caching, and rate limiting
- **Use Cases:**
  - Building Bluesky bots and automation tools
  - Social network analysis on AT Protocol
  - Follower/following relationship tracking
  - Profile data collection and caching
  - Rate-limited bulk operations on Bluesky
- **Key Features:**
  - JWT authentication with automatic refresh
  - Paginated cursor-based following/followers fetch
  - Batch profile fetching (up to 25 at once)
  - SQLite-based caching layer with TTL
  - Rate limiting with configurable delays
  - Comprehensive error handling and retry logic
  - Async and sync interfaces
- **Dependencies:** `requests`, `sqlite3`
- **Source:** `/home/coolhand/inbox/bluesky-cli/`

---

### Academic Tools

**Location:** `/home/coolhand/SNIPPETS/academic-tools/`

Tools for academic research, citation management, and scholarly document processing.

#### `citation_parser.py` ⭐ NEW
- **Description:** Multi-style academic citation extractor supporting APA, MLA, Chicago, Harvard, and IEEE formats with BibTeX generation
- **Use Cases:**
  - Extracting citations from research papers
  - Building bibliography management tools
  - Citation style conversion and validation
  - Academic writing assistants
  - Document analysis for plagiarism detection
- **Key Features:**
  - Regex patterns for 5 major citation styles
  - Extracts both in-text citations and references
  - BibTeX entry generation from parsed data
  - Confidence scoring for citation matches
  - Handles DOI extraction and validation
  - Batch processing with statistics
- **Dependencies:** `re`, `typing`
- **Source:** `/home/coolhand/inbox/apis/llamni/utils/citations.py`

---

### Deduplication

**Location:** `/home/coolhand/SNIPPETS/deduplication/`

File and content deduplication patterns for managing duplicate data across projects.

#### `file_deduplication.py` ⭐ NEW
- **Description:** Comprehensive file deduplication framework with SHA-256 hashing, image-aware comparison, and text similarity analysis
- **Use Cases:**
  - Project cleanup and disk space recovery
  - Photo library deduplication
  - Source code duplicate detection
  - Backup optimization
  - Content management system cleanup
- **Key Features:**
  - SHA-256 hash-based exact duplicate detection
  - Image comparison using size + resolution (not just hash)
  - Text similarity analysis with weighted scoring (50% lines, 30% paragraphs, 20% words)
  - Configurable similarity thresholds
  - Directory scanning with file type filtering
  - Dry-run mode with detailed reports
  - Smart handling of renamed duplicates
- **Dependencies:** `hashlib`, `difflib`, `pathlib`
- **Source:** `/home/coolhand/inbox/cleanupx/cleanupx_core/processors/legacy/deduper.py`

---

### Tool Registration

**Location:** `/home/coolhand/SNIPPETS/tool-registration/`

Patterns for creating dynamically discoverable and registerable tool modules.

#### `swarm_module_pattern.py`
- **Description:** Complete pattern for building swarm-style tool modules with auto-discovery
- **Use Cases:**
  - Building plugin architectures for AI agents
  - Creating modular tool systems for LLMs
  - Implementing auto-discovery of capabilities
  - Organizing tools by functional domain
- **Key Features:**
  - Works standalone and when imported
  - OpenAI function calling schema format
  - Automatic tool registration
  - Comprehensive error handling
  - CLI with interactive testing mode
- **Dependencies:** `json`, `argparse`, `typing`
- **Source:** `/home/coolhand/projects/swarm/hive/swarm_template.py`

#### `mcp_stdio_server_pattern.py` ⭐ NEW
- **Description:** Complete implementation pattern for MCP (Model Context Protocol) stdio servers with JSON-RPC protocol handling
- **Use Cases:**
  - Exposing custom tools to Claude Code marketplace
  - Creating orchestration systems accessible via MCP
  - Building tool servers for Claude Code integration
  - Wrapping existing Python functionality as MCP tools
- **Key Features:**
  - Full MCP protocol 2024-11-05 implementation
  - JSON-RPC 2.0 request/response handling
  - Initialization handshake and capability negotiation
  - Async tool execution support
  - Structured error responses with standard codes
  - Logging to stderr (stdout reserved for protocol)
- **Dependencies:** `asyncio`, `json`, `logging`, `sys`
- **Source:** `/home/coolhand/geepers-orchestrators/mcp/stdio_servers/checkpoint_stdio.py`

---

### Streaming Patterns

**Location:** `/home/coolhand/SNIPPETS/streaming-patterns/`

Server-Sent Events (SSE) and streaming response patterns for real-time applications.

#### `sse_streaming_responses.py`
- **Description:** Comprehensive SSE streaming implementation for Flask and FastAPI
- **Use Cases:**
  - Real-time AI response streaming (ChatGPT-style)
  - Live data updates (stocks, notifications, logs)
  - Progress indicators for long operations
  - Multimodal content streaming
- **Key Features:**
  - Both Flask and FastAPI implementations
  - Client-side consumption examples (Python & JavaScript)
  - Proper connection management
  - Error handling and graceful degradation
  - Progress tracking for large operations
- **Dependencies:** `flask` or `fastapi`, `requests`
- **Source:** `/home/coolhand/projects/apis/api_v2/`, `/home/coolhand/projects/xai_swarm/`

---

### Error Handling

**Location:** `/home/coolhand/SNIPPETS/error-handling/`

Robust error handling patterns including import fallbacks and graceful degradation.

#### `graceful_import_fallbacks.py`
- **Description:** Pattern for handling optional dependencies with graceful degradation
- **Use Cases:**
  - Building modules that work with/without optional deps
  - Creating standalone tools
  - Cross-environment compatibility
  - Development vs. production dependencies
- **Key Features:**
  - Feature flags for tracking availability
  - Lazy import proxies
  - Minimal fallback implementations
  - Clear installation instructions in errors
  - Python version compatibility handling
- **Dependencies:** Core Python only (with optional enhancements)
- **Source:** `/home/coolhand/projects/swarm/hive/` modules

---

### Configuration Management

**Location:** `/home/coolhand/SNIPPETS/configuration-management/`

Multi-source configuration loading with proper precedence handling.

#### `multi_source_config.py`
- **Description:** Comprehensive configuration management from multiple sources
- **Use Cases:**
  - 12-factor compliant applications
  - Multiple deployment environments
  - Secure API key management
  - Hierarchical configuration (system → user → project)
- **Key Features:**
  - Configuration precedence: CLI → ENV → Config Files → Defaults
  - Support for .env, YAML, JSON, key=value formats
  - Environment variable parsing (bool, int, float)
  - Configuration validation
  - Source tracking for debugging
- **Dependencies:** `pathlib`, `json`, optional: `python-dotenv`, `pyyaml`
- **Source:** `/home/coolhand/projects/swarm/core/core_cli.py`

---

### CLI Tools

**Location:** `/home/coolhand/SNIPPETS/cli-tools/`

Interactive command-line interface patterns with LLM integration.

#### `interactive_cli_with_llm.py`
- **Description:** Full-featured interactive CLI for LLM chat with tool calling
- **Use Cases:**
  - Building ChatGPT-style CLI applications
  - Creating AI-powered terminal tools
  - Implementing REPL interfaces
  - Testing LLM integrations
- **Key Features:**
  - Streaming response support
  - Conversation history management
  - Tool/function calling integration
  - Special commands (/help, /clear, /history)
  - Signal handling (Ctrl+C, Ctrl+D)
  - Readline integration for command history
- **Dependencies:** `openai`, `readline`, `json`
- **Source:** `/home/coolhand/projects/swarm/hive/swarm_template.py`, `/home/coolhand/projects/WORKING/xai_tools.py`

---

### Testing

**Location:** `/home/coolhand/SNIPPETS/testing/`

Pytest patterns including fixtures, mocking, and test organization.

#### `pytest_fixtures_patterns.py`
- **Description:** Comprehensive pytest testing patterns and fixtures
- **Use Cases:**
  - Setting up test environments
  - Mocking external dependencies (APIs, databases)
  - Parametrized testing for multiple scenarios
  - Async test support
  - Test data management
- **Key Features:**
  - Scoped fixtures (function, class, module, session)
  - Mock API clients (OpenAI, Anthropic, xAI)
  - Parametrization examples
  - Async test patterns
  - conftest.py and pytest.ini examples
  - Integration test organization
- **Dependencies:** `pytest`, `pytest-asyncio`, `pytest-mock`, `pytest-cov`
- **Source:** `/home/coolhand/projects/tests/conftest.py`

---

### Agent Orchestration

**Location:** `/home/coolhand/SNIPPETS/agent-orchestration/`

Hierarchical agent coordination patterns for complex AI workflows extracted from the Beltalowda multi-agent platform.

#### `hierarchical_agent_coordination.py`
- **Description:** Three-tier hierarchical agent architecture (Belter → Drummer → Camina) for coordinating multi-agent swarms with parallel execution and synthesis layers
- **Use Cases:**
  - Large-scale research requiring multiple perspectives
  - Complex analysis benefiting from parallel investigation
  - Tasks needing hierarchical aggregation of insights
  - Executive-level strategic planning with comprehensive research
- **Key Features:**
  - Automatic scaling of synthesis layers based on agent count
  - Belter agents (workers) execute in parallel with rate limiting
  - Drummer agents (synthesizers) aggregate every 5 Belter responses
  - Camina agent (executive) provides final synthesis when 2+ Drummers exist
  - Progressive temperature reduction for consistency
  - Timeout handling and retry logic for failed agents
- **Dependencies:** `asyncio`, `pydantic`, `typing`, `enum`, `dataclasses`
- **Source:** `/home/coolhand/projects/beltalowda/src/beltalowda/orchestrator.py`

#### `parallel_agent_execution.py`
- **Description:** Pattern for executing multiple async agents in parallel with semaphore-based rate limiting, timeout handling, and retry logic
- **Use Cases:**
  - Executing multiple LLM API calls without exceeding rate limits
  - Coordinating parallel research tasks across specialized agents
  - Managing concurrent database or external API operations
  - Load balancing across multiple service instances
- **Key Features:**
  - Semaphore-based concurrency control
  - Individual timeout handling per agent
  - Return exceptions pattern for partial failures
  - Automatic retry logic for transient failures
  - Progress callbacks for real-time UI updates
- **Dependencies:** `asyncio`, `typing`, `dataclasses`, `enum`
- **Source:** `/home/coolhand/projects/beltalowda/src/beltalowda/orchestrator.py`

#### `task_decomposition_pattern.py`
- **Description:** Pattern for breaking down complex tasks into specific, actionable subtasks using LLM-based decomposition with intelligent padding and validation
- **Use Cases:**
  - Breaking complex research questions into focused sub-questions
  - Decomposing software projects into implementable features
  - Splitting analysis tasks across specialized domains
  - Converting high-level goals into actionable work items
- **Key Features:**
  - Generates 3-15 subtasks based on complexity
  - Automatic padding to match available agent count
  - Validates subtask quality and specificity
  - Domain-specific decomposition strategies
  - Template-based fallback if LLM decomposition fails
- **Dependencies:** `typing`, `dataclasses`, `datetime`, `re`
- **Source:** `/home/coolhand/projects/beltalowda/src/beltalowda/orchestrator.py`

#### `agent_lifecycle_management.py`
- **Description:** Comprehensive pattern for managing agent lifecycle from initialization through execution to cleanup, with state tracking and metrics
- **Use Cases:**
  - Managing agent pools in orchestration systems
  - Tracking agent status and health across distributed systems
  - Resource management and cleanup for long-running agents
  - Cost tracking and budget management for LLM-based agents
  - Debugging and monitoring agent behavior
- **Key Features:**
  - State transitions: PENDING → RUNNING → COMPLETED/FAILED
  - Validation ensures proper configuration before execution
  - Metadata tracking for debugging and analysis
  - Cost estimation for budget management
  - AgentPoolManager for centralized lifecycle control
- **Dependencies:** `abc`, `typing`, `enum`, `pydantic`, `datetime`
- **Source:** `/home/coolhand/projects/beltalowda/src/beltalowda/agents/base.py`

#### `provider_abstraction_pattern.py`
- **Description:** Abstract base class pattern for unified LLM provider interface enabling agents to work with any provider (OpenAI, Anthropic, Gemini, etc.)
- **Use Cases:**
  - Building provider-agnostic multi-agent systems
  - Implementing fallback mechanisms across different LLM providers
  - A/B testing different providers in agent swarms
  - Cost optimization by routing to cheaper providers
  - Supporting multiple LLM vendors in enterprise systems
- **Key Features:**
  - Uniform interface across all providers
  - Supports both streaming and non-streaming responses
  - Cost estimation for budget management
  - API key validation before use
  - Model capability detection for smart routing
- **Dependencies:** `abc`, `typing`, `pydantic`, `enum`, `asyncio`
- **Source:** `/home/coolhand/projects/beltalowda/src/beltalowda/providers/base.py`

#### `multi_agent_data_models.py` ⭐ NEW
- **Description:** Structured data classes for multi-agent workflows with type-safe containers for tasks, results, synthesis, and streaming
- **Use Cases:**
  - Multi-agent research workflows (Beltalowda pattern)
  - Specialized agent swarms (Swarm pattern)
  - Hierarchical task decomposition systems
  - Real-time orchestration dashboards
  - Cost tracking across agent executions
  - Citation and provenance tracking
- **Key Features:**
  - JSON-serializable via to_dict() methods

#### `phased_workflow_orchestrator.py` ⭐ NEW
- **Description:** Abstract base class for orchestrating multi-phase workflows with sequential and parallel execution, phase-level error handling, and automatic report generation
- **Use Cases:**
  - Multi-step data pipelines with dependencies
  - Code analysis workflows (scan → fix → test → report)
  - Deployment orchestration (validate → build → deploy → verify)
  - Research workflows with defined methodology phases
  - Any workflow where phase ordering is critical
- **Key Features:**
  - Explicit workflow phases defined declaratively
  - Context flows from phase to phase
  - Failed phases can stop or continue workflow
  - Automatic tracking of duration and artifacts
  - Reports generated to date-organized directories
  - Different from hierarchical pattern (deterministic vs. automatic scaling)
- **Dependencies:** `asyncio`, `dataclasses`, `datetime`, `pathlib`, `typing`, `json`, `abc`
- **Source:** `/home/coolhand/geepers-orchestrators/orchestrators/base_geepers.py`

#### `task_tool_dispatch_pattern.py` ⭐ NEW
- **Description:** Pattern for MCP servers to dispatch work to Claude Code's Task tool via structured instructions (bridges MCP protocol with Task tool)
- **Use Cases:**
  - MCP servers that need to delegate work to specialized agents
  - Orchestrators coordinating multiple Claude Code subagents
  - Building multi-step workflows where each step is a Task
  - Creating dispatch systems for agent routing
- **Key Features:**
  - Returns instructions instead of direct execution
  - Claude Code reads response and calls Task itself
  - Supports sequential and parallel execution plans
  - Includes prompt templates for common agent types
  - Maps agent names to Task subagent_type values
  - Complete workflow dispatch planning
- **Dependencies:** `dataclasses`, `enum`, `typing`, `datetime`, `pathlib`
- **Source:** `/home/coolhand/geepers-orchestrators/orchestrators/agent_dispatch.py`
  - Supports dependency tracking between subtasks
  - Extensible metadata fields for custom orchestrators
  - Built-in progress tracking for streaming UIs
  - Status enums (PENDING, RUNNING, COMPLETED, FAILED)
  - Agent type enums (WORKER, SYNTHESIZER, EXECUTIVE, MONITOR, SPECIALIZED)
  - Stream events for real-time UI updates
- **Dependencies:** `dataclasses`, `typing`, `datetime`, `enum`
- **Source:** `/home/coolhand/shared/orchestration/models.py`

---

### LangGraph Patterns

**Location:** `/home/coolhand/SNIPPETS/langgraph-patterns/`

Production-ready LangGraph patterns for building autonomous AI agents with reasoning, tool use, and configurable workflows.

#### `react_agent_pattern.py` ⭐ NEW
- **Description:** Complete ReAct (Reasoning and Acting) agent implementation using LangGraph with configurable LLM, tool binding, conditional routing, and state management
- **Use Cases:**
  - Building autonomous AI agents with tool use
  - Research assistants that search and synthesize
  - Task automation with multi-step reasoning
  - Chatbots with external data access
  - Question-answering systems with web search
- **Key Features:**
  - StateGraph with InputState/State dataclass pattern
  - Conditional routing based on tool calls
  - Multi-provider support (Anthropic, OpenAI, Google, Mistral, Cohere)
  - Runtime configuration via config dict
  - IsLastStep safety mechanism for recursion limits
  - ToolNode for automatic tool execution
  - System prompt templating with timestamps
- **Dependencies:** `langgraph`, `langchain-core`, `langchain-anthropic` (or other provider)
- **Source:** `/home/coolhand/inbox/hive/src/react_agent/`

---

### Async Patterns

**Location:** `/home/coolhand/SNIPPETS/async-patterns/`

Async/await patterns, concurrent operations, and async context managers for building scalable async applications.

#### `threadpool_concurrent_execution.py`
- **Description:** Production-ready pattern for executing multiple tasks concurrently using ThreadPoolExecutor with proper error handling and result aggregation
- **Use Cases:**
  - Multi-query research orchestration (generate N queries, execute in parallel, synthesize)
  - Concurrent API calls to multiple providers
  - Batch processing with I/O-bound operations
  - Parallel web scraping or data collection
  - Multi-search workflows (map-reduce pattern)
- **Key Features:**
  - Callback system for progress tracking
  - Result ordering preservation despite concurrent execution
  - Configurable worker count for rate limiting
  - Proper exception handling per task
  - Parallel map and filter helper functions
  - Best for I/O-bound operations
- **Dependencies:** `concurrent.futures`, `typing`, `dataclasses`
- **Source:** `/home/coolhand/shared/utils/multi_search.py`

#### `async_llm_operations.py`
- **Description:** Comprehensive patterns for async LLM operations with concurrency control
- **Use Cases:**
  - Processing multiple LLM requests concurrently
  - Batch operations with rate limiting
  - Async streaming responses
  - Implementing retry logic with exponential backoff
  - Managing API rate limits across concurrent operations
- **Key Features:**
  - Basic async LLM call pattern
  - Concurrent batch processing with semaphores
  - Retry with exponential backoff
  - Streaming async generators
  - Token bucket rate limiter
  - Worker pool pattern for task processing
- **Dependencies:** `asyncio`, `aiohttp`, `openai`, `typing`
- **Source:** `/home/coolhand/enterprise_orchestration/agents/`

#### `parallel_task_execution.py`
- **Description:** Patterns for executing multiple async tasks concurrently with proper error handling and progress tracking
- **Use Cases:**
  - Multi-agent AI workflows with parallel processing
  - Batch processing with concurrent workers
  - Coordinating multiple API calls in parallel
  - Swarm-based task decomposition and execution
  - Real-time progress tracking for long-running operations
- **Key Features:**
  - Parallel execution with asyncio.gather
  - Progress callbacks and streaming updates
  - Task result aggregation and statistics
  - Batched execution for rate limiting
  - Partial failure handling
  - Success rate calculation
- **Dependencies:** `asyncio`, `typing`, `dataclasses`
- **Source:** `/home/coolhand/enterprise_orchestration/core/coordinator.py`, `/home/coolhand/html/beltalowda/task-swarm/src/beltalowda/orchestrator.py`

#### `async_context_managers.py`
- **Description:** Comprehensive patterns for implementing async context managers for resource management
- **Use Cases:**
  - Managing async API client connections and cleanup
  - Database connection pooling with async context
  - Async file operations with proper resource cleanup
  - Module lifecycle management (setup/teardown)
  - Distributed lock acquisition and release
  - Streaming resource management
- **Key Features:**
  - Basic async context manager pattern (__aenter__/__aexit__)
  - API client with connection lifecycle
  - Module lifecycle base class
  - Async lock with timeout
  - Decorator-based context managers (@asynccontextmanager)
  - Temporary configuration overrides
- **Dependencies:** `asyncio`, `typing`, `abc`, `contextlib`
- **Source:** `/home/coolhand/enterprise_orchestration/core/base.py`

#### `task_cancellation_timeout.py`
- **Description:** Patterns for handling async task cancellation, timeouts, and graceful shutdown
- **Use Cases:**
  - Implementing request timeouts in web applications
  - Graceful shutdown of long-running services
  - Cancelling stale or slow operations
  - Cleanup of resources when tasks are cancelled
  - Implementing circuit breakers and fallbacks
  - Coordinating shutdown across multiple async tasks
- **Key Features:**
  - Basic timeout patterns with fallbacks
  - Cancellable task manager with tracking
  - Graceful shutdown with signal handling
  - Shielded operations for critical tasks
  - Timeout context manager
  - Task age-based cleanup
- **Dependencies:** `asyncio`, `typing`, `signal`
- **Source:** `/home/coolhand/enterprise_orchestration/core/base.py`, `/home/coolhand/enterprise_orchestration/core/coordinator.py`

---

### Web Frameworks

**Location:** `/home/coolhand/SNIPPETS/web-frameworks/`

Production-ready Flask patterns for building scalable web applications and API services. Covers application architecture, routing, authentication, middleware, and CORS handling.

#### `flask_multi_provider_api_proxy.py`
- **Description:** Production-ready Flask proxy server for multiple AI/LLM providers with comprehensive error handling, rate limiting, and CORS configuration
- **Use Cases:**
  - Building AI proxy services to centralize API key management
  - Creating unified interfaces across multiple LLM providers (OpenAI, Anthropic, xAI)
  - Implementing rate limiting and request tracking for API services
  - Proxying external APIs with CORS handling for frontend applications
  - Supporting provider failover and load balancing
- **Key Features:**
  - Multi-provider configuration with environment variable support
  - Enhanced CORS with origin validation and credentials support
  - In-memory rate limiting (20 requests/minute default)
  - Request/response logging with proper error handling
  - Health check and provider testing endpoints
  - Request ID tracking with UUID generation
  - Timeout protection (60s default)
- **Dependencies:** `flask`, `flask-cors`, `requests`, `python-dotenv`, `logging`
- **Source:** `/home/coolhand/html/storyblocks/api_proxy.py`, `/home/coolhand/servers/viewer/alt_text_server.py`

#### `flask_factory_pattern_with_blueprints.py`
- **Description:** Production-grade Flask application using factory pattern for testing and configuration flexibility with blueprint organization
- **Use Cases:**
  - Building scalable Flask applications with multiple modules
  - Supporting multiple deployment environments (dev, test, prod)
  - Implementing caching with graceful Redis fallback
  - Organizing routes into logical blueprints by domain
  - Creating testable Flask applications with dependency injection
- **Key Features:**
  - Application factory pattern for multiple app instances
  - Auto-detects Redis availability and falls back to SimpleCache
  - Blueprint registration with URL prefixes
  - Template and static folder configuration with absolute paths
  - Response compression (gzip) for bandwidth optimization
  - Environment-based configuration using Config class
  - Automatic directory creation for templates/static
- **Dependencies:** `flask`, `flask-cors`, `flask-caching`, `flask-compress`, `redis` (optional)
- **Source:** `/home/coolhand/servers/coca/app/__init__.py`, `/home/coolhand/servers/analytics/app.py`

#### `flask_middleware_patterns.py`
- **Description:** Comprehensive patterns for Flask middleware using before_request, after_request, and custom middleware classes
- **Use Cases:**
  - API request analytics and monitoring
  - Authentication and authorization middleware
  - Request/response timing and performance logging
  - Custom CORS handling for specific origins
  - Background task triggering (analytics, logging)
  - Request ID tracking and distributed tracing
- **Key Features:**
  - AnalyticsMiddleware class for automatic tracking
  - Request timing with X-Response-Time header
  - Request ID middleware with UUID generation
  - CORS middleware with origin validation
  - Authentication middleware with exempt endpoints
  - Centralized error handling for all HTTP errors
  - Background threading for non-blocking operations
- **Dependencies:** `flask`, `requests`, `logging`, `threading`
- **Source:** `/home/coolhand/servers/analytics/flask_middleware.py`, `/home/coolhand/html/storyblocks/api_proxy.py`

#### `flask_blueprint_organization.py`
- **Description:** Comprehensive patterns for organizing Flask applications using blueprints with service layer separation
- **Use Cases:**
  - Organizing routes by domain/resource (users, products, orders)
  - Creating RESTful API structures with consistent patterns
  - Implementing caching at route level with query string support
  - Separating business logic from route handlers (service layer pattern)
  - Building modular, testable applications
  - Supporting multiple API versions
- **Key Features:**
  - Blueprint definition with URL prefixes
  - Service layer pattern with factory functions
  - Route-level caching with @cache.cached decorator
  - RESTful endpoint patterns (search, count, list)
  - Blueprint-specific error handlers
  - Nested blueprint pattern for hierarchical routes
  - Multi-version API pattern (v1, v2)
- **Dependencies:** `flask`, `flask-caching`, `logging`
- **Source:** `/home/coolhand/servers/coca/app/routes/corpus.py`, `/home/coolhand/servers/coca/app/routes/ngrams.py`

#### `flask_authentication_decorators.py`
- **Description:** Production-ready authentication patterns using decorators for Flask routes with comprehensive auth strategies
- **Use Cases:**
  - API key authentication for public APIs
  - JWT token-based authentication with role validation
  - Role-based access control (RBAC)
  - License key validation for premium features
  - Rate limiting per user/API key
  - Optional authentication with tiered access
- **Key Features:**
  - @require_api_key decorator with environment variable support
  - @require_jwt_token decorator with PyJWT integration
  - @require_role decorator for RBAC with multiple roles
  - @require_valid_license decorator with custom validators
  - @rate_limit decorator with configurable windows
  - @optional_api_key for tiered access (free/paid)
  - Request context storage (g.user, g.api_key)
- **Dependencies:** `flask`, `functools`, `os`, `PyJWT` (optional)
- **Source:** `/home/coolhand/projects/apis/omni-api/api/core/decorators.py`, `/home/coolhand/projects/apis/omni-api/app.py`

#### `gunicorn_socketio_deployment.py` & `gunicorn_socketio_deployment.md`
- **Description:** Production deployment configuration for Flask-SocketIO applications using Gunicorn with eventlet worker class for WebSocket support
- **Use Cases:**
  - Production deployment of real-time dashboards
  - WebSocket-based collaborative applications
  - Live data streaming applications
  - Any Flask app requiring bidirectional client-server communication
- **Key Features:**
  - Single worker handles 5000-10000 concurrent WebSocket connections
  - Eventlet async I/O for efficient connection handling
  - Comprehensive deployment guide with systemd service templates
  - Nginx/Caddy reverse proxy configurations
  - Multi-worker setup with Redis message queue
  - Health check endpoints and monitoring
- **Dependencies:** `gunicorn`, `eventlet`, `Flask-SocketIO`, `redis` (for multi-worker)
- **Source:** `/home/coolhand/servers/coca/bluesky_firehose/start.sh`, `/home/coolhand/servers/coca/bluesky_firehose/app.py`

#### `flask_blueprint_with_url_prefix.py` ⭐ NEW
- **Description:** Flask Blueprint configuration for hosting applications under sub-paths with proper session cookie handling
- **Use Cases:**
  - Multi-service monorepo with shared domain (dr.eamer.dev/service1, /service2)
  - API versioning (/api/v1, /api/v2)
  - Reverse proxy sub-path routing
  - Microservices behind a gateway
- **Key Features:**
  - URL prefix handling for Blueprint routes
  - SESSION_COOKIE_PATH scoping (critical for auth to work)
  - Static file routing with url_path configuration
  - url_for() automatic prefix generation
  - Complete working example with verification
- **Dependencies:** `flask`
- **Source:** `/home/coolhand/servers/studio/app.py`

#### `flask_multipart_file_upload.py` ⭐ NEW
- **Description:** Comprehensive file upload handling with validation, type checking, and secure processing
- **Use Cases:**
  - Image upload for AI vision models
  - Audio file upload for speech-to-text
  - Video upload for processing
  - Document upload for analysis
  - Multiple file uploads
- **Key Features:**
  - File existence and filename validation
  - Extension whitelist checking
  - Optional PIL image validation (dimensions, validity)
  - Temporary file handling with automatic cleanup
  - Multiple file upload support
  - Secure filename sanitization (werkzeug.utils.secure_filename)
  - Base64 encoding for API submission
- **Dependencies:** `flask`, `PIL/Pillow` (optional), `werkzeug`
- **Source:** `/home/coolhand/servers/studio/app.py`

#### `flask_audio_file_handler.py` ⭐ NEW
- **Description:** Audio file upload, validation, and processing for speech-to-text and text-to-speech workflows
- **Use Cases:**
  - Speech-to-text transcription (OpenAI Whisper, Assembly AI)
  - Text-to-speech generation (OpenAI TTS, ElevenLabs)
  - Audio format conversion
  - Audio metadata extraction
- **Key Features:**
  - Audio format validation (mp3, wav, m4a, ogg, flac, webm)
  - Optional pydub validation (duration, sample rate, channels)
  - Transcription endpoint pattern
  - TTS generation endpoint pattern
  - Audio format conversion with pydub
  - Metadata extraction
  - Base64 audio response pattern
- **Dependencies:** `flask`, `pydub` (optional), `werkzeug`
- **Source:** `/home/coolhand/servers/studio` (patterns extracted)

#### `flask_video_generation_handler.py` ⭐ NEW
- **Description:** Video upload, processing, and AI generation handler
- **Use Cases:**
  - AI video generation (image-to-video, text-to-video)
  - Video upload for analysis
  - Video format conversion
  - Thumbnail generation from video frames
- **Key Features:**
  - Video format validation (mp4, avi, mov, webm, mkv)
  - Optional OpenCV validation (duration, resolution, fps)
  - Video generation endpoint (sync or async with task queue)
  - Video analysis endpoint
  - Thumbnail extraction at specific timestamps
  - File download endpoint with security validation
- **Dependencies:** `flask`, `opencv-python` (optional), `werkzeug`
- **Source:** `/home/coolhand/servers/studio/app.py`

#### `javascript_loading_states_pattern.js` ⭐ NEW
- **Description:** Comprehensive loading state management for async operations in frontend applications
- **Use Cases:**
  - Form submissions with async processing
  - File uploads with progress indication
  - API calls with loading spinners
  - Multi-step workflows with state tracking
- **Key Features:**
  - Basic single loading state pattern
  - Advanced multi-operation tracking with LoadingStateManager
  - File upload with progress bars
  - Button state management (loading, success, error)
  - Toast notifications
  - Fetch with timeout
  - Always using try/finally for cleanup
  - User-friendly error messages
- **Dependencies:** None (vanilla JavaScript)
- **Source:** `/home/coolhand/servers/studio/templates/index.html`

---

### Real-Time Dashboards

**Location:** `/home/coolhand/SNIPPETS/real-time-dashboards/`

Patterns for building real-time data dashboards with live updates, streaming data visualization, and bidirectional communication.

#### `flask_socketio_broadcaster.py`
- **Description:** Flask application with SocketIO for real-time bidirectional communication with server-to-client broadcasting and background data processing
- **Use Cases:**
  - Real-time dashboards updating live data
  - Live notifications and alerts
  - Collaborative applications with multi-user updates
  - Streaming data visualization
  - Progress tracking for long-running tasks
- **Key Features:**
  - Thread-safe broadcasting to all clients or specific rooms
  - Connection tracking and client management
  - Room-based selective broadcasting
  - Background thread integration for periodic updates
  - HTTP endpoints to trigger broadcasts
  - async_mode='threading' for dev, 'eventlet' for production
- **Dependencies:** `Flask`, `Flask-SocketIO`, `Flask-CORS`, `python-socketio`
- **Source:** `/home/coolhand/servers/coca/bluesky_firehose/app.py`

---

### WebSocket Patterns

**Location:** `/home/coolhand/SNIPPETS/websocket-patterns/`

Production-ready WebSocket client patterns for consuming real-time data streams with automatic reconnection and error handling.

#### `websocket_firehose_reconnection.py`
- **Description:** Robust asyncio-based WebSocket client for consuming real-time data streams (firehoses) with automatic reconnection, timeout handling, and graceful error recovery
- **Use Cases:**
  - Consuming real-time data streams (Bluesky, Twitter firehoses)
  - Long-running WebSocket connections requiring high reliability
  - Event-driven data processing pipelines
  - Real-time monitoring systems
- **Key Features:**
  - Automatic reconnection with exponential backoff
  - Timeout detection with ping/pong health checks
  - Graceful error handling for JSON decoding errors
  - State management for clean shutdown
  - Configurable timeouts and reconnection delays
  - Callback-based message processing
- **Dependencies:** `websockets`, `asyncio`
- **Source:** `/home/coolhand/servers/coca/bluesky_firehose/app.py`

---

### Sentiment Analysis

**Location:** `/home/coolhand/SNIPPETS/sentiment-analysis/`

Sentiment analysis patterns using VADER for social media text and real-time sentiment monitoring.

#### `vader_sentiment_analyzer.py`
- **Description:** VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis wrapper with batch processing and filtering capabilities
- **Use Cases:**
  - Analyzing social media posts, tweets, comments
  - Real-time sentiment monitoring of text streams
  - Customer feedback analysis
  - Brand monitoring and reputation management
  - Content moderation based on sentiment
- **Key Features:**
  - Simple function and class-based interfaces
  - Batch analysis with distribution statistics
  - Filtering by sentiment label
  - Most positive/negative text extraction
  - Configurable sentiment thresholds
  - Fast processing (1-2ms per text, thousands per second)
- **Dependencies:** `vaderSentiment`
- **Source:** `/home/coolhand/servers/coca/bluesky_firehose/app.py`

---

### Database Patterns

**Location:** `/home/coolhand/SNIPPETS/database-patterns/`

SQLite integration patterns for Flask applications with proper connection handling and error management.

#### `sqlite_flask_simple_pattern.py`
- **Description:** Straightforward SQLite integration for Flask applications using connection-per-operation pattern with context managers and proper error handling
- **Use Cases:**
  - Logging and metrics collection
  - Simple data persistence for dashboards
  - Prototype and development applications
  - Background tasks with isolated database access
  - Applications where each operation is fast and independent
- **Key Features:**
  - Context manager for safe connection handling
  - WAL mode for better concurrency
  - Row factory for dict-like access
  - Comprehensive examples for CRUD operations
  - Index creation for common queries
  - Good for < 100 requests/second
- **Dependencies:** `sqlite3` (standard library), `Flask`
- **Source:** `/home/coolhand/servers/coca/bluesky_firehose/app.py`

---

### Async Patterns

**Location:** `/home/coolhand/SNIPPETS/async-patterns/`

Asyncio patterns for concurrent operations, background tasks, and integrating async code with synchronous frameworks.

#### `flask_asyncio_background_thread.py`
- **Description:** Pattern for running asyncio event loops in background threads alongside Flask applications, enabling async tasks without blocking request handling
- **Use Cases:**
  - WebSocket client consuming real-time data while serving HTTP API
  - Background async tasks (data polling, API calls) with Flask frontend
  - Integrating async libraries (aiohttp, websockets) with Flask
  - Long-running async operations without blocking Flask responses
  - Combining Flask-SocketIO with asyncio WebSocket clients
- **Key Features:**
  - AsyncBackgroundRunner for managing event loops in threads
  - Graceful start/stop with daemon thread support
  - MultiAsyncRunner for running multiple async tasks concurrently
  - Thread-safe communication between Flask and async code
  - Proper event loop lifecycle management
  - Example integration with WebSocket firehose consumers
- **Dependencies:** `asyncio`, `threading`, `Flask`
- **Source:** `/home/coolhand/servers/coca/bluesky_firehose/app.py`

---

### Data Visualization

**Location:** `/home/coolhand/SNIPPETS/data-visualization/`

Battle-tested visualization patterns extracted from production datavis projects. Interactive charts, maps, timelines, and animation patterns using D3.js, Chart.js, Leaflet, and vanilla JavaScript.

#### `d3-force-network-visualization.js`
- **Description:** Complete pattern for creating interactive force-directed graphs with mobile support, filtering, tooltips, and pinned node layouts
- **Use Cases:**
  - Corporate board interlocks and relationship mapping
  - Social network visualization
  - Organization charts with cross-functional relationships
  - Knowledge graphs and entity relationships
- **Key Features:**
  - Mobile touch handling (pinch-to-zoom, drag, tap)
  - "Dream catcher" layout with pinned peripheral nodes
  - Connection type indicators via line styling
  - Dynamic filtering and re-rendering
  - Keyboard accessible navigation
- **Dependencies:** D3.js v7+
- **Source:** `/home/coolhand/html/datavis/dowjones/script.js`

#### `timeline-animation-interactive.js`
- **Description:** Animated timeline showing historical progression with future projections for data-driven storytelling
- **Use Cases:**
  - Crisis timeline visualization (hospital closures, climate events)
  - Before/after policy impact projection
  - Temporal progression with narrative context
  - Educational timelines with automated playback
- **Key Features:**
  - Historical + projection modes with visual distinction
  - Playback controls and keyboard shortcuts
  - Scrolling event feed
  - Animated number counters with easing
  - Narrative text system tied to specific years
- **Dependencies:** Vanilla JavaScript (no framework)
- **Source:** `/home/coolhand/html/datavis/healthcare_deserts/UX-TEST/layout-crisis-timeline/script.js`

#### `data-transformation-utils.js`
- **Description:** Comprehensive collection of utility functions for data loading, parsing, formatting, filtering, and state management
- **Use Cases:**
  - CSV/JSON data loading with error handling
  - Number and percentage formatting for display
  - Data filtering and grouping operations
  - Simple state management without frameworks
  - UI performance optimization
- **Key Features:**
  - `loadCSV()`, `loadJSON()` with error handling
  - `formatNumber()`, `formatPercent()`, `formatCurrency()`, `formatDate()`
  - `filterBySearch()`, `groupBy()`, `sortBy()`, `aggregate()`
  - `AppState` class - lightweight pub/sub pattern
  - `debounce()`, `throttle()` for performance
  - `animateValue()`, `observeElements()` for animations
- **Dependencies:** None (pure JavaScript)
- **Source:** `/home/coolhand/html/datavis/healthcare_deserts/UX-TEST/shared/utils.js`

#### `leaflet-choropleth-map.js`
- **Description:** Create interactive choropleth maps with Leaflet showing data density by geographic regions
- **Use Cases:**
  - Geographic data visualization (population, statistics, counts)
  - Regional analysis and comparison
  - Data-driven storytelling with maps
  - County/state/country-level visualizations
- **Key Features:**
  - Color scale based on data density
  - Hover highlighting with visual feedback
  - Information control and legend
  - Fully customizable color scheme
- **Dependencies:** Leaflet.js, GeoJSON data
- **Source:** Previously existing in snippets library

#### `chart-js-responsive-dashboards.js`
- **Description:** Complete patterns for creating interactive, themeable dashboards using Chart.js
- **Use Cases:**
  - Multi-metric comparison dashboards
  - Financial data visualization (spending, revenue, budgets)
  - Statistical analysis displays
  - KPI monitoring and reporting
- **Key Features:**
  - Multiple chart types: bar, bubble, radar, line
  - Dark/light theme support with CSS custom properties
  - Charts auto-update on theme change
  - Chart registry for lifecycle management
  - Color palette generator for multi-series charts
- **Dependencies:** Chart.js v3+, optional chartjs-plugin-datalabels
- **Source:** `/home/coolhand/html/datavis/spending/federal_spending_chart_modern.html`

---

### Data Processing

**Location:** `/home/coolhand/SNIPPETS/data-processing/`

Comprehensive data transformation, validation, and pipeline patterns for processing structured data.

#### `format_conversion_patterns.py`
- **Description:** Multi-format data conversion (JSON, YAML, TOML, XML, CSV)
- **Use Cases:**
  - Converting configuration files between formats
  - Transforming API responses to different output formats
  - Batch converting data export files
  - Building format-agnostic data processing pipelines
- **Key Features:**
  - Universal format converter with auto-detection
  - Pretty-printing and minification
  - CSV conversion for flat and nested data
  - XML generation with configurable structure
  - Unicode-safe conversion (ensure_ascii=False)
- **Dependencies:** `json`, `yaml`, `toml`, `xml.dom.minidom`, `csv`
- **Source:** `/home/coolhand/projects/apis/api-v3/gen/api-tools/tools/data/processing/`, `/home/coolhand/projects/swarm/hive/swarm_data.py`

#### `pydantic_validation_patterns.py`
- **Description:** Data validation and schema generation using Pydantic
- **Use Cases:**
  - Validating API request/response data
  - Building type-safe tool interfaces for LLM function calling
  - Converting between Python objects and JSON schemas
  - Sanitizing user input with automatic type coercion
  - Creating configuration validators with defaults
- **Key Features:**
  - Field validators with automatic sanitization
  - OpenAI function calling schema generation
  - Nested model validation
  - Safe validation with detailed error reporting
  - Data transformation during validation
  - Serialization with exclusion options
- **Dependencies:** `pydantic`
- **Source:** `/home/coolhand/projects/swarm/hive/swarm_data.py`, `/home/coolhand/enterprise_orchestration/core/base.py`

#### `json_validation_patterns.py`
- **Description:** JSON validation, analysis, and manipulation (stdlib only)
- **Use Cases:**
  - Validating JSON API responses before processing
  - Analyzing JSON structure for debugging
  - Extracting all keys from nested JSON for schema discovery
  - Formatting/minifying JSON for storage
  - Building JSON diff tools and validators
- **Key Features:**
  - Statistical analysis (depth, type counts)
  - Key extraction with dot-notation paths
  - Path-based value get/set operations
  - JSON comparison and diff generation
  - No external dependencies (pure stdlib)
- **Dependencies:** `json`, `typing`
- **Source:** `/home/coolhand/projects/apis/cli_tools/json_format.py`

#### `data_sanitization_patterns.py`
- **Description:** Data sanitization and cleaning for various input sources
- **Use Cases:**
  - Sanitizing user input before database storage
  - Cleaning API response data for consistency
  - Normalizing text data for search and comparison
  - Validating and formatting email addresses and URLs
  - Removing sensitive information from logs
- **Key Features:**
  - Text sanitization (control chars, whitespace, HTML)
  - Email and URL validation with normalization
  - Username and filename sanitization
  - Type coercion with bounds checking
  - Dictionary key filtering
  - Unicode normalization and accent removal
- **Dependencies:** `re`, `html`, `urllib.parse`, `unicodedata`
- **Source:** Security patterns from `/home/coolhand/projects/tools_bluesky`, text processing from Swarm modules

#### `data_aggregation_pipeline_patterns.py`
- **Description:** Data aggregation and pipeline transformation patterns
- **Use Cases:**
  - Building ETL (Extract, Transform, Load) pipelines
  - Aggregating data from multiple sources
  - Implementing map-reduce style processing
  - Creating data analysis workflows
  - Building streaming data processors
- **Key Features:**
  - Chainable pipeline operations (map, filter, flatmap)
  - Dictionary-specific pipeline for structured data
  - Aggregation functions (sum, avg, min, max, count)
  - Group by and count by operations
  - Left join for combining datasets
  - Functional composition patterns
- **Dependencies:** `typing`, `functools`, `collections`, `itertools`
- **Source:** Patterns from data processing across Swarm and enterprise orchestration projects

---

### File Operations

**Location:** `/home/coolhand/SNIPPETS/file-operations/`

File I/O, path handling, module discovery, and configuration management patterns.

#### `config_file_loading.py`
- **Description:** Load and save configuration from multiple file formats (JSON, YAML, .env, key=value) with automatic type conversion
- **Use Cases:**
  - Loading application settings from various config formats
  - Supporting both development (.env) and production (YAML/JSON) configs
  - Type-safe configuration with automatic conversion (bool, int, float)
  - Hierarchical configuration loading with defaults
- **Key Features:**
  - Automatic format detection from file extension
  - Type conversion (booleans, integers, floats, quoted strings)
  - Graceful handling when PyYAML not available
  - Support for comments and empty lines in key=value files
  - Save config with sensitive key filtering
- **Dependencies:** `pathlib`, `json`, `os`, optional: `pyyaml`
- **Source:** `/home/coolhand/shared/utils/__init__.py`, `/home/coolhand/projects/swarm/core/core_config.py`

#### `path_handling_utils.py`
- **Description:** Modern path manipulation utilities using pathlib.Path for cross-platform compatibility
- **Use Cases:**
  - Cross-platform file path handling (Windows, Linux, Mac)
  - Project directory structure management
  - Safe path operations with validation
  - Finding project root or config directories
  - Path normalization and resolution
- **Key Features:**
  - Absolute path conversion with user directory expansion
  - Project root detection via marker files (.git, pyproject.toml, etc.)
  - Safe directory creation with parents
  - Path traversal attack prevention
  - File extension manipulation
  - Pattern-based file finding (glob)
  - Relative path calculation
- **Dependencies:** `pathlib`, `os`, `typing`
- **Source:** `/home/coolhand/projects/swarm/core/core_config.py`, `/home/coolhand/enterprise_orchestration/cli.py`

#### `module_discovery.py`
- **Description:** Dynamic module discovery and loading from directories with pattern detection
- **Use Cases:**
  - Building plugin systems that auto-discover modules
  - Loading tool modules dynamically for AI agents
  - Creating extensible architectures without hardcoded imports
  - Hot-reload for testing and development
  - Module validation and compatibility checking
- **Key Features:**
  - Pattern-based module discovery (glob patterns)
  - Safe module loading with error handling
  - Required attribute/function validation
  - Multiple pattern detection (tool schemas, registration functions)
  - Function extraction from modules
  - Module interface validation
  - Exclusion patterns for test files and private modules
- **Dependencies:** `pathlib`, `importlib.util`, `sys`, `typing`, `inspect`
- **Source:** `/home/coolhand/projects/swarm/core/core_registry.py`, `/home/coolhand/projects/swarm/hive/`

#### `comprehensive_document_parser.py`
- **Description:** Production-ready parser for 50+ file formats with graceful fallbacks and metadata extraction
- **Use Cases:**
  - Document processing pipelines for AI/RAG systems
  - Content extraction for search indexing
  - Multi-format file analysis tools
  - Knowledge base ingestion systems
  - Content migration and conversion tools
- **Key Features:**
  - 50+ supported formats (PDF, DOCX, XLSX, CSV, HTML, JSON, Jupyter notebooks, etc.)
  - Graceful fallback when optional dependencies unavailable
  - Memory-efficient processing for large files
  - Encoding detection for text files
  - Archive inspection and text extraction
  - Comprehensive error messages with installation suggestions
- **Dependencies:** Core: `pathlib`, `re`, `csv`, `json`; Optional: `pdfminer.six`, `python-docx`, `openpyxl`, `beautifulsoup4`
- **Source:** `/home/coolhand/shared/utils/document_parsers.py`

#### `yaml_frontmatter_markdown_parser.py` ⭐ NEW
- **Description:** Complete toolkit for parsing markdown files with YAML frontmatter, extracting metadata, sections by headers, tables, and nested structures
- **Use Cases:**
  - Parsing agent definition files with structured metadata
  - Building documentation systems from markdown
  - Extracting configuration from markdown files
  - Converting markdown tables to structured data
  - Processing Jekyll/Hugo-style content
- **Key Features:**
  - Frontmatter extraction (YAML between --- markers)
  - Section parsing by header level (## or ###)
  - Markdown table parsing to list of dicts
  - Nested section support (parent/child headers)
  - Code block extraction by language
  - Bullet and numbered list parsing
  - Key-value pair extraction from markdown
- **Dependencies:** `re`, `yaml`, `pathlib`, `typing`
- **Source:** `/home/coolhand/geepers-orchestrators/parser/markdown_parser.py`

---

### Utilities

**Location:** `/home/coolhand/SNIPPETS/utilities/`

General-purpose utility functions for common programming tasks including retry logic, caching, logging, string manipulation, date/time handling, and rate limiting.

#### `retry_decorator.py`
- **Description:** Production-ready retry decorator with exponential backoff and jitter
- **Use Cases:** API calls with transient failures, database operations, external service integrations
- **Key Features:** Exponential backoff, configurable exceptions, jitter variant
- **Dependencies:** `functools`, `time`, `logging`
- **Source:** `/home/coolhand/shared/utils/__init__.py`

#### `redis_cache_manager.py`
- **Description:** Redis caching utilities with TTL support and decorator-based caching
- **Use Cases:** Caching LLM calls, rate limiting, session state, distributed caching
- **Key Features:** JSON serialization, TTL support, decorator caching, graceful degradation
- **Dependencies:** `redis`, `json`, `functools`
- **Source:** `/home/coolhand/shared/memory/__init__.py`

#### `cache_manager_redis_fallback.py` ⭐ NEW
- **Description:** Production-ready cache manager with Redis primary and automatic in-memory fallback
- **Use Cases:**
  - LLM response caching to reduce API costs (40-100x savings)
  - API rate limiting with distributed state
  - Session storage across multiple instances
  - Expensive computation caching
  - Multi-instance cache sharing with local fallback
- **Key Features:**
  - Automatic Redis connection testing on initialization
  - Graceful fallback to in-memory dict if Redis unavailable
  - TTL support (Redis native, datetime-based for memory)
  - SHA256 cache key generation for compact, deterministic keys
  - Statistics tracking (hits, misses, hit rate, backend type)
  - Namespace support via configurable key prefix
  - Automatic expired entry cleanup for memory cache
  - Thread-safe in-memory cache with expiration timestamps
- **Dependencies:** `redis` (optional), `hashlib`, `json`, `logging`
- **Source:** `/home/coolhand/servers/studio/cache_manager.py`

#### `rate_limiter.py`
- **Description:** Multiple rate limiting implementations (async, token bucket, sliding window)
- **Use Cases:** API rate limiting, concurrent request control, multi-provider management
- **Key Features:** AsyncRateLimiter, TokenBucketRateLimiter, SlidingWindowRateLimiter, MultiProviderRateLimiter
- **Dependencies:** `asyncio`, `threading`, `time`
- **Source:** `/home/coolhand/projects/swarm/SUGGESTIONS.md`

#### `datetime_utilities.py`
- **Description:** Date and time manipulation for parsing, formatting, timestamps
- **Use Cases:** ISO 8601 parsing, relative time formatting, Unix timestamps
- **Key Features:** Timezone-aware handling, relative time, duration formatting
- **Dependencies:** `datetime`, `typing`
- **Source:** `/home/coolhand/projects/swarm/llms/anthropic_chat.py`

#### `logging_utilities.py`
- **Description:** Comprehensive logging with JSON support, multiple handlers, log rotation
- **Use Cases:** Structured logging, multi-handler logging, context-aware logging
- **Key Features:** JSON formatting, colored terminal output, context injection, performance logging
- **Dependencies:** `logging`, `json`, `pathlib`
- **Source:** `/home/coolhand/shared/observability/__init__.py`

#### `env_config_utilities.py`
- **Description:** Environment variable loading and validation with type conversion
- **Use Cases:** Loading API keys, type-safe parsing, multi-environment configuration
- **Key Features:** Type conversion, required/optional variables, list/dict parsing
- **Dependencies:** `os`, `typing`
- **Source:** `/home/coolhand/shared/utils/__init__.py`

#### `crypto_utilities.py` ⭐ NEW
- **Description:** Lightweight cryptographic helpers for hashing, HMAC signatures, key derivation, and optional Fernet encryption
- **Use Cases:**
  - API request signing and verification
  - Password hashing and key derivation (PBKDF2)
  - Data integrity verification
  - Token generation and validation
  - Secure configuration encryption
- **Key Features:**
  - SHA-256/512 hashing with multiple algorithms
  - HMAC generation and constant-time verification
  - PBKDF2-HMAC key derivation (100,000 iterations default)
  - URL-safe token generation
  - Optional Fernet symmetric encryption
  - File hashing with chunked reads
- **Dependencies:** `hashlib`, `hmac`, `secrets` (stdlib), `cryptography` (optional)
- **Source:** `/home/coolhand/shared/utils/crypto.py`

#### `string_utilities.py`
- **Description:** String manipulation for text processing, sanitization, validation
- **Use Cases:** Input sanitization, URL slugs, data extraction, masking sensitive info
- **Key Features:** HTML stripping, slug generation, data extraction, text normalization
- **Dependencies:** `re`, `html`
- **Source:** Multiple swarm modules

#### `base-class-pattern.py`
- **Description:** Extensible base class pattern for plugin systems
- **Use Cases:** API tool libraries, plugin architectures, multi-provider integrations
- **Key Features:** UserValves pattern, event emitter, abstract method enforcement
- **Dependencies:** `pydantic`, `abc`
- **Source:** `/home/coolhand/SNIPPETS/utilities/base-class-pattern.py`

#### `embedding_generation_similarity.py`
- **Description:** Production-ready pattern for generating text embeddings and performing semantic similarity search using multiple providers
- **Use Cases:**
  - Semantic search and document retrieval
  - RAG (Retrieval Augmented Generation) systems
  - Content recommendation engines
  - Text similarity and clustering
  - Duplicate detection and question answering
- **Key Features:**
  - Multi-provider support (Ollama local models, OpenAI, custom endpoints)
  - Cosine similarity calculation
  - Top-K similarity search
  - Vector serialization to bytes for database storage
  - Batch embedding generation
  - Memory-efficient numpy operations
- **Dependencies:** `numpy`, optional: `ollama`, `openai`
- **Source:** `/home/coolhand/shared/utils/embeddings.py`

#### `timezone_and_duration_utilities.py`
- **Description:** Comprehensive timezone conversion, time difference calculation, and duration parsing utilities using pytz
- **Use Cases:**
  - Multi-timezone applications (scheduling, calendars)
  - Time difference calculations for distributed systems
  - Duration parsing and addition for time-based logic
  - International application time handling
  - Timezone validation and current time retrieval
- **Key Features:**
  - Accurate timezone handling with pytz
  - DST (Daylight Saving Time) awareness
  - Simple duration string format ("2d3h30m")
  - Timezone validation before operations
  - Grouped timezone listing by region
  - Historical timezone data support
- **Dependencies:** `pytz`, `datetime`
- **Source:** `/home/coolhand/shared/utils/time_utils.py`

#### `flask_image_handling.py` ⭐ NEW
- **Description:** Robust image decoding, validation, and response formatting for Flask vision APIs
- **Use Cases:**
  - Flask APIs accepting image uploads for analysis
  - Alt text generation services
  - Image classification endpoints
  - OCR services with image input
  - Any vision API that needs multiple input formats
- **Key Features:**
  - Handles both JSON (base64) and multipart form uploads
  - Automatically strips data URI prefixes
  - Validates image size before processing (prevents OOM)
  - Standardized success/error responses
  - Smart text truncation at sentence boundaries
  - Image preparation for API consumption (base64, data URI)
- **Dependencies:** `flask`, `base64`, `typing`
- **Source:** `/home/coolhand/shared/web/vision_service.py`

---

### Vision Patterns

**Location:** `/home/coolhand/SNIPPETS/vision-patterns/`

Production-ready patterns for AI-powered vision analysis including image description, video frame extraction, and content-based filename generation.

#### `vision_client.py` ⭐ NEW
- **Description:** Comprehensive vision analysis client for image and video analysis using AI vision models (xAI Grok Vision, OpenAI Vision, etc.) with structured results
- **Use Cases:**
  - Image description and alt text generation
  - Video analysis via frame extraction
  - AI-powered filename generation from visual content
  - Accessibility applications (describing images)
  - Content moderation and classification
  - Visual search and cataloging
- **Key Features:**
  - VisionResult dataclass for structured responses
  - VisionClient class with image and video analysis
  - Multi-provider support (xAI as primary, OpenAI-compatible API)
  - Video frame extraction at configurable positions
  - Base64 encoding utilities for API consumption
  - Convenience functions for quick analysis
  - Graceful fallbacks for optional dependencies (PIL, OpenCV)
  - AI-powered filename generation from content
- **Dependencies:** `openai`, `Pillow` (optional), `opencv-python` (optional)
- **Source:** `/home/coolhand/projects/packages/working/vision-utils/vision_utils/core.py`

---

### Accessibility

**Location:** `/home/coolhand/SNIPPETS/accessibility/`

Comprehensive WCAG 2.1-compliant accessibility patterns for building inclusive web applications. Extracted from production accessibility resource platform serving thousands of users.

#### `url_validation_pattern.py`
- **Description:** Robust URL validation and link checking for accessibility audits
- **Use Cases:**
  - Accessibility compliance checking (broken links, redirects)
  - Content management systems (pre-publish link validation)
  - Documentation maintenance (automated link health checks)
  - SEO optimization (identify and fix redirect chains)
  - Migration tools (validate links during content migration)
- **Key Features:**
  - Rate limiting and retry logic with exponential backoff
  - HTML and Markdown link extraction with HTMLParser
  - Redirect detection and final URL tracking
  - Comprehensive error categorization (404, SSL, timeout, DNS)
  - Section context preservation for better error reporting
  - Batch processing with progress reporting
  - URL deduplication while preserving metadata
- **Dependencies:** `urllib`, `socket`, `typing`, `html.parser`
- **Source:** `/home/coolhand/html/accessibility/link_validator.py`

#### `link_remediation_pattern.py`
- **Description:** Automated link fixing and remediation for broken links, redirects, and SSL issues
- **Use Cases:**
  - Automated link maintenance in documentation
  - Content migration (update old URLs to new domains)
  - Post-validation link fixing workflow
  - Accessibility compliance remediation
  - Periodic link hygiene in CI/CD pipelines
- **Key Features:**
  - Apply redirects to final destinations
  - Fix broken 404 links with replacement URLs
  - Handle SSL certificate issues
  - Support both HTML (`href` attributes) and Markdown (`[text](url)`) formats
  - Generate detailed changelogs for tracking changes
  - Integration with validation results from url_validation_pattern.py
  - Safe regex-based replacement
- **Dependencies:** `re`, `typing`, `json`
- **Source:** `/home/coolhand/html/accessibility/link_fixer.py`

#### `accessible_theme_switcher.js`
- **Description:** Accessible theme switching with screen reader support and localStorage persistence
- **Use Cases:**
  - Dark/light mode implementations
  - High contrast themes for visual impairments
  - CVI-optimized themes (Cortical Visual Impairment - yellow on black)
  - Color blindness-friendly themes (deuteranopia, protanopia)
  - Photophobia accommodations (blue light reduction)
  - User preference persistence across sessions
- **Key Features:**
  - CSS custom properties (CSS variables) for theming
  - Screen reader announcements on theme change
  - ARIA attributes (aria-pressed) for proper state indication
  - localStorage persistence
  - Multiple theme support (dark, light, high contrast, CVI, colorblind-friendly)
  - Keyboard accessible
  - OS preference detection (prefers-color-scheme media query)
  - Class and standalone function implementations
- **Dependencies:** Modern browser with CSS variables and localStorage
- **Source:** `/home/coolhand/html/accessibility/index.html`

#### `screen_reader_announcements.js`
- **Description:** Dynamic content announcements to screen readers using ARIA live regions
- **Use Cases:**
  - Single Page Applications (dynamic content updates)
  - Form validation messages
  - Status updates (loading, success, error)
  - Toast notifications
  - Real-time data updates (chat, notifications, live scores)
  - Search results announcements
  - Modal dialog state changes
- **Key Features:**
  - Polite and assertive announcement levels
  - Automatic cleanup of announcement elements
  - Persistent live regions for frequent updates
  - Helper functions for common patterns
  - Integration with React/Vue/vanilla JS
  - Minimal DOM footprint (sr-only class)
  - Specialized functions (form errors, loading states, page changes)
- **Dependencies:** Modern browser with ARIA support
- **Source:** `/home/coolhand/html/accessibility/index.html`

#### `skip_links_and_landmarks.html`
- **Description:** WCAG-compliant skip navigation links and HTML5 landmark structure
- **Use Cases:**
  - WCAG 2.1 Level A/AA compliance (Success Criterion 2.4.1)
  - Keyboard navigation efficiency
  - Screen reader navigation structure
  - Long pages with repeated navigation
  - Complex layouts with multiple sections
  - Documentation sites and content-heavy pages
- **Key Features:**
  - Skip to main content implementation
  - Proper landmark regions (banner, navigation, main, complementary, contentinfo)
  - Focus management with tabindex="-1"
  - High contrast focus indicators (#ffff00 background, #ff00ff outline)
  - ARIA labels for multiple navigation regions
  - Screen reader announcements on skip
  - Complete working HTML/CSS/JS example with comments
- **Dependencies:** HTML5, CSS, JavaScript
- **Source:** `/home/coolhand/html/accessibility/index.html`

#### `keyboard_navigation_pattern.js`
- **Description:** Comprehensive keyboard navigation patterns for accessible web applications
- **Use Cases:**
  - Smooth scrolling with sticky header compensation
  - Table of contents navigation
  - Keyboard shortcuts for power users
  - Custom widget navigation (tabs, menus, toolbars)
  - Modal focus trapping
  - Back to top buttons with focus restoration
  - Arrow key list navigation
- **Key Features:**
  - Smooth scroll with configurable offset for fixed headers
  - Roving tabindex pattern (ARIA Authoring Practices Guide)
  - Focus trap for modals/dialogs with Tab wrapping
  - Keyboard shortcut manager with conflict prevention
  - Arrow key navigation for lists (Up/Down)
  - Back to top with automatic focus restoration
  - WCAG 2.1 Level A/AA compliant
  - Prevents interference with form inputs
- **Dependencies:** Modern browser with DOM support
- **Source:** `/home/coolhand/html/accessibility/index.html`

#### `altflow_accessible_alt_text.py` ⭐ NEW
- **Description:** Professional-grade alt text generation following WCAG accessibility standards (AltFlow Coze agent pattern)
- **Use Cases:**
  - CMS platforms requiring automated alt text for uploaded images
  - Accessibility tools for web content management
  - Screen reader optimization workflows
  - Compliance testing for WCAG 2.1 Level AA
  - Batch processing of image libraries for accessibility
- **Key Features:**
  - Strict, accessible alt text without social-emotional speculation (unless requested)
  - Default max length 700 characters (adjustable)
  - Automatically strips incorrect "Alt text:" prefixes
  - Handles sensitive content factually without judgment
  - Identifies famous people/characters for context
  - Processes ALL images regardless of content
  - Both async and sync (Flask-compatible) interfaces
- **Dependencies:** LLM provider with vision capabilities (OpenAI GPT-4V, Anthropic Claude, xAI Grok)
- **Source:** `/home/coolhand/shared/web/vision_service.py` (ALTTEXT_SYSTEM_PROMPT, generate_alt_text)

---

## Usage Guidelines

### How to Use a Snippet

1. **Read the Documentation:** Each snippet includes comprehensive docstrings explaining:
   - What the code does
   - Use cases
   - Dependencies
   - Important notes
   - Related snippets

2. **Check Dependencies:** Install required packages:
   ```bash
   # Example for multi_provider_abstraction.py
   pip install openai typing
   ```

3. **Copy and Customize:** Copy the snippet to your project and adjust:
   - Import paths
   - Configuration values
   - API keys (use environment variables!)
   - Model names and parameters

4. **Run Examples:** Most snippets include usage examples at the bottom:
   ```bash
   python snippet_name.py
   ```

### Best Practices

- **Never hardcode secrets:** Use environment variables or configuration files
- **Test thoroughly:** Adapt examples to your specific use case
- **Review security:** Especially for eval(), file operations, and API calls
- **Update dependencies:** Check for newer versions of required packages
- **Contribute improvements:** If you enhance a snippet, consider contributing back

### Pattern Naming Convention

Snippets follow this naming pattern:
- `descriptive_name_pattern.py` - Main pattern implementation
- Use underscores, not hyphens
- Clear, descriptive names that indicate purpose

---

## Contributing

### Adding New Snippets

When adding a new snippet to this library:

1. **Follow the Template:**
   ```python
   """
   [Descriptive Title]

   Description: [What this code does and when to use it]

   Use Cases:
   - [Specific scenario 1]
   - [Specific scenario 2]

   Dependencies:
   - [List required packages]

   Notes:
   - [Important considerations]
   - [Common pitfalls to avoid]

   Related Snippets:
   - [Cross-references to related patterns]

   Source Attribution:
   - Extracted from: [Original file path]
   - Related patterns: [Other source locations]
   """
   ```

2. **Quality Standards:**
   - ✅ Complete and immediately usable
   - ✅ Self-documenting with clear variable names
   - ✅ Proper error handling and edge cases
   - ✅ Generalized (remove project-specific details)
   - ✅ Comprehensive documentation
   - ✅ Usage examples included

3. **Update This README:**
   - Add entry in appropriate category
   - Include description, use cases, key features
   - List dependencies
   - Provide source attribution

4. **Cross-Reference:**
   - Link related snippets in docstrings
   - Update related snippets to reference new addition

---

## Source Attribution

All snippets are extracted from the AI Development Ecosystem codebase:

### Primary Sources

- **Swarm System:** `/home/coolhand/projects/swarm/`
  - Tool module patterns
  - CLI patterns
  - Configuration management

- **Beltalowda:** `/home/coolhand/html/belta/`
  - Multi-agent orchestration
  - Hierarchical agent patterns

- **Enterprise Orchestration:** `/home/coolhand/enterprise_orchestration/`
  - Workflow coordination
  - Provider abstractions
  - Performance monitoring

- **API Projects:** `/home/coolhand/projects/apis/`
  - Multi-provider API patterns
  - Authentication and OAuth
  - Streaming implementations

- **xAI Swarm:** `/home/coolhand/projects/xai_swarm/`
  - Swarm intelligence patterns
  - Real-time updates with SSE

- **Tools CLI:** `/home/coolhand/projects/WORKING/`
  - Interactive CLI tools
  - LLM integrations

### Maintained By

Luke Steuber (@lukesteuber)

### License

These snippets are extracted from open source and internal projects. Use them freely in your own projects. Attribution appreciated but not required.

---

## Index by Use Case

### Building AI Chatbots
- `api-clients/multi_provider_abstraction.py` - Provider switching
- `cli-tools/interactive_cli_with_llm.py` - Interactive chat interface
- `streaming-patterns/sse_streaming_responses.py` - Real-time streaming
- `configuration-management/multi_source_config.py` - API key management

### Creating Plugin Systems
- `tool-registration/swarm_module_pattern.py` - Auto-discovery
- `file-operations/module_discovery.py` - Dynamic module loading
- `error-handling/graceful_import_fallbacks.py` - Optional features
- `testing/pytest_fixtures_patterns.py` - Testing plugins

### Configuration Management
- `file-operations/config_file_loading.py` - Multi-format config loading
- `configuration-management/multi_source_config.py` - Hierarchical config
- `file-operations/path_handling_utils.py` - Path utilities

### Web Applications with AI
- `streaming-patterns/sse_streaming_responses.py` - SSE streaming
- `api-clients/multi_provider_abstraction.py` - Backend providers
- `configuration-management/multi_source_config.py` - Environment config

### Development Tools
- `cli-tools/interactive_cli_with_llm.py` - CLI applications
- `testing/pytest_fixtures_patterns.py` - Test suites
- `error-handling/graceful_import_fallbacks.py` - Dependency management

---

## Quick Reference: Common Patterns

### API Integration
```python
from api_clients.multi_provider_abstraction import ProviderFactory

provider = ProviderFactory.create("openai", api_key="...")
response = provider.generate("Your prompt here")
```

### Streaming Responses
```python
from streaming_patterns.sse_streaming_responses import flask_ai_streaming_example

app = flask_ai_streaming_example()
app.run()
```

### Configuration Loading
```python
from configuration_management.multi_source_config import ConfigurationManager

config = ConfigurationManager("myapp")
config.load_all(cli_args={"debug": True})
api_key = config.require("api_key")
```

### Interactive CLI
```python
from cli_tools.interactive_cli_with_llm import InteractiveCLI

cli = InteractiveCLI(api_key="...", model="grok-beta")
cli.run()
```

---

## Roadmap

### Planned Additions

- [ ] Agent orchestration patterns (Beltalowda hierarchical agents)
- [x] Async patterns (concurrent operations, context managers) - COMPLETED 2025-11-09
  - [x] Parallel task execution with progress tracking
  - [x] Async context managers for resource management
  - [x] Task cancellation and timeout handling
  - [x] Basic async LLM operations
- [ ] Async iterator patterns
- [ ] Event loop management patterns
- [ ] FastAPI application templates
- [ ] Data processing pipelines
- [x] File operations and format conversions - COMPLETED 2025-11-09
  - [x] Configuration file loading (JSON/YAML/.env)
  - [x] Path handling utilities (pathlib patterns)
  - [x] Dynamic module discovery and loading
- [ ] Accessibility compliance patterns
- [ ] Security and authentication patterns
- [ ] Caching and performance optimization
- [ ] Monitoring and observability

### Consolidation Targets

Directories to scan for additional snippets:
- `/home/coolhand/html/belta/` - Agent patterns
- `/home/coolhand/enterprise_orchestration/` - Workflow patterns
- `/home/coolhand/projects/tools_cli/` - CLI utilities
- `/home/coolhand/accessibility/` - Accessibility tools

---

## Support

For questions or issues with these snippets:

1. Check the snippet's documentation and usage examples
2. Review related snippets for alternative approaches
3. Consult the source files for additional context
4. Refer to project documentation in `/home/coolhand/CLAUDE.md`

---

**Remember:** These snippets are starting points. Always review, test, and adapt them for your specific use case. Security, error handling, and edge cases should be carefully considered for production use.
