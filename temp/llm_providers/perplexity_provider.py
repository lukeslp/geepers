"""
Perplexity provider implementation.
"""

from typing import List
from . import BaseLLMProvider, Message, CompletionResponse
import os


class PerplexityProvider(BaseLLMProvider):
    """Perplexity search-augmented provider using OpenAI-compatible API."""

    DEFAULT_MODEL = "sonar-pro"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise ValueError("PERPLEXITY_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.perplexity.ai"
            )
        except ImportError:
            raise ImportError("openai package is required. Install with: pip install openai")

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using Perplexity."""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        response = self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=formatted_messages,
            **{k: v for k, v in kwargs.items() if k != "model"}
        )

        return CompletionResponse(
            content=response.choices[0].message.content,
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            metadata={
                "id": response.id,
                "finish_reason": response.choices[0].finish_reason,
                "citations": getattr(response, "citations", None)  # Perplexity includes citations
            }
        )

    def stream_complete(self, messages: List[Message], **kwargs):
        """Stream a completion using Perplexity."""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        stream = self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=formatted_messages,
            stream=True,
            **{k: v for k, v in kwargs.items() if k not in ["model", "stream"]}
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    def list_models(self) -> List[str]:
        """List available Perplexity models."""
        # Perplexity doesn't provide a models endpoint, return known models (2025 Sonar API)
        return [
            "sonar-pro",
            "sonar",
            "sonar-reasoning-pro",
            "llama-3.1-sonar-large-128k-online",
            "llama-3.1-sonar-small-128k-online",
        ]
