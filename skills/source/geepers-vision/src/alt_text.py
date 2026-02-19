"""
AltFlow Pattern: Accessible Alt Text Generation
Updated for Geepers Vision Skill
"""

from typing import Union, Dict, Any
from .client import VisionClient

ALTTEXT_SYSTEM_PROMPT = """You are an Alt Text Specialist providing precise, accessible alt text for digital images. 

Requirements:
1. Depict essential visuals and visible text accurately
2. Avoid social-emotional context unless explicitly requested
3. Do not speculate on intentions
4. Start directly with the description (NO "Alt text:" prefix)
5. Character limit: ~700 characters
6. Identify famous people/characters if clear
"""

def generate_alt_text(
    client: VisionClient,
    image_path: str,
    include_context: bool = False
) -> Dict[str, Any]:
    
    prompt = "Generate accessible alt text for this image."
    sys_prompt = ALTTEXT_SYSTEM_PROMPT
    
    if include_context:
        sys_prompt += "\nUser requested social-emotional context. Include relevant interpretive details."

    result = client.analyze_image(
        image_path, 
        prompt=prompt, 
        system_prompt=sys_prompt,
        detail="low" # Alt text usually doesn't need pixel-peeping high res
    )
    
    alt_text = result.description
    
    # Post-processing cleanup
    if alt_text.lower().startswith("alt text:"):
        alt_text = alt_text[9:].strip()
        
    return {
        "alt_text": alt_text,
        "success": result.success,
        "error": result.error
    }
