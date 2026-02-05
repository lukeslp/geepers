"""
Hybrid Free/API Provider Pattern

Description: Automatically detect execution environment and use free service
when available (e.g., Claude Code's built-in instance), fall back to paid API
when running standalone. Eliminates API costs when in supported environments.

Use Cases:
- Development tools that work both locally and in Claude Code
- Cost-free prototyping in supported environments
- Educational projects with API key fallback
- Testing workflows that auto-switch contexts
- Multi-environment orchestrators

Dependencies:
- Python 3.8+ (uses typing hints)
- os module for environment detection
- Parent API provider class (e.g., AnthropicProvider)

Notes:
- Zero API costs when running in Claude Code
- Transparent fallback to API when standalone
- Same code works in both contexts
- Set CLAUDE_CODE=1 environment variable to enable
- Can extend pattern to other hybrid contexts (VS Code, Cursor, etc.)

Related Snippets:
- /api-clients/llm_provider_factory.py
- /configuration-management/environment_detection.py
- /utilities/cost_tracking.py

Cost Savings:
    Claude Code context: $0 per call (uses built-in instance)
    Standalone context: Standard API pricing
"""

import os
from typing import Optional, Dict, List, Any


class HybridProviderPattern:
    """
    Base pattern for providers that can use free services when available.

    Detects execution context and routes to appropriate backend:
    - Free service if available (Claude Code, VS Code extension, etc.)
    - Paid API if standalone

    Inherit from this class and implement _call_via_free_service()
    """

    def __init__(self, api_key: Optional[str] = None, free_service_env_var: str = 'CLAUDE_CODE'):
        """
        Initialize hybrid provider.

        Args:
            api_key: API key for fallback mode (optional if always in free context)
            free_service_env_var: Environment variable indicating free service availability
        """
        self.api_key = api_key
        self.free_service_env_var = free_service_env_var
        self.in_free_context = self._detect_free_context()

    def _detect_free_context(self) -> bool:
        """
        Detect if running in free service context.

        Override this method for custom detection logic.

        Returns:
            True if in free context, False if standalone
        """
        # Check environment variable
        if os.getenv(self.free_service_env_var):
            return True

        # Add additional detection logic here
        # Examples:
        # - Check for specific files/directories
        # - Test for tool availability
        # - Check parent process name

        return False

    def get_mode(self) -> str:
        """
        Get current operating mode.

        Returns:
            'free' or 'api'
        """
        return 'free' if self.in_free_context else 'api'

    def get_cost_info(self) -> Dict[str, Any]:
        """
        Get cost information for current mode.

        Returns:
            Dict with mode, cost details, and notes
        """
        if self.in_free_context:
            return {
                'mode': 'free',
                'cost_per_call': 0.0,
                'notes': 'Using free service instance - no API costs'
            }
        else:
            return {
                'mode': 'api',
                'cost_per_call': 'varies',
                'notes': 'Using paid API - standard pricing applies'
            }


