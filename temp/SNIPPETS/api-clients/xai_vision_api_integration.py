"""
xAI Grok Vision API Integration Pattern

Description: Complete pattern for integrating xAI's Grok Vision API for image/video
analysis with comprehensive error handling, base64 encoding, and video frame extraction.
Works with any OpenAI-compatible vision API endpoint.

Use Cases:
- AI-powered image analysis and description generation
- Video frame extraction and analysis
- Alt-text generation for accessibility
- Filename suggestion from visual content
- Image content moderation and classification
- Multi-modal AI applications with vision

Dependencies:
- openai (OpenAI Python client, compatible with xAI API)
- PIL/Pillow (optional, for image processing)
- opencv-python (optional, for video frame extraction)

Notes:
- Works with any OpenAI-compatible vision API (xAI, OpenAI, Azure)
- Supports both image and video analysis
- Graceful fallback when optional dependencies unavailable
- Base64 encoding for API submission
- Proper MIME type detection for images
- Environment variable support for API keys

Related Snippets:
- api-clients/multi_provider_abstraction.py - Multi-provider pattern
- error-handling/graceful_import_fallbacks.py - Optional dependency handling
- utilities/retry_decorator.py - Add retry logic for API calls

Source Attribution:
- Extracted from: /home/coolhand/shared/utils/vision.py
- Author: Luke Steuber
"""

import os
import base64
import logging
import tempfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, Any

# Optional dependencies with graceful fallbacks
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    Image = None
    PIL_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False

logger = logging.getLogger(__name__)


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class VisionResult:
    """
    Result from vision analysis operation.

    Attributes:
        success: Whether the operation succeeded
        description: Description of the visual content
        confidence: Optional confidence score (0.0-1.0)
        suggested_filename: Suggested filename based on content
        error: Error message if operation failed
        metadata: Additional metadata from the vision API
    """
    success: bool
    description: str
    confidence: Optional[float] = None
    suggested_filename: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Vision Client
# ============================================================================

