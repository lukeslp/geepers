"""
Task Cancellation and Timeout Patterns

Description: Comprehensive patterns for handling async task cancellation, timeouts,
graceful shutdown, and cleanup. Includes patterns for cancelling individual tasks,
task groups, and implementing proper cancellation handling.

Use Cases:
- Implementing request timeouts in web applications
- Graceful shutdown of long-running services
- Cancelling stale or slow operations
- Cleanup of resources when tasks are cancelled
- Implementing circuit breakers and fallbacks
- Coordinating shutdown across multiple async tasks

Dependencies:
- asyncio (built-in)
- typing (built-in)
- logging (built-in)

Notes:
- Always handle asyncio.CancelledError appropriately
- Use try/finally for cleanup even when cancelled
- Set reasonable timeout values
- Consider using asyncio.wait_for() for individual task timeouts
- Use asyncio.shield() to protect critical operations
- Implement proper cleanup in finally blocks

Related Snippets:
- /home/coolhand/SNIPPETS/async-patterns/async_llm_operations.py
- /home/coolhand/SNIPPETS/async-patterns/async_context_managers.py
- /home/coolhand/SNIPPETS/async-patterns/parallel_task_execution.py

Source Attribution:
- Extracted from: /home/coolhand/enterprise_orchestration/core/base.py
- Related: /home/coolhand/enterprise_orchestration/core/coordinator.py
- Related: /home/coolhand/projects/swarm/core/
"""

import asyncio
import logging
import signal
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# BASIC TIMEOUT PATTERNS
# ============================================================================

async def with_timeout(coro, timeout: float, default=None):
    """
    Execute coroutine with timeout, returning default on timeout.

    Args:
        coro: Coroutine to execute
        timeout: Timeout in seconds
        default: Value to return on timeout (None by default)

    Returns:
        Result of coroutine or default value on timeout
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        logger.warning(f"Operation timed out after {timeout}s")
        return default


async def with_timeout_and_fallback(
    coro,
    timeout: float,
    fallback_coro,
    error_msg: Optional[str] = None
):
    """
    Execute coroutine with timeout, falling back to alternative on timeout.

    Args:
        coro: Primary coroutine to execute
        timeout: Timeout in seconds
        fallback_coro: Fallback coroutine to execute on timeout
        error_msg: Optional error message to log

    Returns:
        Result of primary or fallback coroutine
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        if error_msg:
            logger.warning(error_msg)
        else:
            logger.warning(f"Primary operation timed out, executing fallback")
        return await fallback_coro


# ============================================================================
# CANCELLABLE TASK WRAPPER
# ============================================================================

@dataclass
class TaskInfo:
    """Information about a managed task."""
    task_id: str
    task: asyncio.Task
    created_at: datetime
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = None

    @property
    def is_done(self) -> bool:
        """Check if task is complete."""
        return self.task.done()

    @property
    def is_cancelled(self) -> bool:
        """Check if task was cancelled."""
        return self.task.cancelled()

    @property
    def age(self) -> float:
        """Get task age in seconds."""
        return (datetime.now() - self.created_at).total_seconds()


