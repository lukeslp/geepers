"""
Google Gemini provider implementation.
"""

from typing import List, Dict, Any
from . import BaseLLMProvider, Message, CompletionResponse
import os


class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider."""

    DEFAULT_MODEL = "gemini-2.5-pro"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.genai = genai
        except ImportError:
            raise ImportError(
                "google-generativeai package is required. "
                "Install with: pip install google-generativeai"
            )

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using Gemini."""
        model_name = kwargs.get("model", self.model)
        model = self.genai.GenerativeModel(model_name)

        # Convert messages to Gemini format
        # Gemini uses a simpler format: just user/model roles
        gemini_messages = []
        for msg in messages:
            role = "user" if msg.role in ["user", "system"] else "model"
            gemini_messages.append({
                "role": role,
                "parts": [msg.content]
            })

        # Use chat if multiple messages, otherwise generate_content
        if len(gemini_messages) > 1:
            chat = model.start_chat(history=gemini_messages[:-1])
            response = chat.send_message(
                gemini_messages[-1]["parts"][0],
                generation_config=self._get_generation_config(kwargs)
            )
        else:
            response = model.generate_content(
                gemini_messages[0]["parts"][0],
                generation_config=self._get_generation_config(kwargs)
            )

        # Extract token counts
        usage = {
            "prompt_tokens": response.usage_metadata.prompt_token_count,
            "completion_tokens": response.usage_metadata.candidates_token_count,
            "total_tokens": response.usage_metadata.total_token_count,
        }

        return CompletionResponse(
            content=response.text,
            model=model_name,
            usage=usage,
            metadata={
                "finish_reason": response.candidates[0].finish_reason.name if response.candidates else None
            }
        )

    def stream_complete(self, messages: List[Message], **kwargs):
        """Stream a completion using Gemini."""
        model_name = kwargs.get("model", self.model)
        model = self.genai.GenerativeModel(model_name)

        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            role = "user" if msg.role in ["user", "system"] else "model"
            gemini_messages.append({
                "role": role,
                "parts": [msg.content]
            })

        # Stream response
        if len(gemini_messages) > 1:
            chat = model.start_chat(history=gemini_messages[:-1])
            response = chat.send_message(
                gemini_messages[-1]["parts"][0],
                generation_config=self._get_generation_config(kwargs),
                stream=True
            )
        else:
            response = model.generate_content(
                gemini_messages[0]["parts"][0],
                generation_config=self._get_generation_config(kwargs),
                stream=True
            )

        for chunk in response:
            if chunk.text:
                yield chunk.text

    def list_models(self) -> List[str]:
        """List available Gemini models."""
        try:
            models = self.genai.list_models()
            return [
                model.name.replace("models/", "")
                for model in models
                if "generateContent" in model.supported_generation_methods
            ]
        except Exception:
            # Fallback list of known models (2025)
            return [
                "gemini-2.5-pro",
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-2.0-pro",
                "gemini-2.0-flash",
                "gemini-2.0-flash-lite",
                "gemini-1.5-pro",
                "gemini-1.5-flash",
            ]

    def _get_generation_config(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Extract Gemini-compatible generation config from kwargs."""
        config = {}
        if "temperature" in kwargs:
            config["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            config["max_output_tokens"] = kwargs["max_tokens"]
        if "top_p" in kwargs:
            config["top_p"] = kwargs["top_p"]
        if "top_k" in kwargs:
            config["top_k"] = kwargs["top_k"]
        return config
