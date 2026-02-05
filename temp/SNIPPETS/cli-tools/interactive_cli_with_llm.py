"""
Interactive CLI with LLM Integration Pattern

Description: Comprehensive pattern for building interactive CLI chat interfaces
that integrate with LLM APIs. Supports streaming responses, conversation history,
tool calling, and graceful error handling.

Use Cases:
- Building ChatGPT-style CLI applications
- Creating AI-powered terminal tools
- Implementing REPL interfaces with AI
- Adding chat capabilities to existing CLI tools
- Testing LLM integrations interactively

Dependencies:
- openai (pip install openai) or provider-specific SDK
- json (built-in)
- sys (built-in)
- typing (built-in)
- readline (built-in) for command history

Notes:
- Use readline for command history and editing
- Implement proper signal handling (Ctrl+C)
- Stream responses for better UX
- Maintain conversation history for context
- Support multi-turn conversations
- Include special commands (/clear, /help, /exit)
- Handle network errors gracefully
- Display token usage if available
- Support tool/function calling

Related Snippets:
- /home/coolhand/SNIPPETS/api-clients/multi_provider_abstraction.py
- /home/coolhand/SNIPPETS/streaming-patterns/sse_streaming_responses.py
- /home/coolhand/SNIPPETS/tool-registration/swarm_module_pattern.py

Source Attribution:
- Extracted from: /home/coolhand/projects/swarm/hive/swarm_template.py
- Related: /home/coolhand/projects/WORKING/xai_tools.py
"""

import json
import os
import sys
import readline
from typing import Any, Dict, List, Optional
from datetime import datetime


# ============================================================================
# BASIC INTERACTIVE CLI
# ============================================================================

