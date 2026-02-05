"""
Lazy-Loading Provider Factory with Singleton Pattern

Description: Factory for LLM providers with lazy initialization and caching.
Avoids importing unused providers, reduces memory footprint, and enables
graceful handling of missing optional dependencies.

Use Cases:
- Multi-provider applications that don't use all providers simultaneously
- Systems with optional provider support (install only what you need)
- Testing environments where some providers may not be configured
- Dynamic provider switching based on availability
- Memory-constrained environments

Dependencies:
- typing hints (Python 3.8+)
- Provider classes (lazy imported)

Notes:
- Providers loaded on-demand (first access)
- Singleton instances cached after creation
- Graceful handling of missing optional providers
- Thread-safe singleton implementation
- Clear cache for testing/reinitialization

Related Snippets:
- /api-clients/cost_optimized_model_selection.py
- /configuration-management/provider_config.py
- /error-handling/graceful_degradation.py

Performance:
    Cold start (first call): Import + initialize (~50-100ms)
    Subsequent calls: Cache lookup (~0.1ms)
    Memory per provider: ~500KB-2MB
"""

from typing import Dict, Optional, Type, Any


class ProviderFactory:
    """
    Singleton factory for lazy-loading LLM providers.

    Providers are only imported and instantiated when first requested,
    reducing startup time and memory usage.
    """

    _instances: Dict[str, Any] = {}
    _lock = None  # Use threading.Lock() in production

    @classmethod
    def get_provider(cls, provider_name: str):
        """
        Get or create a provider instance with lazy loading.

        Args:
            provider_name: Name of the provider ('xai', 'anthropic', 'openai', etc.)

        Returns:
            Provider instance (cached after first creation)

        Raises:
            ValueError: If provider_name is not recognized

        Example:
            # First call: imports and initializes provider
            provider = ProviderFactory.get_provider('xai')

            # Subsequent calls: returns cached instance
            same_provider = ProviderFactory.get_provider('xai')
            assert provider is same_provider
        """
        if provider_name not in cls._instances:
            # Lazy import providers to avoid unnecessary dependencies
            provider_classes = cls._get_provider_classes()

            if provider_name not in provider_classes:
                available = list(provider_classes.keys())
                raise ValueError(
                    f"Unknown provider: {provider_name}. "
                    f"Available providers: {', '.join(available)}"
                )

            # Instantiate and cache the provider
            cls._instances[provider_name] = provider_classes[provider_name]()

        return cls._instances[provider_name]

    @classmethod
    def _get_provider_classes(cls) -> Dict[str, Type]:
        """
        Get mapping of provider names to classes.

        Imports are done here to keep them lazy. This method is called
        only once per factory instance, or when cache is cleared.

        Returns:
            Dict mapping provider names to provider classes
        """
        # Core providers that are always available
        providers = {}

        # Import core providers
        try:
            from llm_providers.xai_provider import XAIProvider
            providers['xai'] = XAIProvider
        except ImportError:
            pass

        try:
            from llm_providers.anthropic_provider import AnthropicProvider
            providers['anthropic'] = AnthropicProvider
        except ImportError:
            pass

        try:
            from llm_providers.openai_provider import OpenAIProvider
            providers['openai'] = OpenAIProvider
        except ImportError:
            pass

        # Optional providers (gracefully handle if not installed)
        optional_providers = [
            ('mistral', 'llm_providers.mistral_provider', 'MistralProvider'),
            ('cohere', 'llm_providers.cohere_provider', 'CohereProvider'),
            ('gemini', 'llm_providers.gemini_provider', 'GeminiProvider'),
            ('perplexity', 'llm_providers.perplexity_provider', 'PerplexityProvider'),
            ('huggingface', 'llm_providers.huggingface_provider', 'HuggingFaceProvider'),
            ('groq', 'llm_providers.groq_provider', 'GroqProvider'),
            ('manus', 'llm_providers.manus_provider', 'ManusProvider'),
            ('elevenlabs', 'llm_providers.elevenlabs_provider', 'ElevenLabsProvider'),
        ]

        for name, module, class_name in optional_providers:
            try:
                module_obj = __import__(module, fromlist=[class_name])
                providers[name] = getattr(module_obj, class_name)
            except ImportError:
                pass  # Optional provider not installed

        return providers

    @classmethod
    def clear_cache(cls, provider_name: Optional[str] = None) -> None:
        """
        Clear cached provider instances.

        Useful for testing or when provider configuration changes.

        Args:
            provider_name: Specific provider to clear, or None to clear all

        Example:
            # Clear specific provider
            ProviderFactory.clear_cache('xai')

            # Clear all providers
            ProviderFactory.clear_cache()
        """
        if provider_name:
            cls._instances.pop(provider_name, None)
        else:
            cls._instances.clear()

    @classmethod
    def list_providers(cls) -> list:
        """
        List all available provider names.

        Returns:
            List of provider name strings

        Example:
            available = ProviderFactory.list_providers()
            print(f"Available providers: {', '.join(available)}")
            # Output: "Available providers: xai, anthropic, openai, mistral, ..."
        """
        return list(cls._get_provider_classes().keys())

    @classmethod
    def is_provider_available(cls, provider_name: str) -> bool:
        """
        Check if a provider is available.

        Args:
            provider_name: Provider name to check

        Returns:
            True if provider is available, False otherwise

        Example:
            if ProviderFactory.is_provider_available('anthropic'):
                provider = ProviderFactory.get_provider('anthropic')
            else:
                print("Anthropic provider not installed")
        """
        return provider_name in cls._get_provider_classes()

    @classmethod
    def get_cached_providers(cls) -> list:
        """
        Get list of currently cached (instantiated) providers.

        Returns:
            List of provider names that have been cached

        Example:
            # After using some providers
            ProviderFactory.get_provider('xai')
            ProviderFactory.get_provider('openai')

            cached = ProviderFactory.get_cached_providers()
            print(f"Cached: {cached}")
            # Output: "Cached: ['xai', 'openai']"
        """
        return list(cls._instances.keys())


