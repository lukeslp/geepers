"""
ElevenLabs provider implementation.
Supports high-quality text-to-speech with voice cloning and emotional control.
"""

from typing import List, Dict
from . import BaseLLMProvider, Message, CompletionResponse, AudioResponse
import os
import requests


class ElevenLabsProvider(BaseLLMProvider):
    """ElevenLabs text-to-speech provider."""

    DEFAULT_MODEL = "eleven_turbo_v2_5"
    API_BASE = "https://api.elevenlabs.io/v1"

    # Pre-made voices (free tier accessible)
    PREMADE_VOICES = {
        "rachel": "21m00Tcm4TlvDq8ikWAM",  # Female, calm narrator
        "drew": "29vD33N1CtxCmqQRPOHJ",    # Male, news anchor
        "clyde": "2EiwWnXFnvU5JabPnv8n",   # Male, middle-aged
        "paul": "5Q0t7uMcjvnagumLfvZi",    # Male, narration
        "domi": "AZnzlk1XvdvUeBnXmlld",    # Female, strong
        "dave": "CYw3kZ02Hs0563khs1Fj",    # Male, conversational
        "fin": "D38z5RcWu1voky8WS1ja",     # Male, Irish accent
        "bella": "EXAVITQu4vr4xnSDxMaL",   # Female, soft
        "antoni": "ErXwobaYiN019PkySvjV",  # Male, well-rounded
        "elli": "MF3mGyEYCl7XYWbV9V6O",    # Female, energetic
        "josh": "TxGEqnHWrfWFTfGW9XjX",    # Male, deep
        "arnold": "VR6AewLTigWG4xSOukaG",  # Male, crisp
        "adam": "pNInz6obpgDQGcFmaJgB",    # Male, deep American
        "sam": "yoZ06aMxZJJ28mfd3POQ",     # Male, raspy
    }

    def __init__(self, api_key: str = None, model: str = None):
        api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY is required")

        model = model or self.DEFAULT_MODEL
        super().__init__(api_key, model)

        # Initialize requests session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "xi-api-key": api_key,
            "Content-Type": "application/json"
        })

    def complete(self, messages: List[Message], **kwargs) -> CompletionResponse:
        """ElevenLabs is TTS-only, doesn't support chat completion."""
        raise NotImplementedError("ElevenLabs does not support chat completion")

    def stream_complete(self, messages: List[Message], **kwargs):
        """ElevenLabs is TTS-only, doesn't support chat streaming."""
        raise NotImplementedError("ElevenLabs does not support chat streaming")

    def list_models(self) -> List[str]:
        """List available TTS models."""
        return [
            "eleven_monolingual_v1",    # English only, fast
            "eleven_multilingual_v1",   # Multi-language
            "eleven_multilingual_v2",   # Improved multi-language
            "eleven_turbo_v2",          # Fastest, lower latency
            "eleven_turbo_v2_5",        # Latest turbo (default)
        ]

    def list_voices(self) -> Dict[str, str]:
        """
        List available pre-made voices.

        Returns:
            Dict mapping voice names to voice IDs
        """
        return self.PREMADE_VOICES.copy()

    def generate_speech(
        self,
        text: str,
        voice_id: str = None,
        voice_name: str = None,
        model_id: str = None,
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        style: float = 0.0,
        use_speaker_boost: bool = True,
        optimize_streaming_latency: int = 0,
        output_format: str = "mp3_44100_128",
        **kwargs
    ) -> AudioResponse:
        """
        Generate speech from text using ElevenLabs TTS.

        Args:
            text: Text to convert (max ~5000 chars for free tier)
            voice_id: Voice ID (overrides voice_name)
            voice_name: Voice name (e.g., "rachel", "drew") - converted to ID
            model_id: Model override (default: self.model)
            stability: 0.0-1.0, more stable = less expressive (default: 0.5)
            similarity_boost: 0.0-1.0, voice clarity boost (default: 0.75)
            style: 0.0-1.0, style exaggeration (v2+ only, default: 0.0)
            use_speaker_boost: Improve clarity (default: True)
            optimize_streaming_latency: 0-4, higher = faster but less accurate
            output_format: Audio format (default: "mp3_44100_128")
            **kwargs: Additional parameters

        Returns:
            AudioResponse with audio_data (bytes), model, metadata

        Raises:
            ValueError: Invalid parameters
            requests.HTTPError: API errors
        """
        # Validate text
        if not text or len(text.strip()) == 0:
            raise ValueError("Text cannot be empty")

        if len(text) > 5000:
            raise ValueError(f"Text too long: {len(text)} characters (max 5000)")

        # Resolve voice ID
        if voice_name and not voice_id:
            # Try to map friendly name to ID
            voice_id = self.PREMADE_VOICES.get(voice_name.lower())
            if not voice_id:
                raise ValueError(
                    f"Unknown voice name: {voice_name}. "
                    f"Available: {', '.join(sorted(self.PREMADE_VOICES.keys()))}"
                )

        # Default voice if none specified
        if not voice_id:
            voice_id = self.PREMADE_VOICES["rachel"]  # Default to Rachel

        model_id = model_id or self.model

        # Build request payload
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": max(0.0, min(1.0, stability)),
                "similarity_boost": max(0.0, min(1.0, similarity_boost)),
            }
        }

        # Add v2+ features if using compatible model
        if "v2" in model_id.lower() or "turbo" in model_id.lower():
            payload["voice_settings"]["style"] = max(0.0, min(1.0, style))
            payload["voice_settings"]["use_speaker_boost"] = use_speaker_boost

        # Optional streaming optimization
        if optimize_streaming_latency > 0:
            payload["optimize_streaming_latency"] = min(4, optimize_streaming_latency)

        # API request
        url = f"{self.API_BASE}/text-to-speech/{voice_id}"

        try:
            response = self.session.post(
                url,
                json=payload,
                headers={"Accept": f"audio/{output_format.split('_')[0]}"},
                timeout=30
            )
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            # Provide helpful error messages
            if e.response.status_code == 401:
                raise ValueError("Invalid ElevenLabs API key") from e
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded (check your ElevenLabs quota)") from e
            elif e.response.status_code == 422:
                raise ValueError(f"Invalid request parameters: {e.response.text}") from e
            else:
                raise ValueError(f"ElevenLabs API error: {e.response.status_code}") from e

        except requests.exceptions.Timeout:
            raise ValueError("ElevenLabs API timeout (30s exceeded)")

        return AudioResponse(
            audio_data=response.content,
            model=model_id,
            metadata={
                "voice_id": voice_id,
                "voice_name": voice_name,
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style if "v2" in model_id.lower() else None,
                "characters": len(text),
                "output_format": output_format,
                "size_bytes": len(response.content)
            }
        )
