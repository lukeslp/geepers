"""
Provider Adapter Pattern for Shared Libraries

Description: Adapter pattern for wrapping shared library implementations with
application-specific methods. Maintains conversation history, adds convenience
methods, and provides consistent interface across providers.

Use Cases:
- Wrapping shared LLM providers with app-specific features
- Adding conversation state to stateless APIs
- Standardizing interfaces across different providers
- Adding local functionality (encoding, validation) to remote services

Dependencies:
- Shared library with base providers
- typing for type hints

Notes:
- Adapter delegates core functionality to shared provider
- Maintains application-specific state (conversation history)
- Adds convenience methods without modifying shared code
- Each provider gets its own adapter subclass

Related Snippets:
- conversation_history_manager.py
- base64_image_encoder.py
- llm_provider_factory.py
"""

from typing import List, Dict, Optional, Any
import base64


# Mock shared library classes (replace with actual imports)
class Message:
    """Shared library message class"""
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class CompletionResponse:
    """Shared library response class"""
    def __init__(self, content: str, model: str, usage: Dict = None):
        self.content = content
        self.model = model
        self.usage = usage or {}
        self.metadata = {}


class BaseProvider:
    """Shared library base provider"""
    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        raise NotImplementedError

    def list_models(self) -> List[str]:
        raise NotImplementedError


# ============================================================================
# ADAPTER PATTERN IMPLEMENTATION
# ============================================================================

class StudioProviderAdapter:
    """
    Base adapter that adds studio-specific methods to shared library providers.

    Responsibilities:
    - Maintain conversation history per instance
    - Convert between studio format and shared library format
    - Add convenience methods (chat, clear_conversation, encode_image)
    - Delegate core functionality to shared provider
    """

    def __init__(self, shared_provider: BaseProvider):
        """
        Initialize adapter with shared provider.

        Args:
            shared_provider: Instance of shared library provider
        """
        self.provider = shared_provider
        self.conversation_history: List[Message] = []

    def chat(
        self,
        message: str,
        model: Optional[str] = None,
        image_data: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> str:
        """
        Studio-compatible chat method with conversation history.

        Args:
            message: User message
            model: Optional model override
            image_data: Optional base64 image data
            image_path: Optional image file path

        Returns:
            Assistant response as string
        """
        # Handle images if provided
        if image_data or image_path:
            content = message
            if image_path and not image_data:
                image_data = self.encode_image(image_path)
            if image_data:
                content = f"{message}\n[Image provided as base64]"

        # Add user message to history
        self.conversation_history.append(
            Message(role="user", content=message)
        )

        # Call shared library complete method
        kwargs = {}
        if model:
            kwargs['model'] = model

        response = self.provider.complete(self.conversation_history, **kwargs)

        # Add assistant response to history
        self.conversation_history.append(
            Message(role="assistant", content=response.content)
        )

        return response.content

    def list_models(self) -> List[str]:
        """List available models - delegates to shared provider"""
        return self.provider.list_models()

    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []

    def encode_image(self, image_path: str) -> Optional[str]:
        """
        Encode image to base64.

        Args:
            image_path: Path to image file

        Returns:
            Base64-encoded image or None on error
        """
        try:
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None


# ============================================================================
# PROVIDER-SPECIFIC ADAPTERS
# ============================================================================

class AnthropicAdapter(StudioProviderAdapter):
    """
    Anthropic-specific adapter with vision support.

    Adds:
    - analyze_image() method for Claude Vision
    """

    def __init__(self, api_key: Optional[str] = None):
        # Import shared library provider
        # from llm_providers.anthropic_provider import AnthropicProvider
        # super().__init__(AnthropicProvider(api_key=api_key))
        super().__init__(BaseProvider())  # Mock for example

    def analyze_image(
        self,
        image: Any,
        prompt: str = "Describe this image",
        **kwargs
    ) -> CompletionResponse:
        """
        Analyze image using Claude Vision.

        Args:
            image: Image bytes or file path
            prompt: Analysis prompt
            **kwargs: Additional arguments (model, etc.)

        Returns:
            CompletionResponse with analysis
        """
        # Delegate to shared library
        return self.provider.analyze_image(image, prompt, **kwargs)


class OpenAIAdapter(StudioProviderAdapter):
    """
    OpenAI-specific adapter with image generation and vision.

    Adds:
    - generate_image() for DALL-E
    - analyze_image() for GPT-4 Vision
    """

    def __init__(self, api_key: Optional[str] = None):
        # from llm_providers.openai_provider import OpenAIProvider
        # super().__init__(OpenAIProvider(api_key=api_key))
        super().__init__(BaseProvider())  # Mock
        self.api_key = api_key

    def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024"
    ):
        """
        Generate image using DALL-E.

        Args:
            prompt: Image description
            model: DALL-E model version
            size: Image dimensions

        Returns:
            ImageResponse with base64 data
        """
        return self.provider.generate_image(prompt, model=model, size=size)

    def analyze_image(self, image: Any, prompt: str = "Describe this image", **kwargs):
        """Analyze image using GPT-4 Vision"""
        return self.provider.analyze_image(image, prompt, **kwargs)


