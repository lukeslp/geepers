"""
xAI (Grok) provider implementation.
Supports Grok models, Aurora image generation, and Grok Vision.
"""

from typing import List, Union
from . import BaseLLMProvider, Message, CompletionResponse, ImageResponse
import os
import base64
import requests


class XAIProvider(BaseLLMProvider):
    """xAI Grok provider using OpenAI-compatible API."""

    DEFAULT_MODEL = "grok-4"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.x.ai/v1"
            )
        except ImportError:
            raise ImportError("openai package is required. Install with: pip install openai")

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using Grok."""
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
        """Stream a completion using Grok."""
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

    async def chat(self, messages=None, system_prompt=None, user_prompt=None, **kwargs) -> CompletionResponse:
        """
        Async alias for complete() to support orchestrator compatibility.
        Orchestrators call await chat(system_prompt=..., user_prompt=...)
        but providers use complete(messages=[...]).
        """
        # Convert orchestrator's system_prompt/user_prompt to messages list
        if messages is None and (system_prompt or user_prompt):
            messages = []
            if system_prompt:
                messages.append(Message(role="system", content=system_prompt))
            if user_prompt:
                messages.append(Message(role="user", content=user_prompt))

        # Run sync complete() in thread pool to make it awaitable
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.complete(messages, **kwargs))

    def list_models(self) -> List[str]:
        """List available Grok models."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception:
            # Fallback list of known models (2025)
            return [
                "grok-4",
                "grok-4-heavy",
                "grok-3",
                "grok-3-mini",
                "grok-2-vision-1212",
                "grok-code-fast-1",
            ]

    def generate_image(self, prompt: str, **kwargs) -> ImageResponse:
        """
        Generate an image using Aurora (xAI's image generation model).

        Args:
            prompt: Text description of the image
            **kwargs: Optional parameters
                - model: Aurora model (default: "aurora")
                - steps: Number of diffusion steps (1-50, default: 30)
                - cfg_scale: Guidance scale (1-20, default: 7)

        Returns:
            ImageResponse with base64-encoded image
        """
        model = kwargs.get("model", "aurora")
        steps = kwargs.get("steps", 30)
        cfg_scale = kwargs.get("cfg_scale", 7)

        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            n=1
        )

        # xAI returns a URL, we need to download and convert to base64
        image_url = response.data[0].url
        img_response = requests.get(image_url)

        if img_response.status_code == 200:
            image_b64 = base64.b64encode(img_response.content).decode('utf-8')
            return ImageResponse(
                image_data=image_b64,
                model=model,
                revised_prompt=None,
                metadata={
                    "url": image_url,
                    "steps": steps,
                    "cfg_scale": cfg_scale
                }
            )
        else:
            raise Exception(f"Failed to download image from xAI: {img_response.status_code}")

    def analyze_image(self, image: Union[str, bytes], prompt: str = "Describe this image", **kwargs) -> CompletionResponse:
        """
        Analyze an image using Grok Vision.

        Args:
            image: Base64-encoded string or raw bytes
            prompt: Question about the image
            **kwargs: Optional parameters
                - model: Vision model (default: "grok-2-vision-1212")
                - max_tokens: Maximum response length

        Returns:
            CompletionResponse with image analysis
        """
        model = kwargs.get("model", "grok-2-vision-1212")
        max_tokens = kwargs.get("max_tokens", 500)

        # Convert bytes to base64 if needed
        if isinstance(image, bytes):
            image_b64 = base64.b64encode(image).decode('utf-8')
        else:
            image_b64 = image

        # Construct vision message
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ]

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
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
                "vision": True
            }
        )