class ClaudeCodeProvider(HybridProviderPattern):
    """
    Example: Claude provider that uses Claude Code when available.

    Demonstrates the hybrid pattern with Anthropic's Claude.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude Code provider.

        Args:
            api_key: Anthropic API key (only needed for standalone mode)
        """
        super().__init__(api_key, free_service_env_var='CLAUDE_CODE')
        self.provider_name = 'anthropic'

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        **kwargs
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
        if self.in_free_context:
            return await self._chat_via_claude_code(messages, **kwargs)
        else:
            return await self._chat_via_api(messages, model=model, **kwargs)

    async def _chat_via_claude_code(
        self,
        messages: List[Dict[str, Any]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute chat via Claude Code's built-in instance.

        This is a conceptual implementation - in practice, you would
        structure this as a proper agent invocation or tool call.

        Args:
            messages: Message list
            **kwargs: Additional parameters

        Returns:
            Response dict
        """
        # Convert messages to prompt
        prompt = self._messages_to_prompt(messages)

        # In actual implementation, this would use the Task tool or similar
        # For example:
        # 1. Format the request for Claude Code
        # 2. Use Task tool to invoke Claude Code
        # 3. Parse the response

        # Placeholder - implement based on Claude Code integration specifics
        raise NotImplementedError(
            "Claude Code integration requires Task tool setup. "
            "Falling back to API mode."
        )

    async def _chat_via_api(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute chat via Anthropic API.

        Args:
            messages: Message list
            model: Model name
            **kwargs: Additional parameters

        Returns:
            Response dict
        """
        # Import Anthropic provider (or implement API call directly)
        from anthropic import AsyncAnthropic

        if not self.api_key:
            raise ValueError("API key required for standalone mode")

        client = AsyncAnthropic(api_key=self.api_key)

        # Call API
        response = await client.messages.create(
            model=model or "claude-3-5-sonnet-20241022",
            messages=messages,
            **kwargs
        )

        return {
            'content': response.content[0].text,
            'model': response.model,
            'usage': {
                'prompt_tokens': response.usage.input_tokens,
                'completion_tokens': response.usage.output_tokens,
                'total_tokens': response.usage.input_tokens + response.usage.output_tokens
            }
        }

    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """Convert message list to single prompt string."""
        parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            parts.append(f"{role.upper()}: {content}")
        return "\n\n".join(parts)


# Generic template for other hybrid providers
class GenericHybridProvider(HybridProviderPattern):
    """
    Template for creating hybrid providers.

    Copy this class and customize for your use case.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        free_service_env_var: str = 'MY_FREE_SERVICE',
        provider_name: str = 'generic'
    ):
        super().__init__(api_key, free_service_env_var)
        self.provider_name = provider_name

    async def execute_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute request with automatic context routing.

        Args:
            request_data: Request data dict

        Returns:
            Response dict
        """
        if self.in_free_context:
            return await self._execute_via_free_service(request_data)
        else:
            return await self._execute_via_api(request_data)

    async def _execute_via_free_service(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implement free service execution logic here."""
        raise NotImplementedError("Implement free service logic")

    async def _execute_via_api(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implement API execution logic here."""
        raise NotImplementedError("Implement API logic")


# Factory function for convenience
def create_hybrid_provider(
    provider_type: str,
    api_key: Optional[str] = None,
    free_service_env_var: Optional[str] = None
) -> HybridProviderPattern:
    """
    Create hybrid provider with automatic mode detection.

    Args:
        provider_type: Type of provider ('claude', 'generic')
        api_key: Optional API key for fallback mode
        free_service_env_var: Optional custom environment variable

    Returns:
        HybridProviderPattern instance

    Example:
        # Create Claude Code provider
        provider = create_hybrid_provider('claude', api_key='sk-ant-...')
        print(f"Running in {provider.get_mode()} mode")
        print(f"Cost info: {provider.get_cost_info()}")

        # Use the provider
        response = await provider.chat([
            {"role": "user", "content": "Hello!"}
        ])
    """
    if provider_type == 'claude':
        return ClaudeCodeProvider(api_key)
    elif provider_type == 'generic':
        env_var = free_service_env_var or 'FREE_SERVICE'
        return GenericHybridProvider(api_key, env_var)
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")


if __name__ == "__main__":
    # Usage examples
    import asyncio

    async def example_usage():
        # Example 1: Check current mode
        provider = create_hybrid_provider('claude', api_key='sk-ant-test')
        print(f"Mode: {provider.get_mode()}")
        print(f"Cost info: {provider.get_cost_info()}")

        # Example 2: Set environment variable to enable free mode
        os.environ['CLAUDE_CODE'] = '1'
        provider2 = create_hybrid_provider('claude')
        print(f"\nAfter setting CLAUDE_CODE=1:")
        print(f"Mode: {provider2.get_mode()}")
        print(f"Cost info: {provider2.get_cost_info()}")

        # Example 3: Custom detection logic
        class CustomHybridProvider(HybridProviderPattern):
            def _detect_free_context(self) -> bool:
                # Custom detection: check if running in Docker
                return os.path.exists('/.dockerenv')

        custom = CustomHybridProvider(api_key='test')
        print(f"\nCustom detection (Docker check):")
        print(f"Mode: {custom.get_mode()}")

    # Run examples
    # asyncio.run(example_usage())
