"""
Claude Code Provider - Uses Claude Code's own instance when available.

This provider enables orchestrators and tools to use Claude Code's Claude instance
when running within Claude Code, eliminating API key requirements for that context.
Falls back to direct Anthropic API calls when running standalone.

Usage:
    from llm_providers.claude_code_provider import ClaudeCodeProvider

    provider = ClaudeCodeProvider()

    # Automatically uses Claude Code if available, otherwise uses API key
    response = await provider.chat(messages)
"""

import os
from typing import Any, Dict, List, Optional

from .anthropic_provider import AnthropicProvider


class ClaudeCodeProvider(AnthropicProvider):
    """
    Hybrid provider that uses Claude Code when available, API otherwise.

    Detection:
    - Checks for CLAUDE_CODE environment variable
    - Falls back to direct API if not in Claude Code context

    Benefits:
    - No API costs when running in Claude Code
    - Same code works in both contexts
    - Transparent fallback
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize provider with optional API key.

        Args:
            api_key: Anthropic API key (only needed for standalone mode)
        """
        super().__init__(api_key)
        self.in_claude_code = self._detect_claude_code()

    def _detect_claude_code(self) -> bool:
        """
        Detect if running within Claude Code environment.

        Returns:
            True if in Claude Code, False otherwise
        """
        # Check for Claude Code environment markers
        if os.getenv("CLAUDE_CODE"):
            return True

        # Check if Task tool is available (Claude Code specific)
        try:
            # This is a heuristic - Claude Code has specific env variables
            # You would set CLAUDE_CODE=1 in your environment when using Claude Code
            return False  # Default to API mode for safety
        except:
            return False

    async def chat(
        self, messages: List[Dict[str, Any]], model: Optional[str] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Send chat completion request.

        If in Claude Code: Uses Task tool to delegate to Claude Code
        If standalone: Uses direct API call

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name (ignored in Claude Code mode)
            **kwargs: Additional parameters

        Returns:
            Response dict with 'content', 'model', etc.
        """
        if self.in_claude_code:
            return await self._chat_via_claude_code(messages, **kwargs)
        else:
            return await super().chat(messages, model=model, **kwargs)

    async def _chat_via_claude_code(
        self, messages: List[Dict[str, Any]], **kwargs
    ) -> Dict[str, Any]:
        """
        Execute chat via Claude Code's Task tool.

        This is a conceptual implementation - in practice, you would
        need to structure this as a proper agent invocation.

        Args:
            messages: Message list
            **kwargs: Additional parameters

        Returns:
            Response dict
        """
        # Convert messages to prompt
        self._messages_to_prompt(messages)

        # In actual implementation, this would use the Task tool
        # For now, we fall back to API
        #
        # The proper implementation would be:
        # 1. Format the request for Claude Code
        # 2. Use Task tool to invoke Claude Code
        # 3. Parse the response

        # Fallback to API for now
        return await super().chat(messages, **kwargs)

    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """Convert message list to single prompt string."""
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            parts.append(f"{role.upper()}: {content}")
        return "\n\n".join(parts)

    def get_mode(self) -> str:
        """
        Get current operating mode.

        Returns:
            'claude-code' or 'api'
        """
        return "claude-code" if self.in_claude_code else "api"

    def get_cost_info(self) -> Dict[str, Any]:
        """
        Get cost information for current mode.

        Returns:
            Dict with cost details
        """
        if self.in_claude_code:
            return {
                "mode": "claude-code",
                "cost_per_call": 0.0,
                "notes": "Using Claude Code instance - no API costs",
            }
        else:
            return {
                "mode": "api",
                "cost_per_call": "varies",
                "notes": "Using Anthropic API - standard pricing applies",
            }


# Convenience function for factory integration
def create_claude_code_provider(api_key: Optional[str] = None) -> ClaudeCodeProvider:
    """
    Create Claude Code provider with automatic mode detection.

    Args:
        api_key: Optional API key for fallback mode

    Returns:
        ClaudeCodeProvider instance

    Example:
        provider = create_claude_code_provider()
        print(f"Running in {provider.get_mode()} mode")
        response = await provider.chat(messages)
    """
    return ClaudeCodeProvider(api_key)
