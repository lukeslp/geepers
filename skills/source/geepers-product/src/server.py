#!/usr/bin/env python3
import sys
import json
import logging
import os
from typing import Optional, Dict, Any

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("product-mcp")

# Clients
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False

# Prompt Library
PM_SYSTEM_PROMPT = """You are a Senior Product Manager and Strategy Lead.
Your goal is to analyze inputs to create professional, industry-standard product documentation.

Output Format: Markdown.
Tone: Professional, Strategic, Actionable.
"""

REVERSE_ENGINEER_PROMPT = """Analyze the provided code or description and Reverse Engineer it into a full Product Requirements Document (PRD).
Include:
1. Executive Summary
2. User Personas
3. User Stories / Functional Requirements
4. Technical Architecture Overview (inferred)
5. Success Metrics (KPIs)
"""

MARKET_PLAN_PROMPT = """Create a Go-To-Market (GTM) Strategy for the described product.
Include:
1. Target Audience & Segmentation
2. Value Proposition
3. Pricing Strategy (if applicable)
4. Distribution Channels
5. Launch Phases (Alpha, Beta, GA)
"""

CRITIQUE_PROMPT = """Perform a Brutal Honest Critique of this product concept.
Focus on:
1. Market Fit Gaps
2. User Experience Flaws
3. Technical Feasibility Risks
4. Competitive Threats
"""

class ProductClient:
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("XAI_API_KEY")
        base_url = None
        self.model = "gpt-4o"
        
        if api_key and "xai" in str(api_key): # Heuristic
             base_url = "https://api.x.ai/v1"
             self.model = "grok-2-1212"

        if not api_key:
            raise ValueError("Missing API Key (OPENAI_API_KEY or XAI_API_KEY)")
            
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, content: str, task_type: str) -> str:
        prompt_map = {
            "reverse_engineer": REVERSE_ENGINEER_PROMPT,
            "market_plan": MARKET_PLAN_PROMPT,
            "critique": CRITIQUE_PROMPT
        }
        
        specific_prompt = prompt_map.get(task_type, "")
        
        messages = [
            {"role": "system", "content": PM_SYSTEM_PROMPT},
            {"role": "user", "content": f"{specific_prompt}\n\nINPUT CONTENT:\n{content}"}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3 # Lower temp for structured docs
        )
        return response.choices[0].message.content

def list_tools():
    return [
        {
            "name": "dream_product_reverse_engineer",
            "description": "Reverse engineer code or descriptions into a detailed Product Requirements Document (PRD).",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Code snippet, file content, or project description"}
                },
                "required": ["content"]
            }
        },
        {
            "name": "dream_product_market_plan",
            "description": "Generate a comprehensive Go-To-Market (GTM) strategy.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Product description or PRD text"}
                },
                "required": ["description"]
            }
        },
        {
            "name": "dream_product_critique",
            "description": "Perform a critical analysis of a product concept.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Product idea or spec to critique"}
                },
                "required": ["content"]
            }
        },
        {
            "name": "dream_product_handoff",
            "description": "Format a Product Plan into an Engineering Handoff package for the Orchestration team.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "prd_content": {"type": "string", "description": "The approved PRD content"}
                },
                "required": ["prd_content"]
            }
        }
    ]

def run_server():
    client = None
    try:
        client = ProductClient()
    except Exception as e:
        logger.error(f"Failed to init ProductClient: {e}")

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
                    "serverInfo": {"name": "geepers-product", "version": "1.1.0"}
                }
            elif request.get("method") == "tools/list":
                response["result"] = {"tools": list_tools()}
            elif request.get("method") == "tools/call":
                if not client:
                     response["error"] = {"code": -32603, "message": "Product Client not initialized. Check API Keys."}
                else:
                    name = request["params"]["name"]
                    args = request["params"]["arguments"]
                    
                    try:
                        if name == "dream_product_reverse_engineer":
                            res = client.generate(args["content"], "reverse_engineer")
                        elif name == "dream_product_market_plan":
                            res = client.generate(args["description"], "market_plan")
                        elif name == "dream_product_critique":
                            res = client.generate(args["content"], "critique")
                        elif name == "dream_product_handoff":
                            prompt = "Convert this PRD into a technical engineering handoff. List specific Tasks, Components, and Acceptance Criteria suitable for an Agent Swarm."
                            res = client.generate(args["prd_content"], "reverse_engineer") # Reuse generation logic with custom prompt injection? 
                            # Actually, let's just use a specific prompt.
                            messages = [
                                {"role": "system", "content": PM_SYSTEM_PROMPT},
                                {"role": "user", "content": f"{prompt}\n\nPRD:\n{args['prd_content']}"}
                            ]
                            resp = client.client.chat.completions.create(model=client.model, messages=messages)
                            res = resp.choices[0].message.content

                        else:
                            raise ValueError(f"Unknown tool: {name}")
                            
                        response["result"] = {"content": [{"type": "text", "text": res}]}
                    except Exception as e:
                        response["error"] = {"code": -32603, "message": str(e)}

            else:
                continue
                
            print(json.dumps(response), flush=True)
        except Exception:
            break

if __name__ == "__main__":
    run_server()
