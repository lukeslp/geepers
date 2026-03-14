"""
Groq provider implementation.
Ultra-fast inference with OpenAI-compatible API.
"""

from typing import List
from . import BaseLLMProvider, Message, CompletionResponse
import os


class GroqProvider(BaseLLMProvider):
    """Groq provider with ultra-fast inference."""

    DEFAULT_MODEL = "llama-3.3-70b-versatile"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        except ImportError:
            raise ImportError("openai package is required. Install with: pip install openai")

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using Groq."""
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
                "finish_reason": response.choices[0].finish_reason
            }
        )

    def stream_complete(self, messages: List[Message], **kwargs):
        """Stream a completion using Groq."""
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
        """List available Groq models."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception:
            # Fallback list of known models (2025)
            return [
                "llama-3.3-70b-versatile",
                "llama-3.3-70b-specdec",
                "llama-3.1-405b-reasoning",
                "llama-3.1-70b-versatile",
                "llama-3.1-8b-instant",
                "llama-3.2-90b-vision-preview",
                "llama-3.2-11b-vision-preview",
                "llama-3.2-3b-preview",
                "llama-3.2-1b-preview",
                "llama-guard-3-8b",
                "mixtral-8x7b-32768",
                "gemma2-9b-it",
                "gemma-7b-it",
            ]