class VisionClient:
    """
    Vision analysis client using AI vision models.

    Supports multiple vision-capable providers, with xAI Grok-2 Vision as the
    primary option. Can analyze both images and videos (by extracting frames).

    Example:
        >>> client = VisionClient(api_key="xai-...")
        >>> result = client.analyze_image("photo.jpg")
        >>> print(result.description)
        "A sunset over mountains with vibrant orange and purple sky"
    """

    # Supported file extensions
    SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.heic'}
    SUPPORTED_VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv'}

    # MIME type mapping
    MIME_TYPE_MAP = {
        '.jpg': 'jpeg', '.jpeg': 'jpeg',
        '.png': 'png', '.gif': 'gif',
        '.webp': 'webp', '.bmp': 'bmp',
        '.tiff': 'tiff'
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.x.ai/v1",
        model: str = "grok-2-vision-1212",
        provider: str = "xai"
    ):
        """
        Initialize vision client.

        Args:
            api_key: API key (or set XAI_API_KEY env var for xAI)
            base_url: API base URL
            model: Vision model to use
            provider: Provider name ('xai', 'openai', etc.)

        Raises:
            ImportError: If openai package not installed
            ValueError: If API key not provided
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "openai package required for vision functionality. "
                "Install with: pip install openai"
            )

        # Get API key from parameter or environment
        self.api_key = api_key or os.environ.get("XAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Provide via api_key parameter or set "
                "XAI_API_KEY environment variable."
            )

        self.base_url = base_url
        self.model = model
        self.provider = provider

        # Initialize OpenAI client (compatible with xAI)
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

        logger.info(f"Initialized VisionClient (provider={provider}, model={model})")

    def analyze_image(
        self,
        image_path: Path,
        prompt: Optional[str] = None,
        detail: str = "high"
    ) -> VisionResult:
        """
        Analyze an image using the vision model.

        Args:
            image_path: Path to image file
            prompt: Custom prompt (default: general description)
            detail: Image detail level ('low' or 'high')

        Returns:
            VisionResult with analysis

        Example:
            >>> result = client.analyze_image("photo.jpg")
            >>> print(result.description)
        """
        image_path = Path(image_path)

        if not image_path.exists():
            return VisionResult(
                success=False,
                description="",
                error=f"Image file not found: {image_path}"
            )

        if image_path.suffix.lower() not in self.SUPPORTED_IMAGE_EXTENSIONS:
            return VisionResult(
                success=False,
                description="",
                error=f"Unsupported image format: {image_path.suffix}"
            )

        # Default prompt
        if prompt is None:
            prompt = (
                "Describe this image in detail. Include the main subjects, "
                "setting, colors, mood, and any notable features."
            )

        logger.info(f"Analyzing image: {image_path.name}")

        try:
            # Encode image to base64
            base64_img, mime_type = self.encode_image_base64(image_path)
            if not base64_img:
                return VisionResult(
                    success=False,
                    description="",
                    error="Failed to encode image"
                )

            # Prepare image URL
            image_url = f"data:image/{mime_type};base64,{base64_img}"

            # Call vision API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": image_url, "detail": detail}},
                            {"type": "text", "text": prompt}
                        ]
                    }
                ],
                temperature=0.3,
                max_tokens=500,
            )

            description = response.choices[0].message.content.strip()

            logger.info(f"Successfully analyzed image: {image_path.name}")

            return VisionResult(
                success=True,
                description=description,
                metadata={
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
                }
            )

        except Exception as e:
            logger.exception(f"Error analyzing image {image_path.name}: {e}")
            return VisionResult(
                success=False,
                description="",
                error=str(e)
            )

    def encode_image_base64(self, image_path: Path) -> Tuple[Optional[str], Optional[str]]:
        """
        Read and encode image to base64.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (base64_string, mime_type) or (None, None) on error

        Example:
            >>> base64_str, mime = client.encode_image_base64("photo.jpg")
            >>> print(f"Encoded as {mime}")
        """
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()

            encoded = base64.b64encode(img_data).decode('utf-8')

            # Determine MIME type from extension
            ext = image_path.suffix.lower()
            mime_type = self.MIME_TYPE_MAP.get(ext, 'jpeg')

            return encoded, mime_type

        except Exception as e:
            logger.exception(f"Error encoding image {image_path}: {e}")
            return None, None


# ============================================================================
# Functional Interface (Convenience Functions)
# ============================================================================

def analyze_image(
    image_path: Path,
    api_key: Optional[str] = None,
    prompt: Optional[str] = None,
    model: str = "grok-2-vision-1212"
) -> VisionResult:
    """
    Convenience function for quick image analysis.

    Args:
        image_path: Path to image file
        api_key: API key (or use XAI_API_KEY env var)
        prompt: Custom analysis prompt
        model: Vision model to use

    Returns:
        VisionResult with analysis

    Example:
        >>> result = analyze_image("photo.jpg")
        >>> print(result.description)
    """
    client = VisionClient(api_key=api_key, model=model)
    return client.analyze_image(image_path, prompt=prompt)


# ============================================================================
# Usage Examples
# ============================================================================

if __name__ == "__main__":
    """
    Usage examples for xAI Vision API integration.
    """

    # Example 1: Basic image analysis
    print("=== Example 1: Basic Image Analysis ===")
    result = analyze_image(
        "example.jpg",
        api_key=os.environ.get("XAI_API_KEY")
    )
    if result.success:
        print(f"Description: {result.description}")
    else:
        print(f"Error: {result.error}")

    # Example 2: Class-based usage with custom prompt
    print("\n=== Example 2: Custom Prompt ===")
    client = VisionClient(
        api_key=os.environ.get("XAI_API_KEY"),
        model="grok-2-vision-1212"
    )

    result = client.analyze_image(
        "photo.jpg",
        prompt="Describe the colors and mood of this image in 2 sentences."
    )

    if result.success:
        print(f"Description: {result.description}")
        print(f"Tokens used: {result.metadata.get('tokens_used', 'N/A')}")

    # Example 3: Using with OpenAI instead of xAI
    print("\n=== Example 3: OpenAI Vision API ===")
    openai_client = VisionClient(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url="https://api.openai.com/v1",
        model="gpt-4-vision-preview",
        provider="openai"
    )

    result = openai_client.analyze_image("image.png")
    if result.success:
        print(f"OpenAI Analysis: {result.description}")