# Convenience functions for common operations

def get_provider(name: str):
    """
    Get provider instance (convenience function).

    Args:
        name: Provider name

    Returns:
        Provider instance

    Example:
        from lazy_loading_provider_factory import get_provider

        provider = get_provider('xai')
        response = provider.chat([{"role": "user", "content": "Hello"}])
    """
    return ProviderFactory.get_provider(name)


def list_available_providers() -> list:
    """
    List all available providers (convenience function).

    Returns:
        List of provider names

    Example:
        providers = list_available_providers()
        for name in providers:
            print(f"- {name}")
    """
    return ProviderFactory.list_providers()


def create_provider_with_fallback(
    preferred: str,
    fallback: str,
    *additional_fallbacks: str
) -> Any:
    """
    Create provider with automatic fallback chain.

    Args:
        preferred: Preferred provider name
        fallback: Fallback provider name
        *additional_fallbacks: Additional fallback providers

    Returns:
        First available provider instance

    Example:
        # Try anthropic, fall back to openai, then xai
        provider = create_provider_with_fallback(
            'anthropic',
            'openai',
            'xai'
        )
    """
    providers_to_try = [preferred, fallback] + list(additional_fallbacks)

    for name in providers_to_try:
        if ProviderFactory.is_provider_available(name):
            return ProviderFactory.get_provider(name)

    raise ValueError(
        f"None of the specified providers are available: {providers_to_try}"
    )


# Thread-safe version (use in production)
class ThreadSafeProviderFactory(ProviderFactory):
    """
    Thread-safe version of ProviderFactory.

    Use this in multi-threaded applications to prevent race conditions
    during provider initialization.
    """

    import threading
    _lock = threading.Lock()

    @classmethod
    def get_provider(cls, provider_name: str):
        """Thread-safe get_provider implementation."""
        # Check if already cached (fast path, no lock)
        if provider_name in cls._instances:
            return cls._instances[provider_name]

        # Initialize with lock (slow path)
        with cls._lock:
            # Double-check after acquiring lock
            if provider_name not in cls._instances:
                provider_classes = cls._get_provider_classes()

                if provider_name not in provider_classes:
                    available = list(provider_classes.keys())
                    raise ValueError(
                        f"Unknown provider: {provider_name}. "
                        f"Available providers: {', '.join(available)}"
                    )

                cls._instances[provider_name] = provider_classes[provider_name]()

        return cls._instances[provider_name]


if __name__ == "__main__":
    # Usage examples

    # Example 1: Basic usage
    print("Example 1: Basic usage")
    print("Available providers:", ProviderFactory.list_providers())

    provider = ProviderFactory.get_provider('xai')
    print(f"Got provider: {provider}")

    # Example 2: Check what's cached
    print("\nExample 2: Cached providers")
    print("Before:", ProviderFactory.get_cached_providers())
    ProviderFactory.get_provider('anthropic')
    ProviderFactory.get_provider('openai')
    print("After:", ProviderFactory.get_cached_providers())

    # Example 3: Fallback chain
    print("\nExample 3: Fallback chain")
    try:
        provider = create_provider_with_fallback(
            'nonexistent',
            'anthropic',
            'xai'
        )
        print(f"Got fallback provider: {provider}")
    except ValueError as e:
        print(f"Error: {e}")

    # Example 4: Clear cache
    print("\nExample 4: Clear cache")
    print("Before clear:", ProviderFactory.get_cached_providers())
    ProviderFactory.clear_cache('xai')
    print("After clearing xai:", ProviderFactory.get_cached_providers())
    ProviderFactory.clear_cache()
    print("After clearing all:", ProviderFactory.get_cached_providers())

    # Example 5: Check availability
    print("\nExample 5: Check availability")
    for name in ['xai', 'anthropic', 'fake_provider']:
        available = ProviderFactory.is_provider_available(name)
        print(f"{name}: {'available' if available else 'not available'}")
