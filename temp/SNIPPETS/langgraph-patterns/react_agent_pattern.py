#!/usr/bin/env python3
"""
LangGraph ReAct Agent Pattern

Description: Complete implementation pattern for a ReAct (Reasoning and Acting) agent
             using LangGraph with configurable LLM, tool binding, and conditional routing.

Use Cases:
- Building autonomous AI agents with tool use
- Research assistants that search and synthesize
- Task automation with multi-step reasoning
- Chatbots with external data access
- Question-answering systems with web search

Dependencies:
- langgraph (pip install langgraph)
- langchain-core (pip install langchain-core)
- langchain provider packages (e.g., langchain-anthropic, langchain-openai)

Notes:
- ReAct pattern: Model reasons about what tool to use, uses it, then continues
- Conditional routing: Model decides when to use tools vs. respond directly
- State management: Messages accumulate through conversation
- Configuration: Model and prompts configurable at runtime
- is_last_step: Safety mechanism to prevent infinite loops

Related Snippets:
- agent-orchestration/hierarchical_agent_coordination.py
- agent-orchestration/parallel_agent_execution.py

Source Attribution:
- Extracted from: /home/coolhand/inbox/hive/src/react_agent/
- Pattern: LangGraph ReAct Agent template
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from datetime import UTC, datetime
from typing import Annotated, Any, Callable, Dict, List, Literal, Optional, Sequence, cast

# LangGraph imports
try:
    from langchain_core.messages import AIMessage, AnyMessage
    from langchain_core.runnables import ensure_config
    from langgraph.config import get_config
    from langgraph.graph import StateGraph, add_messages
    from langgraph.managed import IsLastStep
    from langgraph.prebuilt import ToolNode
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    print("Warning: langgraph not installed. Install with: pip install langgraph langchain-core")


# =============================================================================
# STATE DEFINITIONS
# =============================================================================

@dataclass
class InputState:
    """
    Input state for the agent - the narrower interface to the outside world.

    This defines what the agent receives from users.
    """
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    """
    Messages tracking the conversation state.

    Pattern:
    1. HumanMessage - user input
    2. AIMessage with .tool_calls - agent picks tool(s)
    3. ToolMessage(s) - tool responses
    4. AIMessage without .tool_calls - agent responds to user
    5. HumanMessage - user continues conversation

    The `add_messages` annotation merges new messages with existing ones.
    """


@dataclass
class State(InputState):
    """
    Complete agent state, extending InputState with internal attributes.

    Add custom state attributes here for your agent's needs.
    """
    is_last_step: IsLastStep = field(default=False)
    """
    Managed variable indicating if this is the last step before recursion limit.
    Set to True when step count reaches recursion_limit - 1.
    """

    # Common extensions (uncomment as needed):
    # retrieved_documents: List[Any] = field(default_factory=list)
    # extracted_entities: Dict[str, Any] = field(default_factory=dict)
    # current_context: Optional[str] = None


# =============================================================================
# CONFIGURATION
# =============================================================================

# Default system prompt
DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant with access to tools.

Current time: {system_time}

Use the available tools to help answer questions. When you don't need tools,
respond directly to the user.

Be concise but thorough in your responses."""


@dataclass(kw_only=True)
class Configuration:
    """
    Agent configuration with runtime-configurable parameters.

    Pass configuration via the config dict when invoking the graph:
    graph.invoke({"messages": [...]}, config={"configurable": {"model": "..."}})
    """

    system_prompt: str = field(
        default=DEFAULT_SYSTEM_PROMPT,
        metadata={
            "description": "System prompt setting agent context and behavior."
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="anthropic/claude-3-5-sonnet-20240620",
        metadata={
            "description": "LLM model in format: provider/model-name"
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "Maximum search results to return per query."
        },
    )

    @classmethod
    def from_context(cls) -> Configuration:
        """Create Configuration from current LangGraph context."""
        try:
            config = get_config()
        except RuntimeError:
            config = None
        config = ensure_config(config)
        configurable = config.get("configurable") or {}
        _fields = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in _fields})


# =============================================================================
# TOOLS
# =============================================================================

def create_search_tool(max_results: int = 10) -> Callable:
    """
    Factory for creating a search tool.

    Replace this with your actual tool implementation.
    """
    async def search(query: str) -> Optional[Dict[str, Any]]:
        """
        Search for information.

        Args:
            query: Search query string

        Returns:
            Search results dictionary
        """
        # Example implementation - replace with actual search
        # For real use, integrate with Tavily, SerpAPI, or custom search
        return {
            "query": query,
            "results": [
                {"title": "Example Result", "content": f"Results for: {query}"}
            ],
            "total": 1
        }

    return search


# Default tools list - customize for your agent
def get_default_tools() -> List[Callable]:
    """Get default tools for the agent."""
    return [create_search_tool()]


# =============================================================================
# MODEL LOADING
# =============================================================================

