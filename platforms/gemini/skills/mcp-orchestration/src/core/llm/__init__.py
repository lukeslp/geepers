"""
Unified LLM provider abstraction layer.

Supports multiple AI providers with a consistent interface:
- OpenAI (GPT-4, DALL-E, Vision)
- Anthropic (Claude, Vision)
- xAI (Grok, Aurora, Vision)
- Mistral
- Cohere
- Google (Gemini, Vision)
- Manus (Agent Profiles, Vision)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class Message:
    """Standard message format across all providers."""
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CompletionResponse:
    """Standard response format across all providers."""
    content: str
    model: str
    usage: Dict[str, int]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ImageResponse:
    """Standard response format for image generation."""
    image_data: str  # Base64-encoded image data
    model: str
    revised_prompt: Optional[str] = None  # Some providers revise the prompt
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AudioResponse:
    """Standard response format for audio operations (TTS, transcription)."""
    audio_data: Optional[bytes] = None  # Raw audio bytes (for TTS)
    text: Optional[str] = None  # Transcribed text (for Whisper)
    language: Optional[str] = None  # Detected/specified language
    duration: Optional[float] = None  # Audio duration in seconds
    model: Optional[str] = None  # Model used
    metadata: Optional[Dict[str, Any]] = None  # Additional provider-specific data


@dataclass
class VisionMessage:
    """Message format for vision requests (text + image)."""
    role: str  # "user", "assistant", "system"
    text: str
    image_data: Optional[str] = None  # Base64-encoded image
    image_url: Optional[str] = None  # URL to image
    metadata: Optional[Dict[str, Any]] = None


class BaseLLMProvider(ABC):
    """Base class for all LLM providers."""

    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion from the LLM."""

    @abstractmethod
    def stream_complete(self, messages: List[Message], **kwargs):
        """Stream a completion from the LLM."""

    @abstractmethod
    def list_models(self) -> List[str]:
        """List available models for this provider."""

    def generate_image(self, prompt: str, **kwargs) -> ImageResponse:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text description of the image to generate
            **kwargs: Provider-specific options (model, size, quality, etc.)

        Returns:
            ImageResponse with base64-encoded image data

        Raises:
            NotImplementedError: If provider doesn't support image generation
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support image generation")

    def analyze_image(self, image: Union[str, bytes], prompt: str = "Describe this image", **kwargs) -> CompletionResponse:
        """
        Analyze an image using vision capabilities.

        Args:
            image: Base64-encoded image string or raw bytes
            prompt: Question or instruction about the image
            **kwargs: Provider-specific options (model, max_tokens, etc.)

        Returns:
            CompletionResponse with the analysis/description

        Raises:
            NotImplementedError: If provider doesn't support vision
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support vision")


# Import factory for convenient access
from .factory import ProviderFactory, PROVIDER_CAPABILITIES, COMPLEXITY_TIERS


def get_provider(provider_name: str, api_key: Optional[str] = None, model: Optional[str] = None):
    """
    Backwards-compatible helper that returns a provider instance.

    Args:
        provider_name: Name of the provider (e.g., 'openai', 'anthropic', 'xai')
        api_key: Optional explicit API key. When provided, a fresh provider
                 instance is created instead of using the cached singleton.
        model: Optional default model for the provider.

    Returns:
        BaseLLMProvider instance.
    """
    if api_key:
        return ProviderFactory.create_provider(provider_name, api_key=api_key, model=model)
    return ProviderFactory.get_provider(provider_name)

__all__ = [
    'Message',
    'CompletionResponse',
    'ImageResponse',
    'AudioResponse',
    'VisionMessage',
    'BaseLLMProvider',
    'ProviderFactory',
    'PROVIDER_CAPABILITIES',
    'COMPLEXITY_TIERS',
]
