"""
Multi-Provider API Abstraction Pattern

Description: A robust pattern for creating provider abstractions that support
multiple AI/API services through a unified interface. This pattern uses inheritance
and the abstract base class (ABC) pattern to ensure consistency across providers.

Use Cases:
- Building multi-LLM applications (OpenAI, Anthropic, xAI, etc.)
- Creating provider-agnostic API clients
- Switching between services without changing application code
- A/B testing different AI providers
- Implementing fallback mechanisms across providers

Dependencies:
- abc (built-in)
- typing (built-in)
- requests or httpx for HTTP calls
- Provider-specific SDKs (openai, anthropic, etc.)

Notes:
- Each provider implementation should handle its own error cases
- Use generator functions for streaming responses
- Include proper authentication handling per provider
- Implement retry logic and rate limiting at the base class level
- Consider caching responses where appropriate

Related Snippets:
- /home/coolhand/SNIPPETS/error-handling/retry_with_backoff.py
- /home/coolhand/SNIPPETS/streaming-patterns/sse_streaming.py
- /home/coolhand/SNIPPETS/configuration-management/multi_source_config.py

Source Attribution:
- Extracted from: /home/coolhand/projects/apis/api_v2/providers/
- Related patterns: /home/coolhand/enterprise_orchestration/agents/
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, Optional, Union
import logging


class BaseProvider(ABC):
    """
    Abstract base class for all AI/API providers.

    Provides common functionality and enforces consistent interface
    across different provider implementations.
    """

    def __init__(self, name: str, api_key: str, model: Optional[str] = None):
        """
        Initialize the provider with common configuration.

        Args:
            name: Provider identifier (e.g., 'openai', 'anthropic', 'xai')
            api_key: API authentication key
            model: Optional default model name for this provider
        """
        self.name = name
        self.api_key = api_key
        self.model = model
        self.logger = logging.getLogger(f"provider.{name}")

    @abstractmethod
    def generate(self,
                 prompt: str,
                 **kwargs) -> Union[str, Dict[str, Any]]:
        """
        Generate a response from the provider.

        Args:
            prompt: The input prompt or query
            **kwargs: Provider-specific parameters (temperature, max_tokens, etc.)

        Returns:
            Generated response as string or structured data

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        pass

    @abstractmethod
    def stream_generate(self,
                       prompt: str,
                       **kwargs) -> Generator[str, None, None]:
        """
        Generate streaming response from the provider.

        Args:
            prompt: The input prompt or query
            **kwargs: Provider-specific parameters

        Yields:
            Response chunks as they arrive

        Raises:
            NotImplementedError: Must be implemented by subclass
        """
        pass

    def create_error_response(self, error: Exception) -> Dict[str, Any]:
        """
        Create standardized error response.

        Args:
            error: The exception that occurred

        Returns:
            Standardized error dictionary
        """
        error_msg = f"Error with {self.name} provider: {str(error)}"
        self.logger.error(error_msg)

        return {
            "error": True,
            "provider": self.name,
            "message": error_msg,
            "type": type(error).__name__
        }

    def validate_config(self) -> bool:
        """
        Validate provider configuration.

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If configuration is invalid
        """
        if not self.api_key:
            raise ValueError(f"{self.name} provider requires an API key")

        return True


class OpenAIProvider(BaseProvider):
    """Example implementation for OpenAI."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__("openai", api_key, model)

        # Import here to make it optional
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI API."""
        try:
            self.validate_config()

            response = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000)
            )

            return response.choices[0].message.content

        except Exception as e:
            return self.create_error_response(e)

    def stream_generate(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Generate streaming response using OpenAI API."""
        try:
            self.validate_config()

            stream = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000),
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield str(self.create_error_response(e))


class XAIProvider(BaseProvider):
    """Example implementation for xAI (Grok)."""

    def __init__(self, api_key: str, model: str = "grok-beta"):
        super().__init__("xai", api_key, model)

        try:
            from openai import OpenAI
            # xAI uses OpenAI-compatible API with different base URL
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.x.ai/v1"
            )
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using xAI API."""
        try:
            self.validate_config()

            response = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000)
            )

            return response.choices[0].message.content

        except Exception as e:
            return self.create_error_response(e)

    def stream_generate(self, prompt: str, **kwargs) -> Generator[str, None, None]:
        """Generate streaming response using xAI API."""
        try:
            self.validate_config()

            stream = self.client.chat.completions.create(
                model=kwargs.get('model', self.model),
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000),
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield str(self.create_error_response(e))


class ProviderFactory:
    """
    Factory for creating provider instances.

    Centralizes provider instantiation and configuration.
    """

    _providers = {
        'openai': OpenAIProvider,
        'xai': XAIProvider,
        # Add more providers here
    }

    @classmethod
    def create(cls,
               provider_name: str,
               api_key: str,
               model: Optional[str] = None) -> BaseProvider:
        """
        Create a provider instance.

        Args:
            provider_name: Name of the provider ('openai', 'xai', etc.)
            api_key: API key for the provider
            model: Optional model override

        Returns:
            Configured provider instance

        Raises:
            ValueError: If provider_name is not recognized
        """
        provider_class = cls._providers.get(provider_name.lower())

        if not provider_class:
            available = ', '.join(cls._providers.keys())
            raise ValueError(
                f"Unknown provider: {provider_name}. "
                f"Available providers: {available}"
            )

        return provider_class(api_key=api_key, model=model)

    @classmethod
    def register_provider(cls, name: str, provider_class: type):
        """
        Register a new provider class.

        Args:
            name: Provider identifier
            provider_class: Class inheriting from BaseProvider
        """
        if not issubclass(provider_class, BaseProvider):
            raise TypeError("Provider class must inherit from BaseProvider")

        cls._providers[name.lower()] = provider_class


if __name__ == "__main__":
    # Usage example
    import os

    # Create provider using factory
    provider = ProviderFactory.create(
        provider_name="openai",
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model="gpt-4"
    )

    # Generate response
    response = provider.generate("What is the capital of France?")
    print(f"Response: {response}")

    # Stream response
    print("\nStreaming response:")
    for chunk in provider.stream_generate("Tell me a short story"):
        print(chunk, end="", flush=True)
    print()