def load_chat_model(model_string: str):
    """
    Load a chat model from a provider/model string.

    Args:
        model_string: Format "provider/model-name"

    Returns:
        Initialized chat model

    Supports: anthropic, openai, google-genai, mistral, cohere
    """
    provider, model_name = model_string.split("/", 1)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=model_name)

    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model_name)

    elif provider == "google-genai":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model_name)

    elif provider == "mistral":
        from langchain_mistralai import ChatMistralAI
        return ChatMistralAI(model=model_name)

    elif provider == "cohere":
        from langchain_cohere import ChatCohere
        return ChatCohere(model=model_name)

    else:
        raise ValueError(f"Unsupported provider: {provider}")


# =============================================================================
# GRAPH NODES
# =============================================================================

async def call_model(state: State, tools: List[Callable]) -> Dict[str, List[AIMessage]]:
    """
    Call the LLM with current state and tools.

    This is the main reasoning node of the agent.
    """
    configuration = Configuration.from_context()

    # Initialize model with tool binding
    model = load_chat_model(configuration.model).bind_tools(tools)

    # Format system prompt with current time
    system_message = configuration.system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )

    # Call the model
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages]
        ),
    )

    # Handle last step safety - prevent infinite tool loops
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="I wasn't able to complete the task in the allowed steps. "
                           "Please try a more specific question.",
                )
            ]
        }

    return {"messages": [response]}


def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """
    Determine next node based on model output.

    Routes to:
    - "tools" if model wants to use tools
    - "__end__" if model is ready to respond
    """
    last_message = state.messages[-1]

    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in routing, got {type(last_message).__name__}"
        )

    # No tool calls = ready to respond
    if not last_message.tool_calls:
        return "__end__"

    # Has tool calls = execute tools
    return "tools"


# =============================================================================
# GRAPH BUILDER
# =============================================================================

def build_react_agent(
    tools: Optional[List[Callable]] = None,
    name: str = "ReAct Agent"
) -> StateGraph:
    """
    Build a ReAct agent graph.

    Args:
        tools: List of tools for the agent (defaults to search)
        name: Name for the compiled graph

    Returns:
        Compiled StateGraph
    """
    if not LANGGRAPH_AVAILABLE:
        raise RuntimeError("langgraph not installed")

    tools = tools or get_default_tools()

    # Create the graph
    builder = StateGraph(State, input=InputState, config_schema=Configuration)

    # Add nodes
    builder.add_node(
        "call_model",
        lambda state: call_model(state, tools)
    )
    builder.add_node("tools", ToolNode(tools))

    # Set entry point
    builder.add_edge("__start__", "call_model")

    # Add conditional routing after model
    builder.add_conditional_edges(
        "call_model",
        route_model_output,
    )

    # Tools always return to model
    builder.add_edge("tools", "call_model")

    # Compile and return
    return builder.compile(name=name)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

async def run_agent(
    query: str,
    tools: Optional[List[Callable]] = None,
    model: str = "anthropic/claude-3-5-sonnet-20240620",
    max_steps: int = 10
) -> str:
    """
    Run the ReAct agent with a query.

    Args:
        query: User query
        tools: Optional tools list
        model: Model string (provider/model-name)
        max_steps: Maximum reasoning steps

    Returns:
        Agent's final response
    """
    graph = build_react_agent(tools=tools)

    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": query}]},
        config={
            "configurable": {"model": model},
            "recursion_limit": max_steps
        }
    )

    # Get last AI message
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage) and not msg.tool_calls:
            return msg.content

    return "No response generated"


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    import asyncio

    print("LangGraph ReAct Agent Pattern")
    print("=" * 50)

    if not LANGGRAPH_AVAILABLE:
        print("\nlanggraph not installed. Install with:")
        print("  pip install langgraph langchain-core langchain-anthropic")
        exit(1)

    async def demo():
        # Build the agent
        print("\n1. Building agent...")
        agent = build_react_agent(name="Demo Agent")
        print(f"   Agent created: {agent.name}")

        # Show the graph structure
        print("\n2. Graph structure:")
        print("   __start__ -> call_model")
        print("   call_model -> [tools | __end__] (conditional)")
        print("   tools -> call_model")

        # Example invocation (requires API keys)
        print("\n3. Example invocation:")
        print("   query = 'What is the weather in Tokyo?'")
        print("   result = await agent.ainvoke(")
        print("       {'messages': [{'role': 'user', 'content': query}]},")
        print("       config={'configurable': {'model': 'anthropic/claude-3-5-sonnet-20240620'}}")
        print("   )")

        # State structure
        print("\n4. State structure:")
        print("   InputState:")
        print("     - messages: List[AnyMessage]")
        print("   State(InputState):")
        print("     - is_last_step: bool (managed)")

        # Configuration
        print("\n5. Configuration options:")
        print("   - system_prompt: str")
        print("   - model: str (provider/model-name)")
        print("   - max_search_results: int")

    asyncio.run(demo())
