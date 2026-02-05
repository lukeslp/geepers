"""
Async Context Managers Pattern

Description: Comprehensive patterns for implementing async context managers
(__aenter__/__aexit__) for resource management in async code. Includes patterns
for API clients, database connections, file operations, and lifecycle management.

Use Cases:
- Managing async API client connections and cleanup
- Database connection pooling with async context
- Async file operations with proper resource cleanup
- Module lifecycle management (setup/teardown)
- Distributed lock acquisition and release
- Streaming resource management

Dependencies:
- asyncio (built-in)
- typing (built-in)
- abc (built-in)

Notes:
- Always implement both __aenter__ and __aexit__
- Handle exceptions in __aexit__ properly
- Clean up resources even if exceptions occur
- Use async with statement for automatic cleanup
- Consider using contextlib.asynccontextmanager decorator
- Propagate exceptions unless explicitly handling them

Related Snippets:
- /home/coolhand/SNIPPETS/async-patterns/async_llm_operations.py
- /home/coolhand/SNIPPETS/error-handling/graceful_import_fallbacks.py

Source Attribution:
- Extracted from: /home/coolhand/enterprise_orchestration/core/base.py
- Related: /home/coolhand/projects/swarm/core/
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Optional, TypeVar, Generic
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

T = TypeVar('T')


# ============================================================================
# BASIC ASYNC CONTEXT MANAGER PATTERN
# ============================================================================

class AsyncResourceManager:
    """
    Basic async context manager for resource lifecycle.

    Demonstrates the fundamental pattern of __aenter__ and __aexit__.
    """

    def __init__(self, resource_name: str):
        """Initialize with resource identifier."""
        self.resource_name = resource_name
        self.resource = None
        self.is_initialized = False

    async def __aenter__(self):
        """
        Async entry: acquire/initialize resource.

        Returns:
            The managed resource or self
        """
        logger.info(f"Acquiring resource: {self.resource_name}")

        # Simulate async resource acquisition
        await asyncio.sleep(0.1)
        self.resource = f"Resource({self.resource_name})"
        self.is_initialized = True

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async exit: cleanup/release resource.

        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised

        Returns:
            False to propagate exceptions, True to suppress
        """
        logger.info(f"Releasing resource: {self.resource_name}")

        try:
            # Cleanup operations
            if self.resource:
                await asyncio.sleep(0.1)  # Simulate async cleanup
                self.resource = None
                self.is_initialized = False

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            # Don't suppress the original exception

        # Return False to propagate any exception that occurred in the context
        return False


# ============================================================================
# API CLIENT WITH ASYNC CONTEXT MANAGER
# ============================================================================

