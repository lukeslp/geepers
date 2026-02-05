"""
Cohere provider implementation.
"""

from typing import List
from . import BaseLLMProvider, Message, CompletionResponse
import os


class CohereProvider(BaseLLMProvider):
    """Cohere provider."""

    DEFAULT_MODEL = "command-a-03-2025"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        try:
            import cohere
            self.client = cohere.Client(api_key=api_key)
        except ImportError:
            raise ImportError("cohere package is required. Install with: pip install cohere")

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using Cohere."""
        # Convert messages to Cohere chat format
        chat_history = []
        message = None

        for msg in messages:
            if msg.role == "user":
                message = msg.content
            elif msg.role == "assistant":
                if message:  # Need a user message before assistant
                    chat_history.append({"role": "USER", "message": message})
                    message = None
                chat_history.append({"role": "CHATBOT", "message": msg.content})
            elif msg.role == "system":
                # Cohere handles system messages differently
                kwargs["preamble"] = msg.content

        # Last message should be user message
        if not message and messages:
            message = messages[-1].content

        response = self.client.chat(
            model=kwargs.get("model", self.model),
            message=message,
            chat_history=chat_history if chat_history else None,
            **{k: v for k, v in kwargs.items() if k not in ["model", "preamble"]}
        )

        # Calculate approximate token usage (Cohere doesn't always provide this)
        billed_units = getattr(response.meta, "billed_units", None)
        if billed_units:
            usage = {
                "prompt_tokens": getattr(billed_units, "input_tokens", 0),
                "completion_tokens": getattr(billed_units, "output_tokens", 0),
            }
        else:
            usage = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
            }
        usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]

        return CompletionResponse(
            content=response.text,
            model=response.generation_id or self.model,
            usage=usage,
            metadata={
                "id": response.generation_id,
                "finish_reason": response.finish_reason
            }
        )

    def stream_complete(self, messages: List[Message], **kwargs):
        """Stream a completion using Cohere."""
        # Convert messages to Cohere chat format
        chat_history = []
        message = None

        for msg in messages:
            if msg.role == "user":
                message = msg.content
            elif msg.role == "assistant":
                if message:
                    chat_history.append({"role": "USER", "message": message})
                    message = None
                chat_history.append({"role": "CHATBOT", "message": msg.content})
            elif msg.role == "system":
                kwargs["preamble"] = msg.content

        if not message and messages:
            message = messages[-1].content

        stream = self.client.chat_stream(
            model=kwargs.get("model", self.model),
            message=message,
            chat_history=chat_history if chat_history else None,
            **{k: v for k, v in kwargs.items() if k not in ["model", "preamble"]}
        )

        for event in stream:
            if event.event_type == "text-generation":
                yield event.text

    def list_models(self) -> List[str]:
        """List available Cohere models."""
        try:
            models = self.client.models.list()
            return [model.name for model in models.models if "command" in model.name.lower()]
        except Exception:
            # Fallback list of known models (2025)
            return [
                "command-a-03-2025",
                "command-a-translate-08-2025",
                "command-a-reasoning",
                "command-a-vision",
                "command-r-08-2024",
                "command-r-plus-08-2024",
                "command-r7b",
            ]