class CancellableTaskManager:
    """
    Manager for tracking and cancelling async tasks.

    Provides centralized control over task lifecycle with timeout enforcement.
    """

    def __init__(self):
        """Initialize task manager."""
        self.tasks: Dict[str, TaskInfo] = {}
        self.cleanup_interval = 60  # Cleanup stale tasks every 60s
        self._cleanup_task: Optional[asyncio.Task] = None

    async def start(self):
        """Start the task manager."""
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        logger.info("Task manager started")

    async def stop(self):
        """Stop the task manager and cancel all tasks."""
        logger.info("Stopping task manager...")

        # Cancel cleanup task
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        # Cancel all managed tasks
        await self.cancel_all()

        logger.info("Task manager stopped")

    def create_task(
        self,
        coro,
        task_id: Optional[str] = None,
        timeout: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TaskInfo:
        """
        Create and track a new task.

        Args:
            coro: Coroutine to execute
            task_id: Optional task identifier (auto-generated if not provided)
            timeout: Optional timeout in seconds
            metadata: Optional metadata dictionary

        Returns:
            TaskInfo for the created task
        """
        if task_id is None:
            task_id = f"task_{len(self.tasks) + 1}_{int(time.time() * 1000)}"

        # Wrap coroutine with timeout if specified
        if timeout:
            coro = asyncio.wait_for(coro, timeout=timeout)

        task = asyncio.create_task(coro)
        task_info = TaskInfo(
            task_id=task_id,
            task=task,
            created_at=datetime.now(),
            timeout=timeout,
            metadata=metadata or {}
        )

        self.tasks[task_id] = task_info
        logger.debug(f"Created task {task_id} with timeout={timeout}")

        return task_info

    async def cancel_task(self, task_id: str, wait: bool = True) -> bool:
        """
        Cancel a specific task.

        Args:
            task_id: Task identifier
            wait: Whether to wait for cancellation to complete

        Returns:
            True if task was cancelled, False if not found
        """
        task_info = self.tasks.get(task_id)
        if not task_info:
            logger.warning(f"Task {task_id} not found")
            return False

        if task_info.is_done:
            logger.debug(f"Task {task_id} already completed")
            return False

        logger.info(f"Cancelling task {task_id}")
        task_info.task.cancel()

        if wait:
            try:
                await task_info.task
            except asyncio.CancelledError:
                pass

        self.tasks.pop(task_id, None)
        return True

    async def cancel_all(self, wait: bool = True):
        """
        Cancel all tracked tasks.

        Args:
            wait: Whether to wait for all cancellations
        """
        logger.info(f"Cancelling {len(self.tasks)} tasks")

        # Cancel all tasks
        for task_info in self.tasks.values():
            if not task_info.is_done:
                task_info.task.cancel()

        if wait:
            # Wait for all cancellations
            await asyncio.gather(
                *[t.task for t in self.tasks.values()],
                return_exceptions=True
            )

        self.tasks.clear()

    async def cancel_by_age(self, max_age_seconds: float):
        """
        Cancel tasks older than specified age.

        Args:
            max_age_seconds: Maximum task age in seconds
        """
        to_cancel = [
            task_id for task_id, task_info in self.tasks.items()
            if task_info.age > max_age_seconds and not task_info.is_done
        ]

        for task_id in to_cancel:
            await self.cancel_task(task_id)

        if to_cancel:
            logger.info(f"Cancelled {len(to_cancel)} stale tasks")

    async def _cleanup_loop(self):
        """Periodic cleanup of completed tasks."""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)

                # Remove completed tasks
                completed = [
                    task_id for task_id, task_info in self.tasks.items()
                    if task_info.is_done
                ]

                for task_id in completed:
                    self.tasks.pop(task_id, None)

                if completed:
                    logger.debug(f"Cleaned up {len(completed)} completed tasks")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")

    def get_stats(self) -> Dict[str, int]:
        """Get task statistics."""
        return {
            'total': len(self.tasks),
            'running': sum(1 for t in self.tasks.values() if not t.is_done),
            'completed': sum(1 for t in self.tasks.values() if t.is_done and not t.is_cancelled),
            'cancelled': sum(1 for t in self.tasks.values() if t.is_cancelled)
        }


# ============================================================================
# GRACEFUL SHUTDOWN PATTERN
# ============================================================================

class ShutdownManager:
    """
    Manages graceful shutdown of async services.

    Handles signal handling and coordinated shutdown sequence.
    """

    def __init__(self, shutdown_timeout: float = 30.0):
        """
        Initialize shutdown manager.

        Args:
            shutdown_timeout: Maximum time to wait for shutdown
        """
        self.shutdown_timeout = shutdown_timeout
        self.shutdown_event = asyncio.Event()
        self.active_operations: Set[asyncio.Task] = set()
        self.cleanup_callbacks: List[Callable] = []

    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        loop = asyncio.get_running_loop()

        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(self.shutdown(s))
            )

        logger.info("Signal handlers configured")

    def add_cleanup_callback(self, callback: Callable):
        """
        Add callback to be called during shutdown.

        Args:
            callback: Async function to call on shutdown
        """
        self.cleanup_callbacks.append(callback)

    def track_operation(self, task: asyncio.Task):
        """
        Track an operation that should complete before shutdown.

        Args:
            task: Task to track
        """
        self.active_operations.add(task)
        task.add_done_callback(self.active_operations.discard)

    async def shutdown(self, sig=None):
        """
        Execute graceful shutdown sequence.

        Args:
            sig: Signal that triggered shutdown (optional)
        """
        if self.shutdown_event.is_set():
            logger.warning("Shutdown already in progress")
            return

        logger.info(f"Starting graceful shutdown (signal: {sig})")
        self.shutdown_event.set()

        try:
            # Wait for active operations with timeout
            if self.active_operations:
                logger.info(f"Waiting for {len(self.active_operations)} operations to complete")

                await asyncio.wait_for(
                    asyncio.gather(*self.active_operations, return_exceptions=True),
                    timeout=self.shutdown_timeout
                )

                logger.info("All operations completed")

        except asyncio.TimeoutError:
            logger.warning(f"Shutdown timeout reached, forcefully cancelling {len(self.active_operations)} operations")

            for task in self.active_operations:
                task.cancel()

            await asyncio.gather(*self.active_operations, return_exceptions=True)

        # Execute cleanup callbacks
        if self.cleanup_callbacks:
            logger.info(f"Executing {len(self.cleanup_callbacks)} cleanup callbacks")

            for callback in self.cleanup_callbacks:
                try:
                    await callback()
                except Exception as e:
                    logger.error(f"Error in cleanup callback: {e}")

        logger.info("Graceful shutdown complete")

    async def wait_for_shutdown(self):
        """Wait for shutdown signal."""
        await self.shutdown_event.wait()

    @property
    def is_shutting_down(self) -> bool:
        """Check if shutdown is in progress."""
        return self.shutdown_event.is_set()


