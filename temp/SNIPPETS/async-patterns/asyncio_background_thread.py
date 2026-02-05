"""
Background Asyncio Event Loop in Threading

Description: Pattern for running asyncio coroutines in background threads alongside Flask/synchronous applications.
This is essential for integrating async WebSocket clients, API connections, or other asyncio-based libraries
with synchronous web frameworks.

Use Cases:
- Running WebSocket clients (like Bluesky firehose) alongside Flask applications
- Background async tasks in synchronous web servers
- Integrating async libraries with sync frameworks
- Real-time data streaming from async sources

Dependencies:
- asyncio (standard library)
- threading (standard library)

Notes:
- Creates a new event loop in the background thread (required for thread safety)
- Daemon thread ensures it terminates when main program exits
- Useful for Flask-SocketIO applications that need async data sources
- Can use threading.Event() for graceful shutdown coordination

Related Snippets:
- websocket-patterns/websocket_client_with_reconnect.py
- web-frameworks/flask_socketio_setup.py
"""

import asyncio
import threading
import logging

logger = logging.getLogger(__name__)


class BackgroundAsyncRunner:
    """
    Manages an asyncio event loop running in a background thread.

    Example Usage:
        runner = BackgroundAsyncRunner()

        async def my_async_task():
            while runner.is_running():
                # Your async work here
                await asyncio.sleep(1)

        runner.start(my_async_task)
        # ... do sync work in main thread ...
        runner.stop()
    """

    def __init__(self):
        self.running = False
        self.thread = None
        self._loop = None

    def is_running(self):
        """Check if the background loop is running"""
        return self.running

    def start(self, coroutine_func, *args, **kwargs):
        """
        Start the background asyncio loop with a coroutine.

        Args:
            coroutine_func: Async function to run
            *args, **kwargs: Arguments to pass to the coroutine
        """
        if self.running:
            logger.warning("Background runner already running")
            return

        self.running = True
        self.thread = threading.Thread(
            target=self._run_loop,
            args=(coroutine_func, args, kwargs),
            daemon=True
        )
        self.thread.start()
        logger.info("Background asyncio loop started")

    def _run_loop(self, coroutine_func, args, kwargs):
        """Internal method to run the event loop in the background thread"""
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop

        try:
            # Run the coroutine
            loop.run_until_complete(coroutine_func(*args, **kwargs))
        except Exception as e:
            logger.error(f"Error in background loop: {e}")
        finally:
            loop.close()
            self.running = False

    def stop(self):
        """Stop the background loop"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5.0)
        logger.info("Background asyncio loop stopped")


# Simplified pattern (from Bluesky dashboard)
def run_async_in_background(async_func, *args, **kwargs):
    """
    Simple function to run an async function in a background thread.

    Args:
        async_func: The async function to run
        *args, **kwargs: Arguments to pass to the function

    Returns:
        The started thread object
    """
    def thread_target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(async_func(*args, **kwargs))
        finally:
            loop.close()

    thread = threading.Thread(target=thread_target, daemon=True)
    thread.start()
    return thread


if __name__ == "__main__":
    # Example 1: Using the BackgroundAsyncRunner class
    import time

    async def sample_task(runner):
        count = 0
        while runner.is_running():
            print(f"Async task running: {count}")
            count += 1
            await asyncio.sleep(1)

    runner = BackgroundAsyncRunner()
    runner.start(sample_task, runner)

    # Do synchronous work in main thread
    time.sleep(5)
    runner.stop()

    # Example 2: Using the simple function
    async def simple_task():
        for i in range(3):
            print(f"Simple task: {i}")
            await asyncio.sleep(1)

    thread = run_async_in_background(simple_task)
    thread.join()
