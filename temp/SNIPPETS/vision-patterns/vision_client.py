#!/usr/bin/env python3
"""
Vision API Client

Description: Comprehensive vision analysis client for image and video analysis
             using AI vision models (xAI Grok Vision, OpenAI Vision, etc.)
             with structured results and convenience functions.

Use Cases:
- Image description and alt text generation
- Video analysis via frame extraction
- AI-powered filename generation from visual content
- Accessibility applications (describing images)
- Content moderation and classification
- Visual search and cataloging

Dependencies:
- openai (pip install openai) - Required for API access
- Pillow (optional, for image processing)
- opencv-python (optional, for video frame extraction)

Notes:
- Compatible with OpenAI-compatible vision APIs (xAI, OpenAI, etc.)
- Graceful fallbacks when optional dependencies unavailable
- VisionResult dataclass for structured responses
- Supports both images and videos (via frame extraction)
- Default: xAI Grok-2 Vision model

Related Snippets:
- api-clients/multi_provider_abstraction.py
- utilities/retry_decorator.py

Source Attribution:
- Extracted from: /home/coolhand/projects/packages/working/vision-utils/
- Author: Luke Steuber
"""

from __future__ import annotations

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


# =============================================================================
# DATA CLASSES
# =============================================================================

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


# =============================================================================
# VISION CLIENT
# =============================================================================

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

        >>> result = client.generate_filename("photo.jpg")
        >>> print(result.suggested_filename)
        "sunset_mountains_orange_purple"
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

    def analyze_video(
        self,
        video_path: Path,
        frame_position: float = 0.3,
        prompt: Optional[str] = None
    ) -> VisionResult:
        """
        Analyze a video by extracting and analyzing a representative frame.

        Args:
            video_path: Path to video file
            frame_position: Position to extract frame (0.0 to 1.0, default 0.3 = 30%)
            prompt: Custom prompt for analysis

        Returns:
            VisionResult with analysis

        Example:
            >>> result = client.analyze_video("video.mp4", frame_position=0.5)
            >>> print(result.description)
        """
        video_path = Path(video_path)

        if not video_path.exists():
            return VisionResult(
                success=False,
                description="",
                error=f"Video file not found: {video_path}"
            )

        if video_path.suffix.lower() not in self.SUPPORTED_VIDEO_EXTENSIONS:
            return VisionResult(
                success=False,
                description="",
                error=f"Unsupported video format: {video_path.suffix}"
            )

        logger.info(f"Analyzing video: {video_path.name}")

        # Extract frame from video
        frame_path = self.extract_video_frame(video_path, frame_position)
        if not frame_path:
            return VisionResult(
                success=False,
                description="",
                error="Failed to extract video frame (requires opencv-python)"
            )

        try:
            # Analyze the extracted frame
            result = self.analyze_image(frame_path, prompt)

            # Add video metadata
            if result.success:
                result.metadata["source_type"] = "video"
                result.metadata["frame_position"] = frame_position

            return result

        finally:
            # Clean up temporary frame file
            if frame_path and frame_path.exists():
                try:
                    frame_path.unlink()
                except Exception as e:
                    logger.warning(f"Failed to delete temp frame: {e}")

    def generate_filename(
        self,
        file_path: Path,
        max_words: int = 5,
        lowercase: bool = True
    ) -> VisionResult:
        """
        Generate a descriptive filename based on visual content.

        Args:
            file_path: Path to image or video file
            max_words: Maximum words in filename (default: 5)
            lowercase: Convert to lowercase (default: True)

        Returns:
            VisionResult with suggested_filename populated

        Example:
            >>> result = client.generate_filename("IMG_1234.jpg")
            >>> print(result.suggested_filename)
            "sunset_beach_waves_orange"
        """
        file_path = Path(file_path)

        # Custom prompt for filename generation
        prompt = (
            f"Analyze this image and generate a descriptive filename using {max_words} words or less. "
            "Use only lowercase letters, numbers, and underscores between words. "
            "Be concise and descriptive. Return ONLY the filename, nothing else. "
            "Example format: blue_sky_mountains_sunset or cat_sitting_window"
        )

        # Determine if it's an image or video
        if file_path.suffix.lower() in self.SUPPORTED_IMAGE_EXTENSIONS:
            result = self.analyze_image(file_path, prompt=prompt)
        elif file_path.suffix.lower() in self.SUPPORTED_VIDEO_EXTENSIONS:
            result = self.analyze_video(file_path, prompt=prompt)
        else:
            return VisionResult(
                success=False,
                description="",
                error=f"Unsupported file format: {file_path.suffix}"
            )

        if not result.success:
            return result

        # Clean and format the filename
        filename = result.description.strip()

        if lowercase:
            filename = filename.lower()

        # Remove quotes, punctuation
        filename = filename.strip('"\'`.')

        # Replace spaces and hyphens with underscores
        filename = filename.replace(' ', '_').replace('-', '_')

        # Remove non-alphanumeric except underscores
        filename = ''.join(c for c in filename if c.isalnum() or c == '_')

        # Remove multiple underscores
        while '__' in filename:
            filename = filename.replace('__', '_')

        filename = filename.strip('_')

        # Update result with cleaned filename
        result.suggested_filename = filename

        logger.info(f"Generated filename: {filename}")

        return result

    def extract_video_frame(
        self,
        video_path: Path,
        frame_position: float = 0.3
    ) -> Optional[Path]:
        """
        Extract a frame from video file at specified position.

        Args:
            video_path: Path to video file
            frame_position: Position in video (0.0 to 1.0)

        Returns:
            Path to temporary frame file, or None on error

        Note:
            Caller is responsible for deleting the temporary file
        """
        if not CV2_AVAILABLE:
            logger.error("opencv-python not installed. Cannot extract video frames.")
            return None

        try:
            # Open video
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                logger.error(f"Failed to open video: {video_path}")
                return None

            # Get total frames
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames <= 0:
                logger.error(f"Unable to determine video length: {video_path}")
                cap.release()
                return None

            # Calculate target frame
            target_frame = int(total_frames * frame_position)

            # Seek to target frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

            # Read the frame
            ret, frame = cap.read()
            cap.release()

            if not ret or frame is None:
                logger.error(f"Failed to extract frame from video: {video_path}")
                return None

            # Save frame to temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                temp_path = Path(tmp_file.name)
                cv2.imwrite(str(temp_path), frame)

            logger.info(f"Extracted frame from {video_path.name} at position {frame_position}")

            return temp_path

        except Exception as e:
            logger.exception(f"Error extracting frame from {video_path}: {e}")
            return None

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


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

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


