"""
Anthropic (Claude) provider implementation.
Supports Claude chat models and vision capabilities.
"""

from typing import List, Union
from . import BaseLLMProvider, Message, CompletionResponse
import os
import base64


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider."""

    DEFAULT_MODEL = "claude-sonnet-4-5-20250929"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("anthropic package is required. Install with: pip install anthropic")

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using Claude."""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        response = self.client.messages.create(
            model=kwargs.get("model", self.model),
            messages=formatted_messages,
            max_tokens=kwargs.get("max_tokens", 1024),
            **{k: v for k, v in kwargs.items() if k not in ["model", "max_tokens"]}
        )

        return CompletionResponse(
            content=response.content[0].text,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
            metadata={"id": response.id, "stop_reason": response.stop_reason}
        )

    def stream_complete(self, messages: List[Message], **kwargs):
        """Stream a completion using Claude."""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        with self.client.messages.stream(
            model=kwargs.get("model", self.model),
            messages=formatted_messages,
            max_tokens=kwargs.get("max_tokens", 1024),
        ) as stream:
            for text in stream.text_stream:
                yield text

    def list_models(self) -> List[str]:
        """List available Claude models."""
        return [
            "claude-sonnet-4-5-20250929",
            "claude-opus-4-1",
            "claude-haiku-4-5",
            "claude-3-7-sonnet-20250224",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
        ]

    def analyze_image(self, image: Union[str, bytes], prompt: str = "Describe this image", **kwargs) -> CompletionResponse:
        """
        Analyze an image using Claude's vision capabilities.

        Args:
            image: Base64-encoded string or raw bytes
            prompt: Question about the image
            **kwargs: Optional parameters
                - model: Claude model (default: "claude-sonnet-4-5-20250929")
                - max_tokens: Maximum response length
                - media_type: Image media type (auto-detected if not provided)

        Returns:
            CompletionResponse with image analysis
        """
        model = kwargs.get("model", self.model)
        max_tokens = kwargs.get("max_tokens", 1024)

        # Convert bytes to base64 if needed
        if isinstance(image, bytes):
            image_b64 = base64.b64encode(image).decode('utf-8')
            # Auto-detect media type from bytes
            if image[:8] == b'\x89PNG\r\n\x1a\n':
                media_type = "image/png"
            elif image[:2] == b'\xff\xd8':
                media_type = "image/jpeg"
            elif image[:6] in (b'GIF87a', b'GIF89a'):
                media_type = "image/gif"
            elif image[:4] == b'RIFF' and image[8:12] == b'WEBP':
                media_type = "image/webp"
            else:
                media_type = "image/jpeg"  # Default fallback
        else:
            image_b64 = image
            media_type = "image/jpeg"  # Default for base64 strings

        # Allow override via kwargs
        media_type = kwargs.get("media_type", media_type)

        # Anthropic uses content blocks format
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]

        response = self.client.messages.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )

        return CompletionResponse(
            content=response.content[0].text,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
            metadata={
                "id": response.id,
                "stop_reason": response.stop_reason,
                "vision": True
            }
        )
