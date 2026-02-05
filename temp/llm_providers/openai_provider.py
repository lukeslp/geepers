"""
OpenAI provider implementation.
Supports GPT models, DALL-E image generation, and GPT-4 Vision.
"""

from typing import List, Union, Optional
from pathlib import Path
from . import BaseLLMProvider, Message, CompletionResponse, ImageResponse, AudioResponse
import os
import base64


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT provider."""

    DEFAULT_MODEL = "gpt-4.1"

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package is required. Install with: pip install openai")

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """Generate a completion using GPT."""
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
        """Stream a completion using GPT."""
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
        """List available OpenAI models."""
        models = self.client.models.list()
        return [model.id for model in models.data if "gpt" in model.id.lower()]

    def generate_image(self, prompt: str, **kwargs) -> ImageResponse:
        """
        Generate an image using DALL-E.

        Args:
            prompt: Text description of the image
            **kwargs: Optional parameters
                - model: DALL-E model ("dall-e-3" or "dall-e-2", default: "dall-e-3")
                - size: Image size ("1024x1024", "1792x1024", "1024x1792" for dall-e-3)
                - quality: "standard" or "hd" (dall-e-3 only)
                - n: Number of images (1-10, dall-e-2 only)

        Returns:
            ImageResponse with base64-encoded image
        """
        model = kwargs.get("model", "dall-e-3")
        size = kwargs.get("size", "1024x1024")
        quality = kwargs.get("quality", "standard")
        n = kwargs.get("n", 1)

        # Build request params
        params = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": n,
            "response_format": "b64_json"
        }

        # Only add quality for dall-e-3
        if model == "dall-e-3":
            params["quality"] = quality

        response = self.client.images.generate(**params)

        return ImageResponse(
            image_data=response.data[0].b64_json,
            model=model,
            revised_prompt=getattr(response.data[0], 'revised_prompt', None),
            metadata={
                "size": size,
                "quality": quality if model == "dall-e-3" else None
            }
        )

    def analyze_image(self, image: Union[str, bytes], prompt: str = "Describe this image", **kwargs) -> CompletionResponse:
        """
        Analyze an image using GPT-4 Vision.

        Args:
            image: Base64-encoded string or raw bytes
            prompt: Question about the image
            **kwargs: Optional parameters
                - model: Vision model (default: "gpt-4o")
                - max_tokens: Maximum response length

        Returns:
            CompletionResponse with image analysis
        """
        model = kwargs.get("model", "gpt-4o")
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

    def transcribe_audio(
        self,
        audio_file: Union[str, Path],
        language: Optional[str] = None,
        model: str = "whisper-1",
        response_format: str = "verbose_json",
        temperature: float = 0.0,
        **kwargs
    ) -> AudioResponse:
        """
        Transcribe audio to text using Whisper API.

        Args:
            audio_file: Path to audio file (supports mp3, mp4, mpeg, mpga, m4a, wav, webm)
            language: ISO-639-1 language code (e.g., 'en', 'es') - improves accuracy if known
            model: Whisper model (currently only "whisper-1" available)
            response_format: "json", "text", "srt", "verbose_json" (default), "vtt"
            temperature: 0.0-1.0, affects randomness (default: 0.0 for consistency)
            **kwargs: Additional parameters (timestamp_granularities, prompt)

        Returns:
            AudioResponse with text, language, duration, metadata

        Raises:
            ValueError: Invalid file format or missing file
            FileNotFoundError: Audio file not found
        """
        # Convert to Path object for validation
        audio_path = Path(audio_file)

        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        # Validate file extension
        valid_extensions = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm', '.ogg'}
        if audio_path.suffix.lower() not in valid_extensions:
            raise ValueError(
                f"Invalid audio format: {audio_path.suffix}. "
                f"Supported: {', '.join(valid_extensions)}"
            )

        # Build API request parameters
        params = {
            "model": model,
            "response_format": response_format,
            "temperature": temperature,
        }

        if language:
            params["language"] = language

        # Add any additional parameters
        for key, value in kwargs.items():
            if key not in params:
                params[key] = value

        # Open and transcribe the file
        with open(audio_path, "rb") as audio_file_handle:
            response = self.client.audio.transcriptions.create(
                file=audio_file_handle,
                **params
            )

        # Parse response based on format
        if response_format == "verbose_json":
            # Verbose format includes detailed metadata
            return AudioResponse(
                text=response.text,
                language=response.language,
                duration=response.duration,
                model=model,
                metadata={
                    "segments": response.segments if hasattr(response, 'segments') else None,
                    "words": response.words if hasattr(response, 'words') else None,
                }
            )
        else:
            # Simple format (text, json, srt, vtt)
            return AudioResponse(
                text=str(response) if not hasattr(response, 'text') else response.text,
                model=model,
                metadata={"response_format": response_format}
            )

    def generate_speech(
        self,
        text: str,
        voice: str = "alloy",
        model: str = "tts-1",
        speed: float = 1.0,
        response_format: str = "mp3",
        **kwargs
    ) -> AudioResponse:
        """
        Generate speech from text using OpenAI TTS.

        Args:
            text: Text to convert to speech (max 4096 characters)
            voice: Voice ID - "alloy", "echo", "fable", "onyx", "nova", "shimmer"
                   alloy: neutral, balanced (default)
                   echo: male, confident
                   fable: British accent, expressive
                   onyx: male, deep
                   nova: female, energetic
                   shimmer: female, soft
            model: "tts-1" (faster, cheaper) or "tts-1-hd" (higher quality)
            speed: 0.25-4.0, playback speed multiplier (default: 1.0)
            response_format: "mp3" (default), "opus", "aac", "flac", "wav", "pcm"
            **kwargs: Additional parameters

        Returns:
            AudioResponse with audio_data (bytes), model, metadata

        Raises:
            ValueError: Text too long or invalid parameters
        """
        # Validate text length
        if not text or len(text.strip()) == 0:
            raise ValueError("Text cannot be empty")

        if len(text) > 4096:
            raise ValueError(f"Text too long: {len(text)} characters (max 4096)")

        # Validate voice
        valid_voices = {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}
        if voice not in valid_voices:
            raise ValueError(
                f"Invalid voice: {voice}. "
                f"Valid voices: {', '.join(sorted(valid_voices))}"
            )

        # Validate speed
        if not 0.25 <= speed <= 4.0:
            raise ValueError(f"Speed must be between 0.25 and 4.0 (got {speed})")

        # Generate speech
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text,
            speed=speed,
            response_format=response_format
        )

        # Get audio bytes
        audio_bytes = response.content

        return AudioResponse(
            audio_data=audio_bytes,
            model=model,
            metadata={
                "voice": voice,
                "speed": speed,
                "format": response_format,
                "characters": len(text),
                "size_bytes": len(audio_bytes)
            }
        )
