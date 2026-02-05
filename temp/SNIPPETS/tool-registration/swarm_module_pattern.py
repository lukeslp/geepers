"""
Swarm Module Pattern - Dynamic Tool Registration

Description: A comprehensive pattern for creating dynamically discoverable and
registerable tool modules. This pattern allows tools to be automatically discovered,
validated, and integrated into larger systems without manual configuration.

Use Cases:
- Building plugin architectures for AI agents
- Creating modular tool systems for LLMs
- Implementing auto-discovery of capabilities
- Organizing tools by functional domain
- Creating reusable tool modules that work standalone or integrated

Dependencies:
- json (built-in)
- sys (built-in)
- argparse (built-in)
- typing (built-in)
- pathlib (built-in)

Notes:
- Modules should work both standalone (CLI) and when imported
- Each module exports TOOL_SCHEMAS for automatic discovery
- Tools are mapped to implementation functions via TOOL_IMPLEMENTATIONS dict
- The handle_tool_calls() function provides standardized tool execution
- Modules auto-register when imported (not when run as __main__)
- Include comprehensive error handling and fallback modes

Related Snippets:
- /home/coolhand/SNIPPETS/api-clients/multi_provider_abstraction.py
- /home/coolhand/SNIPPETS/cli-tools/interactive_cli_pattern.py
- /home/coolhand/SNIPPETS/error-handling/graceful_import_fallbacks.py

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/hive/swarm_template.py
- Pattern used across: /home/coolhand/projects/swarm/hive/swarm_*.py modules
"""

import json
import sys
import argparse
import traceback
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


def get(attr: str, default=None):
    """
    Utility function to get attributes from this module.
    Used by registry system when organizing tools.

    Args:
        attr: Attribute name to get
        default: Default value if attribute doesn't exist

    Returns:
        Attribute value or default
    """
    module = sys.modules[__name__]
    return getattr(module, attr, default)


# --- Path Handling for Both Standalone and Imported Modes ---

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Add project root to sys.path if needed
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --- Core Module Configuration ---

MODULE_NAME = "example_tools"
MODULE_DESCRIPTION = "Example tool module demonstrating the swarm pattern"


# --- Tool Function Implementations ---

def search_web(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Example web search tool implementation.

    Args:
        query: Search query string
        limit: Maximum number of results to return

    Returns:
        Dictionary with search results
    """
    try:
        # Mock implementation - replace with actual search logic
        results = [
            {
                "title": f"Result {i+1} for: {query}",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"This is a snippet for result {i+1}"
            }
            for i in range(min(limit, 3))
        ]

        return {
            "success": True,
            "query": query,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "query": query
        }


def calculate(expression: str) -> Dict[str, Any]:
    """
    Safe mathematical expression evaluator.

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        Dictionary with calculation result
    """
    try:
        # Security: only allow safe characters
        safe_chars = set("0123456789+-*/() .")
        if not all(c in safe_chars for c in expression):
            return {
                "success": False,
                "error": "Expression contains invalid characters",
                "expression": expression
            }

        # Evaluate in restricted environment
        result = eval(expression, {"__builtins__": {}})

        return {
            "success": True,
            "expression": expression,
            "result": result
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "expression": expression
        }


def analyze_text(text: str, analysis_type: str = "sentiment") -> Dict[str, Any]:
    """
    Example text analysis tool.

    Args:
        text: Text to analyze
        analysis_type: Type of analysis (sentiment, entities, summary)

    Returns:
        Dictionary with analysis results
    """
    try:
        # Mock implementation
        results = {
            "sentiment": {"score": 0.8, "label": "positive"},
            "entities": ["example", "entity"],
            "summary": f"Summary of: {text[:50]}..."
        }

        return {
            "success": True,
            "text": text,
            "analysis_type": analysis_type,
            "result": results.get(analysis_type, {})
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": text
        }


# --- Tool Schema Definitions (OpenAI Function Format) ---

def get_tool_schemas() -> List[Dict[str, Any]]:
    """
    Return tool schemas in OpenAI function calling format.

    These schemas define the interface for each tool, including
    parameters, types, and descriptions for LLM understanding.

    Returns:
        List of tool schema dictionaries
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the web for information on a given topic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 5)",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Evaluate a mathematical expression",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression (e.g., '2 + 2 * 3')"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "analyze_text",
                "description": "Analyze text for sentiment, entities, or generate summary",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to analyze"
                        },
                        "analysis_type": {
                            "type": "string",
                            "enum": ["sentiment", "entities", "summary"],
                            "description": "Type of analysis to perform",
                            "default": "sentiment"
                        }
                    },
                    "required": ["text"]
                }
            }
        }
    ]


# Export for automatic discovery
TOOL_SCHEMAS = get_tool_schemas()