class XAIAdapter(StudioProviderAdapter):
    """
    xAI Grok adapter with Aurora image generation and vision.

    Adds:
    - generate_image() for Aurora
    - analyze_image() for Grok Vision
    - generate_video() for future video generation
    """

    def __init__(self, api_key: Optional[str] = None):
        # from llm_providers.xai_provider import XAIProvider
        # super().__init__(XAIProvider(api_key=api_key))
        super().__init__(BaseProvider())
        self.api_key = api_key

    def generate_image(self, prompt: str, **kwargs):
        """Generate image using Aurora"""
        return self.provider.generate_image(prompt, **kwargs)

    def analyze_image(self, image: Any, prompt: str = "Describe this image", **kwargs):
        """Analyze image using Grok Vision"""
        return self.provider.analyze_image(image, prompt, **kwargs)

    def generate_video(self, prompt: str, image_path: Optional[str] = None) -> Dict:
        """
        Generate video (future capability).

        Args:
            prompt: Video description
            image_path: Optional starting image for image-to-video

        Returns:
            Dict with success status and video URL/data
        """
        # Placeholder for future implementation
        return {
            "success": False,
            "error": "Video generation not yet available"
        }


# ============================================================================
# FACTORY PATTERN FOR PROVIDER CREATION
# ============================================================================

class ProviderFactory:
    """Factory for creating provider adapters with graceful failure"""

    @staticmethod
    def create_provider(
        provider_name: str,
        api_key: Optional[str] = None
    ) -> Optional[StudioProviderAdapter]:
        """
        Create provider adapter with error handling.

        Args:
            provider_name: Name of provider (anthropic, openai, xai, etc.)
            api_key: API key for provider

        Returns:
            Provider adapter instance or None on failure
        """
        adapters = {
            'anthropic': AnthropicAdapter,
            'openai': OpenAIAdapter,
            'xai': XAIAdapter,
        }

        adapter_class = adapters.get(provider_name.lower())
        if not adapter_class:
            print(f"Unknown provider: {provider_name}")
            return None

        try:
            return adapter_class(api_key=api_key)
        except Exception as e:
            print(f"Failed to initialize {provider_name}: {e}")
            return None


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    import os

    # Initialize providers with factory
    providers = {}

    # Try to create each provider
    for name, key_var in [
        ('anthropic', 'ANTHROPIC_API_KEY'),
        ('openai', 'OPENAI_API_KEY'),
        ('xai', 'XAI_API_KEY'),
    ]:
        api_key = os.getenv(key_var)
        if api_key:
            provider = ProviderFactory.create_provider(name, api_key)
            if provider:
                providers[name] = provider
                print(f"✓ {name.title()} provider initialized")

    # Use a provider
    if 'anthropic' in providers:
        claude = providers['anthropic']

        # Chat with conversation history
        response = claude.chat("Hello! What's your name?")
        print(f"Claude: {response}")

        response = claude.chat("What did I just ask you?")
        print(f"Claude: {response}")

        # List available models
        models = claude.list_models()
        print(f"Available models: {models}")

        # Clear conversation
        claude.clear_conversation()

    # Image generation
    if 'openai' in providers:
        gpt = providers['openai']

        image_result = gpt.generate_image("A serene mountain landscape")
        print(f"Generated image: {len(image_result.image_data)} chars of base64")