class AsyncAPIClient:
    """
    Async context manager for API client lifecycle.

    Handles connection setup, session management, and proper cleanup.
    """

    def __init__(self, base_url: str, api_key: str, timeout: int = 30):
        """
        Initialize API client.

        Args:
            base_url: Base URL for API
            api_key: API authentication key
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.session = None
        self.is_connected = False

    async def __aenter__(self):
        """Setup API client and establish connection."""
        logger.info(f"Connecting to {self.base_url}")

        try:
            # In real implementation, would use aiohttp.ClientSession
            # Simulating connection setup
            await asyncio.sleep(0.1)

            self.session = {
                'base_url': self.base_url,
                'headers': {'Authorization': f'Bearer {self.api_key}'},
                'timeout': self.timeout
            }
            self.is_connected = True

            logger.info("API client connected successfully")
            return self

        except Exception as e:
            logger.error(f"Failed to connect API client: {e}")
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close API client connection and cleanup."""
        if self.is_connected:
            logger.info("Closing API client connection")

            try:
                # Close session
                if self.session:
                    await asyncio.sleep(0.1)  # Simulate async close
                    self.session = None

                self.is_connected = False
                logger.info("API client closed successfully")

            except Exception as e:
                logger.error(f"Error closing API client: {e}")

        return False

    async def make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API request.

        Args:
            endpoint: API endpoint
            data: Request data

        Returns:
            Response data
        """
        if not self.is_connected:
            raise RuntimeError("API client not connected. Use 'async with' context.")

        # Simulated API call
        await asyncio.sleep(0.1)
        return {
            'status': 'success',
            'endpoint': endpoint,
            'data': data
        }


# ============================================================================
# MODULE LIFECYCLE MANAGER
# ============================================================================

class ModuleStatus(Enum):
    """Module lifecycle status."""
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    STOPPED = "stopped"
    ERROR = "error"


class AsyncModuleBase:
    """
    Base class for modules with async lifecycle management.

    Provides standardized setup/teardown via context manager pattern.
    """

    def __init__(self, module_id: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize module.

        Args:
            module_id: Unique module identifier
            config: Optional configuration dictionary
        """
        self.module_id = module_id
        self.config = config or {}
        self.status = ModuleStatus.UNINITIALIZED
        self.start_time: Optional[datetime] = None
        self.active_tasks: Dict[str, asyncio.Task] = {}

        logger.info(f"Module {module_id} created")

    async def __aenter__(self):
        """Initialize and setup module."""
        logger.info(f"Initializing module {self.module_id}")
        self.status = ModuleStatus.INITIALIZING

        try:
            # Load dependencies
            await self._load_dependencies()

            # Setup module-specific resources
            await self._setup()

            # Validate setup
            if await self._validate_setup():
                self.status = ModuleStatus.READY
                self.start_time = datetime.now()
                logger.info(f"Module {self.module_id} ready")
            else:
                self.status = ModuleStatus.ERROR
                raise RuntimeError(f"Module {self.module_id} setup validation failed")

            return self

        except Exception as e:
            self.status = ModuleStatus.ERROR
            logger.error(f"Module {self.module_id} initialization failed: {e}")
            raise

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Shutdown and cleanup module."""
        logger.info(f"Shutting down module {self.module_id}")
        self.status = ModuleStatus.SHUTTING_DOWN

        try:
            # Cancel active tasks
            if self.active_tasks:
                logger.info(f"Cancelling {len(self.active_tasks)} active tasks")
                for task in self.active_tasks.values():
                    task.cancel()

                # Wait for cancellation
                await asyncio.gather(*self.active_tasks.values(), return_exceptions=True)
                self.active_tasks.clear()

            # Cleanup module-specific resources
            await self._cleanup()

            self.status = ModuleStatus.STOPPED
            logger.info(f"Module {self.module_id} stopped successfully")

        except Exception as e:
            logger.error(f"Error during module shutdown: {e}")
            self.status = ModuleStatus.ERROR

        return False

    async def _load_dependencies(self):
        """Load module dependencies. Override in subclasses."""
        await asyncio.sleep(0.05)  # Simulate dependency loading

    async def _setup(self):
        """Setup module resources. Override in subclasses."""
        await asyncio.sleep(0.05)  # Simulate setup

    async def _validate_setup(self) -> bool:
        """Validate setup. Override in subclasses."""
        return True

    async def _cleanup(self):
        """Cleanup module resources. Override in subclasses."""
        await asyncio.sleep(0.05)  # Simulate cleanup


# ============================================================================
# ASYNC LOCK WITH TIMEOUT
# ============================================================================

class AsyncLockWithTimeout:
    """
    Async context manager for acquiring locks with timeout.

    Useful for distributed systems and resource coordination.
    """

    def __init__(self, lock_name: str, timeout: float = 30.0):
        """
        Initialize lock manager.

        Args:
            lock_name: Lock identifier
            timeout: Maximum seconds to wait for lock
        """
        self.lock_name = lock_name
        self.timeout = timeout
        self.lock = asyncio.Lock()
        self.acquired = False

    async def __aenter__(self):
        """Acquire lock with timeout."""
        logger.debug(f"Attempting to acquire lock: {self.lock_name}")

        try:
            # Try to acquire with timeout
            await asyncio.wait_for(
                self.lock.acquire(),
                timeout=self.timeout
            )
            self.acquired = True
            logger.debug(f"Lock acquired: {self.lock_name}")
            return self

        except asyncio.TimeoutError:
            logger.error(f"Failed to acquire lock {self.lock_name} within {self.timeout}s")
            raise TimeoutError(f"Could not acquire lock '{self.lock_name}'")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Release lock."""
        if self.acquired:
            self.lock.release()
            self.acquired = False
            logger.debug(f"Lock released: {self.lock_name}")

        return False