# --- Tool Implementation Mapping ---

TOOL_IMPLEMENTATIONS: Dict[str, Callable] = {
    "search_web": search_web,
    "calculate": calculate,
    "analyze_text": analyze_text
}


# --- Tool Call Handler ---

def handle_tool_calls(tool_calls: List[Dict[str, Any]],
                     config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Handle tool calls from LLM in standardized format.

    Args:
        tool_calls: List of tool call objects from LLM
        config: Optional configuration dictionary

    Returns:
        List of standardized tool response objects
    """
    results = []
    config = config or {}

    for call in tool_calls:
        tool_call_id = call.get("id", "")
        function = call.get("function", {})
        name = function.get("name", "")

        # Extract parameters (handle both 'parameters' and 'arguments' keys)
        params = function.get("parameters", {})
        if not params and "arguments" in function:
            try:
                arguments = function.get("arguments", "{}")
                if isinstance(arguments, str):
                    params = json.loads(arguments)
                else:
                    params = arguments
            except json.JSONDecodeError:
                params = {}

        # Validate tool exists
        if name not in TOOL_IMPLEMENTATIONS:
            error_msg = f"Unknown tool: {name}"
            results.append({
                "tool_call_id": tool_call_id,
                "role": "tool",
                "name": MODULE_NAME,
                "content": json.dumps({"error": error_msg})
            })
            continue

        # Execute tool
        try:
            tool_func = TOOL_IMPLEMENTATIONS[name]
            result = tool_func(**params)

            results.append({
                "tool_call_id": tool_call_id,
                "role": "tool",
                "name": name,
                "content": json.dumps(result) if isinstance(result, dict) else str(result)
            })

        except Exception as e:
            error_msg = f"Error executing {name}: {str(e)}"
            results.append({
                "tool_call_id": tool_call_id,
                "role": "tool",
                "name": name,
                "content": json.dumps({"error": error_msg})
            })

            if "--debug" in sys.argv:
                traceback.print_exc()

    return results


# --- Registry Integration ---

def register_with_registry():
    """
    Register all tools with the central tool registry.

    This function is called automatically when the module is imported
    (but not when run as __main__).
    """
    try:
        # Import registry - this may not be available in standalone mode
        from core.core_registry import get_registry

        registry = get_registry()

        # Register each tool with the registry
        for schema in get_tool_schemas():
            if isinstance(schema, dict) and "function" in schema:
                tool_name = schema["function"]["name"]

                # Create handler adapter for this specific tool
                def create_handler(name=tool_name):
                    def handler_adapter(args):
                        tool_call = {
                            "id": "direct_call",
                            "function": {
                                "name": name,
                                "arguments": json.dumps(args) if isinstance(args, dict) else args
                            }
                        }
                        results = handle_tool_calls([tool_call])

                        if results and len(results) > 0:
                            result = results[0]
                            content = result.get("content", "{}")
                            if isinstance(content, str):
                                try:
                                    return json.loads(content)
                                except:
                                    return content
                            return content

                        return {"error": "No result from tool call"}

                    return handler_adapter

                # Register tool
                registry.register_tool(
                    name=tool_name,
                    schema=schema,
                    handler=create_handler(),
                    module_name=MODULE_NAME
                )

        # Register the module itself
        registry.register_module(MODULE_NAME, sys.modules[__name__])

        return True

    except Exception as e:
        print(f"Warning: Failed to register tools with registry: {e}")
        if "--debug" in sys.argv:
            traceback.print_exc()

    return False


# --- CLI Entry Point ---

def main():
    """Command-line interface for testing this module."""
    parser = argparse.ArgumentParser(description=MODULE_DESCRIPTION)
    parser.add_argument("--test", action="store_true",
                       help="Run module tests")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug output")

    args = parser.parse_args()

    print(f"\n{'=' * 80}")
    print(f"{MODULE_NAME}")
    print(f"{'=' * 80}")
    print(f"{MODULE_DESCRIPTION}")
    print(f"{'=' * 80}\n")

    if args.test:
        print("Running tool tests...\n")

        # Test search_web
        print("[search_web] test:")
        result = search_web("test query", limit=3)
        print(json.dumps(result, indent=2))

        # Test calculate
        print("\n[calculate] test:")
        result = calculate("2 + 2 * 3")
        print(json.dumps(result, indent=2))

        # Test analyze_text
        print("\n[analyze_text] test:")
        result = analyze_text("This is a great example!", "sentiment")
        print(json.dumps(result, indent=2))

        print("\n[Tool tests complete]")
        return 0

    print("Use --test to run module tests")
    return 0


# --- Auto-registration when imported ---
if __name__ != "__main__":
    register_with_registry()


# --- Main entry point ---
if __name__ == "__main__":
    sys.exit(main())
