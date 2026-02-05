#!/usr/bin/env python3
"""
Vision API Client for Geepers Vision Skill
Supports xAI, OpenAI, and Anthropic vision models.
"""

import os
import base64
import logging
import tempfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, Any

# Required dependency
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class VisionResult:
    success: bool
    description: str
    confidence: Optional[float] = None
    suggested_filename: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class VisionClient:
    SUPPORTED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.heic'}
    SUPPORTED_VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.webm'}
    
    MIME_TYPE_MAP = {
        '.jpg': 'jpeg', '.jpeg': 'jpeg',
        '.png': 'png', '.gif': 'gif',
        '.webp': 'webp', 
        '.heic': 'heic'
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = None,
        model: str = "gpt-4o", # Defaulting to GPT-4o or similar high-end vision
        provider: str = "openai"
    ):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package required.")

        self.api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("XAI_API_KEY")
        
        # Smart Text-to-Provider mapping
        if not base_url:
            if "xai" in str(api_key): # Heuristic
                base_url = "https://api.x.ai/v1"
                self.model = "grok-2-vision-1212"
            else:
                base_url = "https://api.openai.com/v1"
                self.model = model
        
        self.base_url = base_url
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        logger.info(f"Initialized VisionClient (base_url={base_url})")

    def analyze_image(
        self,
        image_path: Path,
        prompt: Optional[str] = None,
        detail: str = "high",
        system_prompt: str = None
    ) -> VisionResult:
        image_path = Path(image_path)
        if not image_path.exists():
            return VisionResult(False, "", error=f"File not found: {image_path}")

        try:
            base64_img, mime_type = self.encode_image_base64(image_path)
            image_url = f"data:image/{mime_type};base64,{base64_img}"
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            user_content = [
                {"type": "image_url", "image_url": {"url": image_url, "detail": detail}},
                {"type": "text", "text": prompt or "Describe this image."}
            ]
            
            messages.append({"role": "user", "content": user_content})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.2
            )
            
            return VisionResult(
                success=True,
                description=response.choices[0].message.content.strip(),
                metadata={"model": self.model}
            )

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return VisionResult(False, "", error=str(e))

    def analyze_video(self, video_path: Path, prompt: str = None) -> VisionResult:
        """Simple frame extraction analysis for video"""
        if not CV2_AVAILABLE:
            return VisionResult(False, "", error="OpenCV not installed.")
            
        # Extract middle frame
        path = self.extract_video_frame(video_path, 0.5)
        if path:
            res = self.analyze_image(path, prompt, detail="high")
            path.unlink() # cleanup
            return res
        return VisionResult(False, "", error="Frame extraction failed.")

    def extract_video_frame(self, video_path: Path, position: float) -> Optional[Path]:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened(): return None
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(total * position))
        ret, frame = cap.read()
        cap.release()
        if not ret: return None
        
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            cv2.imwrite(f.name, frame)
            return Path(f.name)

    def encode_image_base64(self, image_path: Path) -> Tuple[str, str]:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8"), self.MIME_TYPE_MAP.get(image_path.suffix.lower(), "jpeg")