# ============================================================================
# ASYNC CONTEXT MANAGER DECORATOR
# ============================================================================

@asynccontextmanager
async def managed_resource(resource_id: str, config: Dict[str, Any]) -> AsyncIterator[Any]:
    """
    Async context manager using decorator pattern.

    Simpler alternative to class-based context managers for simple cases.

    Args:
        resource_id: Resource identifier
        config: Resource configuration

    Yields:
        Initialized resource
    """
    logger.info(f"Setting up resource: {resource_id}")
    resource = None

    try:
        # Setup
        await asyncio.sleep(0.1)
        resource = {
            'id': resource_id,
            'config': config,
            'created_at': datetime.now()
        }

        # Yield resource for use in 'async with' block
        yield resource

    finally:
        # Cleanup (always runs)
        logger.info(f"Cleaning up resource: {resource_id}")
        if resource:
            await asyncio.sleep(0.1)
            resource = None


@asynccontextmanager
async def temporary_config_override(config: Dict[str, Any], overrides: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
    """
    Temporarily override configuration within context.

    Args:
        config: Original configuration dict
        overrides: Temporary overrides

    Yields:
        Merged configuration
    """
    # Save original values
    original_values = {k: config.get(k) for k in overrides.keys()}

    try:
        # Apply overrides
        config.update(overrides)
        logger.debug(f"Applied config overrides: {overrides.keys()}")

        yield config

    finally:
        # Restore original values
        for k, v in original_values.items():
            if v is None:
                config.pop(k, None)
            else:
                config[k] = v

        logger.debug("Restored original configuration")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def example_basic_context_manager():
    """Example: Basic async context manager."""
    print("=== Basic Async Context Manager ===\n")

    async with AsyncResourceManager("database") as resource_mgr:
        print(f"Resource active: {resource_mgr.is_initialized}")
        print(f"Resource: {resource_mgr.resource}")

    print("Context exited, resource cleaned up\n")


async def example_api_client():
    """Example: API client with context manager."""
    print("=== API Client Context Manager ===\n")

    async with AsyncAPIClient("https://api.example.com", "secret-key") as client:
        print(f"Client connected: {client.is_connected}")

        # Make requests
        result = await client.make_request("/data", {"query": "test"})
        print(f"Request result: {result}")

    print("API client closed\n")


async def example_module_lifecycle():
    """Example: Module lifecycle management."""
    print("=== Module Lifecycle Management ===\n")

    class MyModule(AsyncModuleBase):
        """Custom module implementation."""

        async def _setup(self):
            """Custom setup logic."""
            await super()._setup()
            print("  Setting up custom module...")

        async def _cleanup(self):
            """Custom cleanup logic."""
            await super()._cleanup()
            print("  Cleaning up custom module...")

    async with MyModule("my-module", {"setting": "value"}) as module:
        print(f"Module status: {module.status.value}")
        print(f"Module started at: {module.start_time}")

    print(f"Final status: {module.status.value}\n")


async def example_lock_with_timeout():
    """Example: Lock acquisition with timeout."""
    print("=== Lock with Timeout ===\n")

    lock_mgr = AsyncLockWithTimeout("shared-resource", timeout=5.0)

    async with lock_mgr:
        print("Lock acquired, performing work...")
        await asyncio.sleep(0.5)

    print("Lock released\n")


async def example_decorator_pattern():
    """Example: Using decorator-based context managers."""
    print("=== Decorator-Based Context Managers ===\n")

    # Managed resource
    async with managed_resource("cache", {"ttl": 300}) as resource:
        print(f"Resource ID: {resource['id']}")
        print(f"Created at: {resource['created_at']}")

    print()

    # Config override
    config = {"debug": False, "timeout": 30}
    print(f"Original config: {config}")

    async with temporary_config_override(config, {"debug": True, "timeout": 60}):
        print(f"Overridden config: {config}")

    print(f"Restored config: {config}\n")


async def main():
    """Run all examples."""
    await example_basic_context_manager()
    await example_api_client()
    await example_module_lifecycle()
    await example_lock_with_timeout()
    await example_decorator_pattern()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main())
