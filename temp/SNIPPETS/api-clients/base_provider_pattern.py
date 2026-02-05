"""
Abstract Base Provider Pattern for API Clients

Description: Reusable abstract base class pattern for implementing multi-provider API
integrations with consistent interfaces. Supports streaming responses, base64 encoding,
and standardized error handling.

Use Cases:
- Creating unified interfaces for multiple AI/ML providers
- Alt-text generation providers (Anthropic, xAI, OpenAI, etc.)
- LLM chat completion providers
- Image/file processing APIs
- Any multi-provider abstraction layer

Dependencies:
- abc (standard library)
- base64 (standard library)
- flask (for Response) - or adapt for your framework

Notes:
- Subclasses must implement the abstract generate() method
- Provides helper methods for common operations (base64, streaming)
- Framework-agnostic pattern - adapt Response for FastAPI/other frameworks
- Use type hints for better IDE support

Related Snippets:
- api-clients/xai_provider_implementation.py
- streaming-patterns/flask_streaming_response.py
- error-handling/provider_error_handling.py

Source:
Extracted from: /home/coolhand/projects/apis/api_v2/providers/base_provider.py
"""

import base64
from abc import ABC, abstractmethod
from typing import Generator, Any, Optional

# For Flask - replace with your framework's response type
from flask import Response


class BaseProvider(ABC):
    """
    Abstract base class for all API providers (e.g., alt-text generation, LLM completion).

    This pattern provides:
    - Consistent interface across multiple providers
    - Built-in base64 encoding for image/file data
    - Streaming response creation
    - Standardized provider naming
    """

    def __init__(self, name: str):
        """
        Initialize the provider with a unique name.

        Args:
            name: Unique identifier for this provider (e.g., "xai", "anthropic", "openai")
        """
        self.name = name

    @abstractmethod
    def generate(self, image_data: bytes, prompt: Optional[str] = None) -> Response:
        """
        Generate output for the given input data.

        This method MUST be implemented by all subclasses.

        Args:
            image_data: The input data (bytes for images/files)
            prompt: Optional custom prompt for generation

        Returns:
            Streaming response with the generated output

        Raises:
            NotImplementedError: If subclass doesn't implement this method
        """
        pass

    def image_to_base64(self, image_data: bytes) -> str:
        """
        Convert image/file data to base64 encoding.

        This is commonly needed for API requests that accept base64-encoded data.

        Args:
            image_data: The raw bytes data

        Returns:
            Base64 encoded string (decoded to UTF-8)

        Example:
            >>> provider = SomeProvider("test")
            >>> b64_data = provider.image_to_base64(image_bytes)
            >>> image_url = f"data:image/jpeg;base64,{b64_data}"
        """
        return base64.b64encode(image_data).decode('utf-8')

    def create_response(self, text_generator: Generator[str, None, None]) -> Response:
        """
        Create a streaming HTTP response from a text generator.

        This enables real-time streaming of generated content to clients.

        Args:
            text_generator: Generator that yields text chunks

        Returns:
            Streaming response with text/plain mimetype

        Example:
            >>> def generate_text():
            ...     for chunk in ["Hello", " ", "World"]:
            ...         yield chunk
            >>> response = provider.create_response(generate_text())
        """
        return Response(text_generator, mimetype="text/plain")


# Example implementation for xAI provider
class XaiProvider(BaseProvider):
    """Example concrete implementation for xAI API."""

    def __init__(self, api_key: str, model: str = "grok-2-vision-latest"):
        super().__init__("xai")
        self.api_key = api_key
        self.model = model
        # Initialize your API client here

    def generate(self, image_data: bytes, prompt: Optional[str] = None) -> Response:
        """
        Generate alt text using xAI API.

        Args:
            image_data: Image bytes
            prompt: Optional custom prompt

        Returns:
            Streaming response with generated text
        """
        # Convert image to base64
        image_b64 = self.image_to_base64(image_data)
        image_url = f"data:image/jpeg;base64,{image_b64}"

        # Prepare request
        default_prompt = "Describe this image in detail."
        messages = [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": prompt or default_prompt}
            ]
        }]

        def event_stream():
            try:
                # Make API call (pseudo-code - adapt for your client)
                # completion = self.client.chat.completions.create(...)
                # for chunk in completion:
                #     yield chunk.choices[0].delta.content
                yield "Generated text here"
            except Exception as e:
                yield f"Error: {e}"

        return self.create_response(event_stream())


if __name__ == "__main__":
    # Usage example
    print("BaseProvider Pattern")
    print("=" * 50)
    print("\nThis pattern provides a consistent interface for multiple API providers.")
    print("\nTo use:")
    print("1. Subclass BaseProvider")
    print("2. Implement the generate() method")
    print("3. Use helper methods: image_to_base64(), create_response()")
    print("\nExample providers: XAI, Anthropic, OpenAI, Google, Mistral")
