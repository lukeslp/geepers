#!/usr/bin/env python3
import sys
import json
import logging
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__)))
from client import VisionClient
import alt_text as alt_flow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vision-mcp")

# Initialize Client
# We check for keys. If multiple are present, we prefer OpenAI/xAI as per client logic.
# The user explicitly asked for "No Ollama", which is handled by our Client only supporting OpenAI compatible APIs.
try:
    client = VisionClient()
except Exception as e:
    client = None
    logger.error(f"Failed to init VisionClient: {e}")

# Specialist Prompts
SAFETY_SYSTEM_PROMPT = """You are a Certified Safety Expert and Risk Assessor.
Analyze this image for:
1. Potential hazards (OSHA violations, fire risks, trip hazards)
2. PPE compliance (Helmest, vests, glasses)
3. Environmental risks
4. Structural integrity concerns

Provide a structured report with severity ratings (LOW/MED/HIGH) for each finding.
"""

SCHEMATIC_SYSTEM_PROMPT = """You are a Senior Engineering Lead specializing in blueprints, schematics, and technical diagrams.
Analyze this technical document/image for:
1. Components and their relationships
2. Dimensions and tolerances
3. potential design issues or flaws
4. Compliance with standard engineering practices

Be extremely detailed. Do not summarize; extract full fidelity technical data.
"""

def list_tools():
    return [
        {
            "name": "dream_vision_analyze",
            "description": "General purpose visual analysis of an image or video path.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to image or video file"},
                    "prompt": {"type": "string", "description": "Question or instruction for analysis"}
                },
                "required": ["path"]
            }
        },
        {
            "name": "dream_vision_alt_text",
            "description": "Generate WCAG-compliant alt text for an image.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to image file"},
                    "context": {"type": "boolean", "description": "Include social/emotional context?", "default": False}
                },
                "required": ["path"]
            }
        },
        {
            "name": "dream_vision_safety_eval",
            "description": "Evaluate an image for safety hazards, PPE compliance, and risks.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to image/video"}
                },
                "required": ["path"]
            }
        },
        {
            "name": "dream_vision_schematic",
            "description": "Analyze engineering schematics, blueprints, or technical diagrams in high detail.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to schematic"},
                    "focus": {"type": "string", "description": "Specific area/component to focus on"}
                },
                "required": ["path"]
            }
        },
        {
            "name": "dream_vision_rename",
            "description": "Generate a descriptive file name based on visual content.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute path to file"}
                },
                "required": ["path"]
            }
        }
    ]

def handle_call_tool(name, arguments):
    if not client:
        return {"content": [{"type": "text", "text": "Error: Vision Client not initialized. Check API Keys (OPENAI_API_KEY or XAI_API_KEY)."}], "isError": True}

    path = arguments["path"]
    if not os.path.exists(path):
        return {"content": [{"type": "text", "text": f"Error: File not found at {path}"}], "isError": True}

    try:
        # Determine if Video or Image
        is_video = str(path).lower().endswith(tuple(client.SUPPORTED_VIDEO_EXTENSIONS))
        method = client.analyze_video if is_video else client.analyze_image

        if name == "dream_vision_analyze":
            prompt = arguments.get("prompt", "Describe this in detail.")
            res = method(path, prompt=prompt)
            
        elif name == "dream_vision_alt_text":
            if is_video:
                 return {"content": [{"type": "text", "text": "Alt text tool doesn't support video yet."}], "isError": True}
            res_dict = alt_flow.generate_alt_text(client, path, arguments.get("context", False))
            if res_dict["success"]:
                 return {"content": [{"type": "text", "text": res_dict["alt_text"]}]}
            else:
                 return {"content": [{"type": "text", "text": f"Error: {res_dict['error']}"}], "isError": True}

        elif name == "dream_vision_safety_eval":
            # Safety Eval always uses the specialist system prompt
            # For video, analyze_video extracts a frame, so we pass the system prompt context differently if needed
            # But the client.analyze_video relies on analyze_image, so we need to ensure system_prompt is passed through if we refactor client
            # The current simple client.analyze_image supports system_prompt.
            # However, client.analyze_video calls analyze_image. Let's handle image directly for now with full control.
            
            if is_video:
                # Video Safety: Extract frame first manually to pass system prompt? 
                # Or just trust the general prompt. Let's use the method but with the prompt payload.
                res = client.analyze_video(path, prompt="Evaluate this video frame for safety hazards and PPE compliance.")
            else:
                res = client.analyze_image(path, prompt="Perform a comprehensive safety evaluation.", system_prompt=SAFETY_SYSTEM_PROMPT)

        elif name == "dream_vision_schematic":
            focus = arguments.get("focus", "")
            prompt = f"Analyze this schematic. {f'Focus on: {focus}' if focus else ''}"
            if is_video:
                 res = client.analyze_video(path, prompt=prompt)
            else:
                 res = client.analyze_image(path, prompt=prompt, system_prompt=SCHEMATIC_SYSTEM_PROMPT, detail="high")

        elif name == "dream_vision_rename":
            # Simple prompt for rename
            prompt = "Generate a concise, descriptive filename (lowercase, underscores) for this visual."
            if is_video:
                res = client.analyze_video(path, prompt=prompt)
            else:
                res = client.analyze_image(path, prompt=prompt)
            
            # Post-process response to get just the filename
            if res.success:
                return {"content": [{"type": "text", "text": res.description.strip().replace(" ", "_").lower()[:50]}]}

        else:
             return {"content": [{"type": "text", "text": f"Tool not found: {name}"}], "isError": True}

        if res.success:
            return {"content": [{"type": "text", "text": res.description}]}
        else:
            return {"content": [{"type": "text", "text": f"Vision API Error: {res.error}"}], "isError": True}

    except Exception as e:
        return {"content": [{"type": "text", "text": f"Server Error: {str(e)}"}], "isError": True}

def run_server():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            request = json.loads(line)
            req_id = request.get("id")
            
            response = {"jsonrpc": "2.0", "id": req_id}
            
            if request.get("method") == "initialize":
                response["result"] = {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "geepers-vision", "version": "1.0.0"}
                }
            elif request.get("method") == "tools/list":
                response["result"] = {"tools": list_tools()}
            elif request.get("method") == "tools/call":
                result = handle_call_tool(request["params"]["name"], request["params"]["arguments"])
                if result.get("isError"):
                     response["error"] = {"code": -32603, "message": result["content"][0]["text"]}
                else:
                     response["result"] = result
            else:
                continue
                
            print(json.dumps(response), flush=True)
        except Exception:
            break

if __name__ == "__main__":
    run_server()
