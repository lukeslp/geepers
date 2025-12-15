"""
Multi-Provider Abstraction for Agent Communication

Description: Abstract base class pattern for unified LLM provider interface in multi-agent
systems. Enables agents to work with any LLM provider (OpenAI, Anthropic, Gemini, etc.)
through a consistent interface, facilitating provider switching and fallback strategies.

Use Cases:
- Building provider-agnostic multi-agent systems
- Implementing fallback mechanisms across different LLM providers
- A/B testing different providers in agent swarms
- Cost optimization by routing to cheaper providers
- Supporting multiple LLM vendors in enterprise systems

Dependencies:
- abc (for abstract base classes)
- typing (for type hints)
- pydantic (for data models)
- enum (for capability definitions)
- asyncio (for async operations)

Notes:
- All providers must implement the same core methods
- Supports both streaming and non-streaming responses
- Includes cost estimation for budget management
- Validates API keys before use
- Model capability detection enables smart routing
- Chat message format is provider-agnostic

Related Snippets:
- hierarchical_agent_coordination.py - Uses providers for agent execution
- agent_lifecycle_management.py - Validates provider in agent setup

Source Attribution:
- Extracted from: /home/coolhand/projects/beltalowda/src/beltalowda/providers/base.py
- Additional patterns from: providers/openai_adapter.py, providers/anthropic_adapter.py
- Original author: Luke Steuber
- Project: Beltalowda Multi-Agent Orchestration Platform
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, AsyncGenerator, Any
from pydantic import BaseModel
from enum import Enum
import asyncio


# ============================================================================
# CAPABILITY AND MODEL DEFINITIONS
# ============================================================================

class ModelCapability(str, Enum):
    """Enumeration of model capabilities"""
    TEXT = "text"
    VISION = "vision"
    FUNCTION_CALLING = "function_calling"
    IMAGE_GENERATION = "image_generation"
    WEB_SEARCH = "web_search"
    FILE_SEARCH = "file_search"
    CODE_EXECUTION = "code_execution"


class ModelInfo(BaseModel):
    """Model information and capabilities"""
    id: str
    name: str
    provider: str
    context_length: int
    description: str
    capabilities: List[ModelCapability]
    cost_per_1k_tokens: Optional[float] = None
    created: Optional[str] = None


class ChatMessage(BaseModel):
    """Standard chat message format"""
    role: str  # system, user, assistant
    content: Union[str, List[Dict[str, Any]]]  # text or multimodal content
    metadata: Optional[Dict[str, Any]] = None


class StreamingResponse(BaseModel):
    """Streaming response chunk from LLM"""
    content: str
    is_complete: bool = False
    metadata: Optional[Dict[str, Any]] = None
    usage: Optional[Dict[str, int]] = None


# ============================================================================
# PROVIDER ADAPTER BASE CLASS
# ============================================================================

class ProviderAdapter(ABC):
    """
    Abstract base class for all LLM provider adapters.

    All provider implementations must inherit from this class and implement
    the required methods to ensure consistent behavior across the platform.

    Key Design Principles:
    - Uniform interface across all providers
    - Async-first for non-blocking operations
    - Streaming support for real-time responses
    - Cost estimation for budget management
    - Capability detection for smart routing
    """

    def __init__(self, api_key: str, **kwargs):
        """
        Initialize the provider adapter with API key and optional config.

        Args:
            api_key: Provider API key
            **kwargs: Additional provider-specific configuration
        """
        self.api_key = api_key
        self.config = kwargs

    @abstractmethod
    async def list_models(self) -> List[ModelInfo]:
        """
        List available models for this provider.

        Returns:
            List of ModelInfo objects describing available models

        Example:
            models = await provider.list_models()
            for model in models:
                print(f"{model.name}: {model.capabilities}")
        """
        pass

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a single chat completion response.

        Args:
            messages: List of ChatMessage objects forming the conversation
            model: Model identifier to use
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Returns:
            Complete response text as string

        Example:
            messages = [
                ChatMessage(role="system", content="You are helpful."),
                ChatMessage(role="user", content="Hello!")
            ]
            response = await provider.chat_completion(
                messages=messages,
                model="gpt-4",
                temperature=0.7
            )
        """
        pass

    @abstractmethod
    async def chat_completion_stream(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[StreamingResponse, None]:
        """
        Generate a streaming chat completion response.

        Args:
            messages: List of ChatMessage objects
            model: Model identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Yields:
            StreamingResponse objects with incremental content

        Example:
            async for chunk in provider.chat_completion_stream(messages, "gpt-4"):
                print(chunk.content, end='', flush=True)
                if chunk.is_complete:
                    print(f"\nUsage: {chunk.usage}")
        """
        pass

    @abstractmethod
    async def supports_capability(self, model: str, capability: ModelCapability) -> bool:
        """
        Check if a model supports a specific capability.

        Args:
            model: Model identifier to check
            capability: Capability to verify

        Returns:
            True if model supports the capability, False otherwise

        Example:
            if await provider.supports_capability("gpt-4", ModelCapability.VISION):
                print("Model supports vision")
        """
        pass

    async def validate_api_key(self) -> bool:
        """
        Validate that the API key is working.

        Returns:
            True if API key is valid, False otherwise

        Note:
            Default implementation lists models with timeout.
            Override for provider-specific validation.
        """
        try:
            # Add timeout to prevent hanging on network issues
            models = await asyncio.wait_for(self.list_models(), timeout=5.0)
            return len(models) > 0
        except asyncio.TimeoutError:
            return False
        except Exception:
            return False

    def get_provider_name(self) -> str:
        """
        Get the provider name.

        Returns:
            Provider name as lowercase string

        Note:
            Default implementation derives name from class name.
            Override for custom naming.
        """
        return self.__class__.__name__.replace("Adapter", "").lower()

    async def estimate_cost(
        self,
        messages: List[ChatMessage],
        model: str,
        max_tokens: Optional[int] = None
    ) -> float:
        """
        Estimate the cost for a given request.

        Args:
            messages: Messages to estimate cost for
            model: Model to use
            max_tokens: Maximum tokens to generate

        Returns:
            Estimated cost in USD

        Note:
            Default implementation returns 0.0.
            Override with actual pricing logic for the provider.
        """
        return 0.0


# ============================================================================
# EXAMPLE: MOCK PROVIDER IMPLEMENTATION
# ============================================================================

class MockProviderAdapter(ProviderAdapter):
    """
    Mock provider for testing and demonstration.

    Implements all required methods with simulated behavior.
    """

    async def list_models(self) -> List[ModelInfo]:
        """List mock models"""
        return [
            ModelInfo(
                id="mock-gpt-4",
                name="Mock GPT-4",
                provider="mock",
                context_length=8192,
                description="Mock GPT-4 model for testing",
                capabilities=[
                    ModelCapability.TEXT,
                    ModelCapability.VISION,
                    ModelCapability.FUNCTION_CALLING
                ],
                cost_per_1k_tokens=0.03
            ),
            ModelInfo(
                id="mock-claude",
                name="Mock Claude",
                provider="mock",
                context_length=200000,
                description="Mock Claude model for testing",
                capabilities=[
                    ModelCapability.TEXT,
                    ModelCapability.VISION
                ],
                cost_per_1k_tokens=0.015
            )
        ]

    async def chat_completion(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate mock completion"""
        # Simulate API delay
        await asyncio.sleep(0.1)

        # Extract last user message
        last_message = messages[-1].content if messages else "No message"

        return f"Mock response to: {last_message[:100]}"

    async def chat_completion_stream(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[StreamingResponse, None]:
        """Generate mock streaming response"""
        response_text = "This is a mock streaming response."
        words = response_text.split()

        for i, word in enumerate(words):
            await asyncio.sleep(0.05)
            yield StreamingResponse(
                content=word + " ",
                is_complete=(i == len(words) - 1),
                metadata={"word_index": i}
            )

    async def supports_capability(self, model: str, capability: ModelCapability) -> bool:
        """Check mock capability support"""
        models = await self.list_models()

        for m in models:
            if m.id == model:
                return capability in m.capabilities

        return False

    async def estimate_cost(
        self,
        messages: List[ChatMessage],
        model: str,
        max_tokens: Optional[int] = None
    ) -> float:
        """Estimate mock cost"""
        # Simple estimation: count tokens in messages
        total_chars = sum(len(str(m.content)) for m in messages)
        estimated_tokens = total_chars // 4  # Rough estimate

        # Get model info
        models = await self.list_models()
        cost_per_1k = 0.01  # Default

        for m in models:
            if m.id == model:
                cost_per_1k = m.cost_per_1k_tokens or 0.01
                break

        return (estimated_tokens / 1000) * cost_per_1k


# ============================================================================
# PROVIDER FACTORY
# ============================================================================

class ProviderFactory:
    """
    Factory for creating provider instances.

    Centralizes provider instantiation and configuration.
    """

    # Registry of available providers
    _providers: Dict[str, type] = {}

    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """
        Register a provider class.

        Args:
            name: Provider name
            provider_class: Provider class to register
        """
        cls._providers[name] = provider_class

    @classmethod
    def create(cls, provider_name: str, api_key: str, **config) -> ProviderAdapter:
        """
        Create a provider instance.

        Args:
            provider_name: Name of provider to create
            api_key: API key for the provider
            **config: Additional configuration

        Returns:
            Provider adapter instance

        Raises:
            ValueError: If provider not found
        """
        if provider_name not in cls._providers:
            raise ValueError(f"Provider '{provider_name}' not found. Available: {list(cls._providers.keys())}")

        provider_class = cls._providers[provider_name]
        return provider_class(api_key=api_key, **config)

    @classmethod
    def list_providers(cls) -> List[str]:
        """List all registered providers"""
        return list(cls._providers.keys())


# Register mock provider
ProviderFactory.register_provider("mock", MockProviderAdapter)


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    async def example_basic_usage():
        """Basic provider usage"""
        print("Example 1: Basic Provider Usage")
        print("=" * 60)

        # Create provider
        provider = ProviderFactory.create("mock", api_key="mock-key")

        # Validate API key
        is_valid = await provider.validate_api_key()
        print(f"API Key Valid: {is_valid}")

        # List models
        models = await provider.list_models()
        print(f"\nAvailable Models:")
        for model in models:
            print(f"  - {model.name} ({model.context_length} context)")
            print(f"    Capabilities: {[c.value for c in model.capabilities]}")

        # Check capability
        supports_vision = await provider.supports_capability(
            "mock-gpt-4",
            ModelCapability.VISION
        )
        print(f"\nMock GPT-4 supports vision: {supports_vision}")

    async def example_completion():
        """Chat completion example"""
        print("\n\nExample 2: Chat Completion")
        print("=" * 60)

        provider = ProviderFactory.create("mock", api_key="mock-key")

        messages = [
            ChatMessage(role="system", content="You are a helpful assistant."),
            ChatMessage(role="user", content="What is the capital of France?")
        ]

        # Estimate cost
        cost = await provider.estimate_cost(messages, "mock-gpt-4")
        print(f"Estimated cost: ${cost:.6f}")

        # Get completion
        response = await provider.chat_completion(
            messages=messages,
            model="mock-gpt-4",
            temperature=0.7
        )

        print(f"\nResponse: {response}")

    async def example_streaming():
        """Streaming completion example"""
        print("\n\nExample 3: Streaming Completion")
        print("=" * 60)

        provider = ProviderFactory.create("mock", api_key="mock-key")

        messages = [
            ChatMessage(role="user", content="Tell me a story")
        ]

        print("Streaming response: ", end='', flush=True)

        async for chunk in provider.chat_completion_stream(
            messages=messages,
            model="mock-claude"
        ):
            print(chunk.content, end='', flush=True)
            if chunk.is_complete:
                print(f"\n\nStream complete!")

    # Run all examples
    async def main():
        await example_basic_usage()
        await example_completion()
        await example_streaming()

    asyncio.run(main())
