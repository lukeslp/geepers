#!/usr/bin/env python3
import sys
import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('data_fetch_mcp')

# Add lib to path
current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, "lib")
sys.path.insert(0, lib_path)

try:
    from data_fetching import (
        CensusClient, ArxivClient, SemanticScholarClient, ArchiveClient,
        WeatherClient, NewsClient, GitHubClient, NASAClient, FinanceClient,
        OpenLibraryClient
    )
    # Import Factory if available or just use clients directly
    from data_fetching.factory import DataFetchingFactory
except ImportError as e:
    logger.error(f"Failed to import data_fetching library: {e}")
    sys.exit(1)

class DataFetchMCPServer:
    def __init__(self):
        self.running = False
        # Initialize clients lazily
        self._clients = {}

    def get_client(self, name: str):
        if name not in self._clients:
            try:
                self._clients[name] = DataFetchingFactory.create_client(name)
            except Exception as e:
                logger.error(f"Error creating client {name}: {e}")
                return None
        return self._clients[name]

    async def run(self):
        logger.info("Starting Data Fetch MCP Server (Stdio)...")
        self.running = True
        while self.running:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                
                response = await self.handle_message(message)
                if response:
                    print(json.dumps(response), flush=True)

            except Exception as e:
                logger.exception(f"Error in main loop: {e}")

    async def handle_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        msg_id = message.get('id')
        method = message.get('method')
        params = message.get('params', {})

        if not msg_id: return None # Notification?

        try:
            if method == 'initialize':
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "data-fetch-skill", "version": "1.0.0"}
                    }
                }
            elif method == 'tools/list':
                return {
                    "jsonrpc": "2.0", "id": msg_id,
                    "result": {"tools": self.get_tool_definitions()}
                }
            elif method == 'tools/call':
                result = await self.call_tool(params.get('name'), params.get('arguments', {}))
                return {
                    "jsonrpc": "2.0", "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
                }
            elif method == 'ping':
                 return {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            else:
                return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}

        except Exception as e:
            logger.exception(f"Error handling {method}")
            return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32603, "message": str(e)}}

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "dream_of_arxiv",
                "description": "Search arXiv for academic papers",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "default": 5},
                        "category": {"type": "string", "description": "arXiv category (e.g. cs.AI)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "dream_of_census_acs",
                "description": "Fetch US Census ACS demographic data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "integer", "description": "Year (e.g. 2022)"},
                        "variables": {"type": "object", "description": "Map of variable codes to names"},
                        "state": {"type": "string", "description": "State FIPS code"},
                        "geography": {"type": "string", "default": "county:*"}
                    },
                    "required": ["year", "variables"]
                }
            },
            {
                "name": "dream_of_weather",
                "description": "Get current weather for a location",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name or location"}
                    },
                    "required": ["location"]
                }
            },
            {
                "name": "dream_of_news",
                "description": "Search for news articles",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "category": {"type": "string"}
                    }
                }
            },
            {
                "name": "dream_of_github_repos",
                "description": "Search GitHub repositories",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "sort": {"type": "string", "enum": ["stars", "forks", "updated"]}
                    },
                    "required": ["query"]
                }
            }
        ]

    async def call_tool(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name == "dream_of_arxiv":
             client = self.get_client("arxiv")
             query = args.get("query")
             if args.get("category"):
                 query = f"cat:{args['category']} AND {query}"
             results = client.search(query, max_results=args.get("max_results", 5))
             return {"papers": [r.to_dict() for r in results]}
        
        elif name == "dream_of_census_acs":
            client = self.get_client("census")
            # Assuming client needs API key which should be in env
            df = client.fetch_acs(
                year=args['year'],
                variables=args['variables'],
                state=args.get('state'),
                geography=args.get('geography', 'county:*')
            )
            return {"records": df.to_dict('records')}

        elif name == "dream_of_weather":
            client = self.get_client("weather")
            return client.get_current_weather(args['location'])

        elif name == "dream_of_news":
            client = self.get_client("news")
            if args.get("query"):
                return client.search_everything(args['query'])
            return client.get_top_headlines(category=args.get("category"))

        elif name == "dream_of_github_repos":
            client = self.get_client("github")
            return client.search_repositories(args['query'], sort=args.get("sort", "stars"))

        else:
            raise ValueError(f"Unknown tool: {name}")

if __name__ == "__main__":
    server = DataFetchMCPServer()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        pass
