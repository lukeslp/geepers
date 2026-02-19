#!/usr/bin/env python3
import sys
import os
import argparse
import asyncio
import uuid
from pathlib import Path

# Add src to path so we can import modules
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from src.core.orchestration.cascade import DreamCascadeOrchestrator, OrchestratorConfig
from src.core.reporting.manager import DocumentGenerationManager

async def run_orchestration(args):
    # 1. Setup Config
    config = OrchestratorConfig(
        num_agents=args.belters,
        enable_drummer=args.drummers > 0,
        enable_camina=args.caminas > 0,
        max_concurrent_agents=args.concurrent
    )
    
    # 2. Initialize Orchestrator
    # We use the provider specify in args
    orchestrator = DreamCascadeOrchestrator(
        provider_name=args.provider,
        model=args.model,
        config=config
    )
    
    print(f"🚀 Starting orchestration: {args.pattern.upper()}")
    print(f"Topic: {args.task}")
    print(f"Setup: {args.belters} Belters, {args.drummers} Drummers, {args.caminas} Caminas")
    
    # 3. Execute
    async def progress_callback(event_type: str, data: any):
        if event_type == 'status':
            print(f"  [STATUS] {data}")
            
    result = await orchestrator.execute_task(args.task, stream_callback=progress_callback)
    
    # 4. Generate Reports
    manager = DocumentGenerationManager(output_dir="reports")
    
    # Prep content sections
    content_sections = []
    
    # Add Belter findings
    for r in result['belter_responses']:
        if r.status == "completed":
            content_sections.append({
                "title": f"Belter {r.agent_id} Analysis",
                "content": r.content,
                "type": "analysis"
            })
            
    # Add Drummer syntheses
    for r in result['drummer_responses']:
        if r.status == "completed":
            content_sections.append({
                "title": f"Drummer {r.agent_id} Synthesis",
                "content": r.content,
                "type": "synthesis"
            })
            
    # Add Camina executive synthesis
    if result.get('camina_response') and result['camina_response'].status == "completed":
        content_sections.append({
            "title": "Executive Summary",
            "content": result['camina_response'].content,
            "type": "executive"
        })
        
    doc_id = str(uuid.uuid4())[:8]
    report_result = manager.generate_reports(
        content_sections=content_sections,
        title=f"Research Report: {args.task}",
        document_id=doc_id,
        formats=["markdown", "pdf"] if args.pdf else ["markdown"]
    )
    
    print("\n✅ Orchestration Complete!")
    print(f"Time: {result['execution_time']:.1f}s")
    print(f"Reports generated in: {manager.output_dir}")
    for file in report_result.get('generated_files', []):
        print(f" - {file['filename']}")

def main():
    parser = argparse.ArgumentParser(description="MCP Orchestration Skill - Main Launcher")
    parser.add_argument("task", help="The research task or question")
    parser.add_argument("--pattern", choices=["cascade", "swarm"], default="cascade", help="Orchestration pattern")
    parser.add_argument("--belters", "-b", type=int, default=5, help="Number of Belter agents")
    parser.add_argument("--drummers", "-d", type=int, default=1, help="Number of Drummer agents")
    parser.add_argument("--caminas", "-c", type=int, default=0, help="Number of Camina agents")
    parser.add_argument("--provider", "-p", default="anthropic", help="LLM Provider")
    parser.add_argument("--model", "-m", help="Specific model to use")
    parser.add_argument("--concurrent", type=int, default=5, help="Max concurrent agents")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF report also")
    
    args = parser.parse_args()
    
    asyncio.run(run_orchestration(args))

if __name__ == "__main__":
    main()
