"""
Mistral AI provider implementation.
"""

from typing import List
from . import BaseLLMProvider, Message, CompletionResponse
import os
import json


class MistralProvider(BaseLLMProvider):
    """Mistral AI provider."""

    DEFAULT_MODEL = "mistral-large-2411"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        self.api_url = "https://api.mistral.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("requests package is required. Install with: pip install requests")

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using Mistral."""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        payload = {
            "model": kwargs.get("model", self.model),
            "messages": formatted_messages,
            **{k: v for k, v in kwargs.items() if k != "model"}
        }

        response = self.requests.post(
            f"{self.api_url}/chat/completions",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        return CompletionResponse(
            content=data["choices"][0]["message"]["content"],
            model=data["model"],
            usage={
                "prompt_tokens": data["usage"]["prompt_tokens"],
                "completion_tokens": data["usage"]["completion_tokens"],
                "total_tokens": data["usage"]["total_tokens"],
            },
            metadata={
                "id": data["id"],
                "finish_reason": data["choices"][0]["finish_reason"]
            }
        )

    def stream_complete(self, messages: List[Message], **kwargs):
        """Stream a completion using Mistral."""
        formatted_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

        payload = {
            "model": kwargs.get("model", self.model),
            "messages": formatted_messages,
            "stream": True,
            **{k: v for k, v in kwargs.items() if k not in ["model", "stream"]}
        }

        response = self.requests.post(
            f"{self.api_url}/chat/completions",
            headers=self.headers,
            json=payload,
            stream=True
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                if line_text.startswith("data: "):
                    line_text = line_text[6:]
                if line_text == "[DONE]":
                    break
                try:
                    data = json.loads(line_text)
                    content = data['choices'][0]['delta'].get('content', '')
                    if content:
                        yield content
                except json.JSONDecodeError:
                    continue

    def list_models(self) -> List[str]:
        """List available Mistral models."""
        try:
            response = self.requests.get(
                f"{self.api_url}/models",
                headers=self.headers
            )
            response.raise_for_status()
            models = response.json().get("data", [])
            return [model["id"] for model in models]
        except Exception:
            # Fallback list of known models (2025)
            return [
                "mistral-large-2411",
                "pixtral-large-latest",
                "mistral-small-3-1",
                "open-mixtral-8x22b",
                "pixtral-12b",
                "ministral-8b",
                "ministral-3b",
            ]