# ============================================================================
# SHIELDED OPERATIONS
# ============================================================================

async def critical_operation_with_shield(operation, cleanup):
    """
    Execute critical operation that should not be cancelled.

    Uses asyncio.shield() to protect from cancellation, with guaranteed cleanup.

    Args:
        operation: Async operation to protect
        cleanup: Async cleanup function

    Returns:
        Result of operation
    """
    try:
        # Shield the operation from cancellation
        result = await asyncio.shield(operation())
        return result

    except asyncio.CancelledError:
        logger.warning("Cancellation attempted on shielded operation")
        raise

    finally:
        # Cleanup always runs, even if cancelled
        try:
            await cleanup()
        except Exception as e:
            logger.error(f"Error in cleanup: {e}")


# ============================================================================
# TIMEOUT CONTEXT MANAGER
# ============================================================================

@asynccontextmanager
async def timeout_context(seconds: float, error_msg: Optional[str] = None):
    """
    Context manager for timeout enforcement.

    Args:
        seconds: Timeout in seconds
        error_msg: Optional error message

    Raises:
        asyncio.TimeoutError: If operations exceed timeout
    """
    async def timeout_watchdog():
        await asyncio.sleep(seconds)
        raise asyncio.TimeoutError(error_msg or f"Operation timed out after {seconds}s")

    task = asyncio.create_task(timeout_watchdog())

    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def example_basic_timeout():
    """Example: Basic timeout patterns."""
    print("=== Basic Timeout Patterns ===\n")

    async def slow_operation():
        await asyncio.sleep(5)
        return "completed"

    async def fast_fallback():
        return "fallback result"

    # Timeout with default value
    result = await with_timeout(slow_operation(), timeout=1.0, default="timed out")
    print(f"Result with default: {result}")

    # Timeout with fallback
    result = await with_timeout_and_fallback(
        slow_operation(),
        timeout=1.0,
        fallback_coro=fast_fallback()
    )
    print(f"Result with fallback: {result}\n")


async def example_task_manager():
    """Example: Cancellable task manager."""
    print("=== Cancellable Task Manager ===\n")

    manager = CancellableTaskManager()
    await manager.start()

    async def long_running_task(n: int):
        try:
            for i in range(10):
                await asyncio.sleep(0.5)
                print(f"  Task {n} progress: {i+1}/10")
            return f"Task {n} completed"
        except asyncio.CancelledError:
            print(f"  Task {n} was cancelled")
            raise

    # Create tasks
    task1 = manager.create_task(long_running_task(1), timeout=3.0)
    task2 = manager.create_task(long_running_task(2), timeout=10.0)

    # Let them run briefly
    await asyncio.sleep(1.5)

    # Cancel task 2
    await manager.cancel_task(task2.task_id)

    # Wait for task 1 to complete or timeout
    try:
        result = await task1.task
        print(f"Task 1 result: {result}")
    except asyncio.TimeoutError:
        print("Task 1 timed out")

    print(f"Stats: {manager.get_stats()}")

    await manager.stop()
    print()


async def example_graceful_shutdown():
    """Example: Graceful shutdown with cleanup."""
    print("=== Graceful Shutdown Pattern ===\n")

    shutdown_mgr = ShutdownManager(shutdown_timeout=5.0)

    async def service_cleanup():
        print("  Cleaning up service resources...")
        await asyncio.sleep(0.5)
        print("  Cleanup complete")

    shutdown_mgr.add_cleanup_callback(service_cleanup)

    async def background_task():
        try:
            for i in range(20):
                if shutdown_mgr.is_shutting_down:
                    print("  Background task detected shutdown, exiting gracefully")
                    break
                await asyncio.sleep(0.3)
                print(f"  Background task iteration {i+1}")
        except asyncio.CancelledError:
            print("  Background task cancelled")
            raise

    # Start background task
    task = asyncio.create_task(background_task())
    shutdown_mgr.track_operation(task)

    # Let it run briefly
    await asyncio.sleep(2)

    # Trigger shutdown
    await shutdown_mgr.shutdown()
    print()


async def example_timeout_context():
    """Example: Timeout context manager."""
    print("=== Timeout Context Manager ===\n")

    try:
        async with timeout_context(2.0, "Operation took too long"):
            print("Starting operation...")
            await asyncio.sleep(1.0)
            print("Operation completed within timeout")
    except asyncio.TimeoutError as e:
        print(f"Caught timeout: {e}")

    print()


async def main():
    """Run all examples."""
    await example_basic_timeout()
    await example_task_manager()
    await example_graceful_shutdown()
    await example_timeout_context()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s'
    )
    asyncio.run(main())
