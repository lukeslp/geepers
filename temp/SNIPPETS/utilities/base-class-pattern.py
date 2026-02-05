"""
Base Class Pattern for Plugin/Tool Architecture

Description: Extensible base class pattern for building plugin systems, tool libraries,
or modular components. Uses Pydantic for validation, abstract methods for enforcement,
and event emitters for progress tracking.

Use Cases:
- API tool libraries (search, generation, analysis tools)
- Plugin architectures for extensible applications
- Microservice component frameworks
- Multi-provider integrations (LLMs, search engines, etc.)

Dependencies:
- pydantic (pip install pydantic)
- typing (standard library)

Notes:
- UserValves pattern for credential management
- Event emitter pattern for async progress updates
- Abstract execute() method enforces implementation
- Built-in logging and error handling
- Credential validation on initialization

Related Snippets:
- See multi-provider-llm-client.js for JavaScript equivalent
- See service-manager-pattern.py for process management base
"""

from typing import Dict, Any, Optional, Callable, Awaitable, List
from pydantic import BaseModel, Field
import logging
from abc import ABC, abstractmethod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """
    Base class for all tools in a plugin/tool system.

    Subclasses must:
    1. Define UserValves with required credentials
    2. Implement execute() method
    3. Call emit_event() for progress updates
    """

    class UserValves(BaseModel):
        """
        Base class for tool credentials and configuration.

        Override this in subclasses to define required credentials:

        class UserValves(BaseModel):
            api_key: str = Field(..., description="API key for service")
            base_url: str = Field(default="https://api.example.com")
        """
        pass

    def __init__(self, credentials: Dict[str, str] = None):
        """
        Initialize the tool.

        Args:
            credentials: Dictionary of credentials matching UserValves fields

        Raises:
            ValueError: If required credentials are missing
        """
        self.credentials = credentials or {}
        self.validate_credentials()
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_credentials(self) -> None:
        """
        Validate that all required credentials are present.

        Raises:
            ValueError: If required credentials are missing
        """
        required_creds = self.UserValves.__annotations__.keys()
        missing = [cred for cred in required_creds if cred not in self.credentials]

        if missing:
            raise ValueError(
                f"{self.__class__.__name__} missing required credentials: {', '.join(missing)}"
            )

    @abstractmethod
    async def execute(
        self,
        **kwargs: Any,
        __user__: dict = {},
        __event_emitter__: Optional[Callable[[Any], Awaitable[None]]] = None
    ) -> Any:
        """
        Execute the tool's main functionality.

        Args:
            **kwargs: Tool-specific arguments
            __user__: User context dictionary (auth, preferences, etc.)
            __event_emitter__: Optional event emitter for progress updates

        Returns:
            Tool-specific result (dict, str, list, etc.)

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError(f"{self.__class__.__name__} must implement execute()")

    async def emit_event(
        self,
        event_type: str,
        description: str,
        done: bool = False,
        data: Dict[str, Any] = None,
        emitter: Optional[Callable[[Any], Awaitable[None]]] = None
    ) -> None:
        """
        Emit a status event if an emitter is available.

        Args:
            event_type: Type of event ("status", "error", "result", etc.)
            description: Human-readable description
            done: Whether this is the final event
            data: Additional event data
            emitter: Optional event emitter function
        """
        if emitter:
            event_payload = {
                "type": event_type,
                "data": {
                    "description": description,
                    "done": done,
                    **(data or {})
                }
            }
            try:
                await emitter(event_payload)
            except Exception as e:
                self.logger.error(f"Event emission failed: {e}")

    def get_credentials(self, key: str, default: Any = None) -> Any:
        """
        Safely get a credential value.

        Args:
            key: Credential key
            default: Default value if not found

        Returns:
            Credential value or default
        """
        return self.credentials.get(key, default)


# Example implementation
class WebSearchTool(BaseTool):
    """Example tool implementation for web search"""

    class UserValves(BaseModel):
        """Required credentials for web search"""
        search_api_key: str = Field(..., description="API key for search service")
        max_results: int = Field(default=10, description="Maximum results to return")

    async def execute(
        self,
        query: str,
        **kwargs,
        __user__: dict = {},
        __event_emitter__: Optional[Callable[[Any], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """
        Execute web search.

        Args:
            query: Search query string
            **kwargs: Additional search parameters
            __user__: User context
            __event_emitter__: Progress emitter

        Returns:
            Dictionary with search results
        """
        await self.emit_event(
            "status",
            f"Searching for: {query}",
            emitter=__event_emitter__
        )

        try:
            # Get configuration
            api_key = self.get_credentials("search_api_key")
            max_results = self.get_credentials("max_results", 10)

            # Perform search (example - replace with actual API call)
            results = await self._perform_search(query, api_key, max_results)

            await self.emit_event(
                "status",
                f"Found {len(results)} results",
                done=True,
                data={"count": len(results)},
                emitter=__event_emitter__
            )

            return {
                "query": query,
                "results": results,
                "count": len(results)
            }

        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            await self.emit_event(
                "error",
                f"Search failed: {str(e)}",
                done=True,
                emitter=__event_emitter__
            )
            raise

    async def _perform_search(
        self,
        query: str,
        api_key: str,
        max_results: int
    ) -> List[Dict]:
        """
        Perform the actual search.

        This is a placeholder - implement with actual API.
        """
        # Example implementation
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.search.example.com/search",
                params={"q": query, "limit": max_results},
                headers={"Authorization": f"Bearer {api_key}"}
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("results", [])


# Example usage
async def main():
    """Example usage of the tool pattern"""

    # Initialize tool with credentials
    search_tool = WebSearchTool(credentials={
        "search_api_key": "your-api-key-here",
        "max_results": 5
    })

    # Define event handler
    async def event_handler(event):
        print(f"[{event['type']}] {event['data']['description']}")

    # Execute tool
    results = await search_tool.execute(
        query="Python best practices",
        __event_emitter__=event_handler
    )

    print(f"Results: {results}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


"""
Creating Your Own Tool:

1. Subclass BaseTool
2. Define UserValves with required credentials
3. Implement execute() method
4. Use emit_event() for progress updates
5. Handle errors gracefully

Example:

class MyCustomTool(BaseTool):
    class UserValves(BaseModel):
        api_key: str
        timeout: int = 30

    async def execute(self, input_data: str, **kwargs):
        await self.emit_event("status", "Processing...", emitter=kwargs.get('__event_emitter__'))

        # Your logic here
        result = process_data(input_data)

        await self.emit_event("status", "Complete!", done=True, emitter=kwargs.get('__event_emitter__'))
        return result
"""
