#!/usr/bin/env python3
import sys
import argparse
import asyncio
from pathlib import Path

# Add project root to path
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from src.core.orchestration.cascade import DreamCascadeOrchestrator, OrchestratorConfig

async def main():
    parser = argparse.ArgumentParser(description="MCP Orchestration Skill - Cascade Launcher")
    parser.add_argument("task", help="The research task")
    parser.add_argument("--belters", "-b", type=int, default=5, help="Number of Belters")
    args = parser.parse_args()
    
    config = OrchestratorConfig(num_agents=args.belters)
    orchestrator = DreamCascadeOrchestrator(provider_name="anthropic", config=config)
    
    print(f"🌊 Launching Cascade: {args.belters} agents")
    print(f"Task: {args.task}")
    
    result = await orchestrator.execute_task(args.task)
    print("\nResult summary:")
    if result.get('camina_response'):
        print(result['camina_response'].content)
    elif result['drummer_responses']:
        print(result['drummer_responses'][0].content)

if __name__ == "__main__":
    asyncio.run(main())
