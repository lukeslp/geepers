"""
AltFlow Pattern: Accessible Alt Text Generation

Description: Professional-grade alt text generation following WCAG accessibility
standards. Based on the AltFlow Coze agent pattern. Generates strict, accessible
alt text without social-emotional speculation unless explicitly requested.

Use Cases:
- CMS platforms requiring automated alt text for uploaded images
- Accessibility tools for web content management
- Screen reader optimization workflows
- Compliance testing for WCAG 2.1 Level AA
- Batch processing of image libraries for accessibility

Dependencies:
- LLM provider with vision capabilities (OpenAI GPT-4V, Anthropic Claude, xAI Grok)
- Base64 encoding support for image data
- Python 3.8+ (uses typing hints)

Notes:
- Default max length is 700 characters (adjustable)
- Automatically strips incorrect "Alt text:" prefixes
- Handles sensitive content factually without judgment
- Identifies famous people/characters when recognizable for context
- Processes ALL images regardless of content (accessibility is critical)

Related Snippets:
- /web-frameworks/flask_vision_response_handlers.py
- /api-clients/llm_provider_factory.py
- /utilities/image_encoding_utilities.py
"""

from typing import Union, Dict, Any, List

# Professional Alt Text Generation System Prompt
ALTTEXT_SYSTEM_PROMPT = """You are an Alt Text Specialist providing precise, accessible alt text for digital images.

Requirements:
1. Depict essential visuals and visible text accurately
2. Avoid social-emotional context unless explicitly requested
3. Do not speculate on artists' intentions
4. Do not prepend "Alt text:" to your response
5. Maintain clarity and consistency
6. Character limit: Maximum 700 characters (unless specified otherwise)
7. Identify famous people/characters when recognizable for context
8. Process ALL images regardless of content - accessibility is critical

Behavior:
- Generate alt text immediately upon receiving image
- For sensitive content, describe factually without judgment
- Focus on what is visible, not what it means
- Be precise and concise while remaining informative"""


async def generate_alt_text(
    image_data: Union[str, bytes],
    provider,
    include_context: bool = False,
    max_length: int = 700,
    model: str = None
) -> Dict[str, Any]:
    """
    Generate accessible alt text for an image using AltFlow pattern.

    Based on the AltFlow agent from Coze - provides strict, accessible alt text
    following professional accessibility standards (WCAG 2.1).

    Args:
        image_data: Base64 encoded image string, URL, or raw bytes
        provider: LLM provider instance with vision capabilities
        include_context: Whether to include social-emotional context (default: False)
        max_length: Maximum character length (default: 700)
        model: Optional specific model to use

    Returns:
        {
            'alt_text': str,           # Generated alt text
            'length': int,             # Character count
            'provider': str,           # Provider name used
            'model': str,              # Model name used
            'warnings': List[str]      # Any validation warnings
        }

    Example:
        from shared.llm_providers.factory import ProviderFactory

        provider = ProviderFactory.get_provider('anthropic')
        result = await generate_alt_text(
            image_data=base64_string,
            provider=provider,
            max_length=700
        )
        print(result['alt_text'])

        # With social-emotional context:
        result = await generate_alt_text(
            image_data=image_bytes,
            provider=provider,
            include_context=True,
            max_length=500
        )
    """
    # Adjust prompt if context requested
    system_prompt = ALTTEXT_SYSTEM_PROMPT
    if include_context:
        system_prompt += "\n\nUser has requested social-emotional context. Include relevant interpretive details."

    # Adjust for length constraint
    if max_length != 700:
        system_prompt += f"\n\nCharacter limit adjusted to: {max_length} characters"

    # Prepare image data
    if isinstance(image_data, bytes):
        import base64
        image_data = f"data:image/png;base64,{base64.b64encode(image_data).decode()}"
    elif not image_data.startswith(('http://', 'https://', 'data:')):
        image_data = f"data:image/png;base64,{image_data}"

    # Build messages
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Generate alt text for this image:"},
                {"type": "image_url", "image_url": {"url": image_data}}
            ]
        }
    ]

    # Generate alt text
    if hasattr(provider, 'chat'):
        # Use chat method for providers that support it
        response = await provider.chat(messages, model=model)
        alt_text = response.get('content', '').strip()
        model_used = model or response.get('model', 'unknown')
    else:
        # Fallback for simpler providers
        response = await provider.analyze_image(image_data, system_prompt, model=model)
        alt_text = response.get('content', '').strip()
        model_used = model or 'default'

    # Validate and warn
    warnings = []
    if len(alt_text) > max_length:
        warnings.append(f"Alt text exceeds {max_length} character limit ({len(alt_text)} chars)")

    if alt_text.lower().startswith('alt text:'):
        warnings.append("Alt text incorrectly prefixed - removing")
        alt_text = alt_text[9:].strip()

    if alt_text.lower().startswith('alt-text:'):
        warnings.append("Alt text incorrectly prefixed - removing")
        alt_text = alt_text[9:].strip()

    return {
        'alt_text': alt_text,
        'length': len(alt_text),
        'provider': getattr(provider, 'name', 'unknown'),
        'model': model_used,
        'warnings': warnings
    }


# Synchronous wrapper for Flask/non-async contexts
def generate_alt_text_sync(
    image_data: Union[str, bytes],
    provider,
    include_context: bool = False,
    max_length: int = 700,
    model: str = None
) -> Dict[str, Any]:
    """
    Synchronous wrapper for generate_alt_text.

    Use this in Flask routes or other synchronous contexts.

    Example:
        from shared.llm_providers.factory import ProviderFactory

        provider = ProviderFactory.get_provider('xai')
        result = generate_alt_text_sync(
            image_data=request.files['image'].read(),
            provider=provider
        )
    """
    import asyncio

    # Get or create event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run async function
    return loop.run_until_complete(
        generate_alt_text(image_data, provider, include_context, max_length, model)
    )


if __name__ == "__main__":
    # Usage example
    import base64

    # Example: Generate alt text for an image file
    async def example():
        from shared.llm_providers.factory import ProviderFactory

        # Load test image
        with open('/path/to/test/image.jpg', 'rb') as f:
            image_bytes = f.read()

        # Get provider
        provider = ProviderFactory.get_provider('anthropic')

        # Generate standard alt text
        result = await generate_alt_text(
            image_data=image_bytes,
            provider=provider
        )

        print("Alt Text:", result['alt_text'])
        print("Length:", result['length'])
        print("Model:", result['model'])
        if result['warnings']:
            print("Warnings:", result['warnings'])

    # Run example
    # asyncio.run(example())