class InteractiveCLI:
    """
    Basic interactive CLI for LLM chat.

    Provides conversation management, history, and streaming.
    """

    def __init__(self,
                 api_key: str,
                 model: str = "grok-beta",
                 base_url: str = "https://api.x.ai/v1",
                 system_prompt: Optional[str] = None):
        """
        Initialize interactive CLI.

        Args:
            api_key: API key for the LLM provider
            model: Model to use
            base_url: API base URL
            system_prompt: Optional custom system prompt
        """
        from openai import OpenAI

        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

        # Initialize conversation history
        default_system = (
            "You are a helpful AI assistant. Provide clear, accurate, "
            "and concise responses. If you're unsure about something, "
            "say so rather than guessing."
        )

        self.conversation_history = [
            {"role": "system", "content": system_prompt or default_system}
        ]

        # Statistics
        self.message_count = 0
        self.total_tokens = 0

    def print_banner(self):
        """Print welcome banner."""
        print("\n" + "=" * 80)
        print("  INTERACTIVE AI CHAT")
        print("=" * 80)
        print(f"  Model: {self.model}")
        print(f"  Commands: /help, /clear, /history, /exit")
        print("=" * 80 + "\n")

    def print_help(self):
        """Print help information."""
        help_text = """
Available Commands:
  /help      - Show this help message
  /clear     - Clear conversation history
  /history   - Show conversation history
  /stats     - Show usage statistics
  /model     - Show current model
  /system    - Update system prompt
  /exit      - Exit the chat (or use Ctrl+D, Ctrl+C)

Tips:
  - Press Ctrl+C to interrupt streaming responses
  - Press Ctrl+D or type /exit to quit
  - Use up/down arrows to navigate command history
        """
        print(help_text)

    def print_history(self):
        """Print conversation history."""
        print("\nConversation History:")
        print("=" * 80)

        for i, msg in enumerate(self.conversation_history):
            role = msg["role"].upper()
            content = msg["content"]

            if role == "SYSTEM":
                continue  # Skip system messages

            print(f"\n[{i}] {role}:")
            print(content[:200] + "..." if len(content) > 200 else content)

        print("\n" + "=" * 80)

    def print_stats(self):
        """Print usage statistics."""
        print(f"\nStatistics:")
        print(f"  Messages: {self.message_count}")
        print(f"  Total tokens: {self.total_tokens}")
        print(f"  Conversation length: {len(self.conversation_history) - 1}")

    def handle_command(self, command: str) -> bool:
        """
        Handle special commands.

        Args:
            command: Command string (starting with /)

        Returns:
            True if command was handled, False to exit
        """
        command = command.lower().strip()

        if command == "/help":
            self.print_help()
        elif command == "/clear":
            system_msg = self.conversation_history[0]
            self.conversation_history = [system_msg]
            print("Conversation history cleared.")
        elif command == "/history":
            self.print_history()
        elif command == "/stats":
            self.print_stats()
        elif command == "/model":
            print(f"Current model: {self.model}")
        elif command == "/system":
            new_prompt = input("Enter new system prompt: ")
            self.conversation_history[0]["content"] = new_prompt
            print("System prompt updated.")
        elif command in ("/exit", "/quit", "/q"):
            return False
        else:
            print(f"Unknown command: {command}")
            print("Type /help for available commands")

        return True

    def chat_completion(self, user_message: str, stream: bool = True):
        """
        Send message and get response.

        Args:
            user_message: User's input message
            stream: Whether to stream the response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            if stream:
                self.stream_response()
            else:
                self.get_response()

            self.message_count += 1

        except KeyboardInterrupt:
            print("\n[Response interrupted]")
            # Remove incomplete assistant message if any
            if self.conversation_history[-1]["role"] == "assistant":
                self.conversation_history.pop()

        except Exception as e:
            print(f"\nError: {e}")
            # Remove user message on error
            self.conversation_history.pop()

    def stream_response(self):
        """Stream response from LLM."""
        print("\nAssistant: ", end="", flush=True)

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                stream=True,
                temperature=0.7
            )

            full_content = ""

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_content += content
                    print(content, end="", flush=True)

                # Track token usage if available
                if hasattr(chunk, 'usage') and chunk.usage:
                    self.total_tokens += chunk.usage.total_tokens

            print()  # Newline after streaming

            # Add complete assistant message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": full_content
            })

        except Exception as e:
            print(f"\n[Streaming error: {e}]")
            raise

    def get_response(self):
        """Get non-streaming response from LLM."""
        print("\nAssistant: ", end="", flush=True)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            temperature=0.7
        )

        content = response.choices[0].message.content
        print(content)

        # Track tokens
        if response.usage:
            self.total_tokens += response.usage.total_tokens

        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": content
        })

    def run(self):
        """Run the interactive CLI loop."""
        self.print_banner()

        try:
            while True:
                # Get user input
                try:
                    user_input = input("\nYou: ").strip()
                except EOFError:
                    # Ctrl+D pressed
                    print("\nGoodbye!")
                    break

                # Skip empty input
                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    if not self.handle_command(user_input):
                        print("\nGoodbye!")
                        break
                    continue

                # Process chat message
                self.chat_completion(user_input, stream=True)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")


# ============================================================================
# ADVANCED: CLI WITH TOOL CALLING
# ============================================================================

class ToolEnabledCLI(InteractiveCLI):
    """
    Interactive CLI with tool/function calling support.

    Extends basic CLI to support LLM tool calling.
    """

    def __init__(self,
                 api_key: str,
                 model: str = "grok-beta",
                 base_url: str = "https://api.x.ai/v1",
                 system_prompt: Optional[str] = None,
                 tools: Optional[List[Dict[str, Any]]] = None):
        """
        Initialize with tool support.

        Args:
            api_key: API key
            model: Model to use
            base_url: API base URL
            system_prompt: Optional system prompt
            tools: List of tool schemas (OpenAI function format)
        """
        super().__init__(api_key, model, base_url, system_prompt)

        self.tools = tools or []
        self.tool_handlers: Dict[str, callable] = {}

    def register_tool(self,
                     schema: Dict[str, Any],
                     handler: callable):
        """
        Register a tool with its handler.

        Args:
            schema: Tool schema in OpenAI function format
            handler: Function to call when tool is invoked
        """
        if "function" in schema:
            tool_name = schema["function"]["name"]
            self.tool_handlers[tool_name] = handler
            self.tools.append(schema)

    def print_banner(self):
        """Print welcome banner with available tools."""
        super().print_banner()

        if self.tools:
            print("Available Tools:")
            for tool in self.tools:
                name = tool["function"]["name"]
                desc = tool["function"].get("description", "")
                print(f"  - {name}: {desc}")
            print()

    def chat_completion(self, user_message: str, stream: bool = True):
        """
        Send message with tool calling support.

        Args:
            user_message: User input
            stream: Whether to stream (note: tool calls disable streaming)
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            # Create completion with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                tools=self.tools if self.tools else None,
                stream=False  # Tool calling doesn't support streaming
            )

            message = response.choices[0].message

            # Add assistant message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": message.tool_calls if hasattr(message, 'tool_calls') else None
            })

            # Print response
            if message.content:
                print(f"\nAssistant: {message.content}")

            # Handle tool calls
            if hasattr(message, 'tool_calls') and message.tool_calls:
                print("\n[Executing tools...]")
                tool_results = self.execute_tools(message.tool_calls)

                # Add tool results to conversation
                for result in tool_results:
                    self.conversation_history.append(result)

                # Get follow-up response with tool results
                follow_up = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history
                )

                final_message = follow_up.choices[0].message
                print(f"\nAssistant: {final_message.content}")

                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_message.content
                })

            self.message_count += 1

            if response.usage:
                self.total_tokens += response.usage.total_tokens

        except Exception as e:
            print(f"\nError: {e}")
            self.conversation_history.pop()  # Remove user message

    def execute_tools(self, tool_calls) -> List[Dict[str, Any]]:
        """
        Execute tool calls and return results.

        Args:
            tool_calls: List of tool call objects

        Returns:
            List of tool result messages
        """
        results = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"  Calling: {function_name}({arguments})")

            # Execute tool
            if function_name in self.tool_handlers:
                try:
                    result = self.tool_handlers[function_name](**arguments)
                    print(f"  Result: {result}")

                    results.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps(result)
                    })

                except Exception as e:
                    print(f"  Error: {e}")
                    results.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": json.dumps({"error": str(e)})
                    })
            else:
                print(f"  Unknown tool: {function_name}")

        return results


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: Basic CLI
    print("Basic Interactive CLI Example")
    print("=" * 80)

    # Get API key from environment
    api_key = os.getenv("XAI_API_KEY", "")
    if not api_key:
        print("Error: XAI_API_KEY environment variable not set")
        sys.exit(1)

    # Create and run CLI
    cli = InteractiveCLI(
        api_key=api_key,
        model="grok-beta",
        system_prompt="You are a helpful coding assistant."
    )

    # Run interactive loop
    cli.run()


def example_with_tools():
    """Example showing tool-enabled CLI."""

    # Define example tools
    def get_weather(location: str) -> dict:
        """Get weather for a location."""
        return {
            "location": location,
            "temperature": 72,
            "condition": "sunny"
        }

    def calculate(expression: str) -> dict:
        """Calculate a mathematical expression."""
        try:
            result = eval(expression, {"__builtins__": {}})
            return {"expression": expression, "result": result}
        except Exception as e:
            return {"error": str(e)}

    # Tool schemas
    weather_tool = {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    }

    calc_tool = {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression"
                    }
                },
                "required": ["expression"]
            }
        }
    }

    # Create CLI with tools
    api_key = os.getenv("XAI_API_KEY", "")
    cli = ToolEnabledCLI(api_key=api_key)

    # Register tools
    cli.register_tool(weather_tool, get_weather)
    cli.register_tool(calc_tool, calculate)

    # Run
    cli.run()