def analyze_video(
    video_path: Path,
    api_key: Optional[str] = None,
    frame_position: float = 0.3,
    prompt: Optional[str] = None,
    model: str = "grok-2-vision-1212"
) -> VisionResult:
    """
    Convenience function for quick video analysis.

    Args:
        video_path: Path to video file
        api_key: API key (or use XAI_API_KEY env var)
        frame_position: Position to extract frame (0.0-1.0)
        prompt: Custom analysis prompt
        model: Vision model to use

    Returns:
        VisionResult with analysis

    Example:
        >>> result = analyze_video("video.mp4", frame_position=0.5)
        >>> print(result.description)
    """
    client = VisionClient(api_key=api_key, model=model)
    return client.analyze_video(video_path, frame_position=frame_position, prompt=prompt)


def generate_filename(
    file_path: Path,
    api_key: Optional[str] = None,
    max_words: int = 5,
    model: str = "grok-2-vision-1212"
) -> VisionResult:
    """
    Generate a descriptive filename from visual content.

    Args:
        file_path: Path to image or video file
        api_key: API key (or use XAI_API_KEY env var)
        max_words: Maximum words in filename
        model: Vision model to use

    Returns:
        VisionResult with suggested_filename

    Example:
        >>> result = generate_filename("IMG_1234.jpg")
        >>> print(result.suggested_filename)
        "sunset_beach_waves"
    """
    client = VisionClient(api_key=api_key, model=model)
    return client.generate_filename(file_path, max_words=max_words)


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

if __name__ == "__main__":
    print("Vision Client Demo")
    print("=" * 50)

    print("\n1. Dependency Status:")
    print(f"   OpenAI available: {OPENAI_AVAILABLE}")
    print(f"   PIL available: {PIL_AVAILABLE}")
    print(f"   OpenCV available: {CV2_AVAILABLE}")

    if not OPENAI_AVAILABLE:
        print("\nERROR: openai package required")
        print("Install with: pip install openai")
        exit(1)

    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        print("\n2. API Key Status:")
        print("   XAI_API_KEY not set")
        print("   Set with: export XAI_API_KEY=your-key-here")
        print("\n3. Example usage (when API key is set):")
    else:
        print(f"\n2. API Key Status:")
        print(f"   Found: {api_key[:10]}...")
        print("\n3. VisionClient ready!")

    print("\n   # Analyze an image")
    print("   from vision_client import VisionClient, analyze_image")
    print("")
    print("   # Quick analysis")
    print("   result = analyze_image('photo.jpg')")
    print("   print(result.description)")
    print("")
    print("   # Advanced usage")
    print("   client = VisionClient()")
    print("   result = client.analyze_image('photo.jpg', prompt='Describe colors')")
    print("")
    print("   # Generate filename")
    print("   result = client.generate_filename('IMG_1234.jpg')")
    print("   print(result.suggested_filename)")
    print("")
    print("   # Analyze video (extracts frame)")
    print("   result = client.analyze_video('video.mp4', frame_position=0.5)")
