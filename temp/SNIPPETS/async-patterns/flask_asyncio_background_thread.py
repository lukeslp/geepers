"""
Flask + Asyncio Background Thread Integration

Description: Pattern for running asyncio event loops in background threads alongside Flask
applications. Enables async tasks (WebSocket clients, async APIs) to run concurrently with
Flask's synchronous HTTP server without blocking request handling.

Use Cases:
- WebSocket client consuming real-time data streams while serving HTTP API
- Background async tasks (data polling, API calls) with Flask frontend
- Integrating async libraries (aiohttp, asyncio, websockets) with Flask
- Long-running async operations without blocking Flask responses
- Combining Flask-SocketIO (synchronous) with asyncio WebSocket clients

Dependencies:
- asyncio (standard library)
- threading (standard library)
- Flask (pip install Flask)

Notes:
- Each asyncio event loop runs in its own thread with isolated state
- Use daemon=True for threads to auto-terminate when main process exits
- asyncio.new_event_loop() required because threads don't have event loops by default
- Communication between Flask and async thread via thread-safe data structures
- For production, ensure graceful shutdown handling
- Flask-SocketIO can trigger async operations via threading.Thread

Performance Considerations:
- Background thread doesn't block Flask request handling
- GIL (Global Interpreter Lock) may limit CPU-bound parallelism
- I/O-bound async tasks work well (network calls, file I/O)
- Multiple background threads can run different async event loops

Related Snippets:
- websocket-patterns/websocket_firehose_reconnection.py
- real-time-dashboards/flask_socketio_broadcaster.py
- async-patterns/asyncio_task_queue.py
"""

import asyncio
import logging
import threading
from typing import Callable, Optional
import time

from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncBackgroundRunner:
    """Manages an asyncio event loop running in a background thread."""

    def __init__(self, name: str = "AsyncWorker"):
        """Initialize the async background runner.

        Args:
            name: Name for the background thread (for logging/debugging)
        """
        self.name = name
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.thread: Optional[threading.Thread] = None
        self.running = False

    def start(self, coro_func: Callable, *args, **kwargs):
        """Start the background thread with an async coroutine.

        Args:
            coro_func: Async function to run in background
            *args: Positional arguments for coro_func
            **kwargs: Keyword arguments for coro_func
        """
        if self.running:
            logger.warning(f"{self.name} already running")
            return

        self.running = True

        def run_in_thread():
            """Run the event loop in a background thread."""
            # Create new event loop for this thread
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            try:
                logger.info(f"{self.name} thread started")
                # Run the coroutine until complete or stopped
                self.loop.run_until_complete(coro_func(*args, **kwargs))
            except Exception as e:
                logger.error(f"{self.name} error: {e}")
            finally:
                # Clean up
                self.loop.close()
                logger.info(f"{self.name} thread stopped")

        # Start thread as daemon so it exits when main process exits
        self.thread = threading.Thread(target=run_in_thread, daemon=True, name=self.name)
        self.thread.start()

    def stop(self):
        """Stop the background thread gracefully."""
        self.running = False
        if self.loop and self.loop.is_running():
            # Stop the loop from another thread
            self.loop.call_soon_threadsafe(self.loop.stop)

    def is_alive(self) -> bool:
        """Check if the background thread is alive."""
        return self.thread.is_alive() if self.thread else False


# Example: Async worker function
async def example_async_worker(runner: AsyncBackgroundRunner):
    """Example async function that runs in background.

    Args:
        runner: AsyncBackgroundRunner instance for checking running state
    """
    counter = 0
    while runner.running:
        counter += 1
        logger.info(f"Async worker tick #{counter}")
        await asyncio.sleep(5)  # Simulate async work


# Example: WebSocket firehose consumer in background
async def websocket_consumer(runner: AsyncBackgroundRunner, uri: str, handler: Callable):
    """Example WebSocket consumer running in background.

    Args:
        runner: AsyncBackgroundRunner instance
        uri: WebSocket URI to connect to
        handler: Callback function to handle messages
    """
    import websockets
    import json

    while runner.running:
        try:
            logger.info(f"Connecting to WebSocket: {uri}")
            async with websockets.connect(uri) as websocket:
                logger.info("WebSocket connected")

                while runner.running:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                        data = json.loads(message)
                        # Call handler in a separate thread to avoid blocking
                        threading.Thread(target=handler, args=(data,), daemon=True).start()
                    except asyncio.TimeoutError:
                        logger.debug("WebSocket timeout, continuing...")
                        continue
                    except Exception as e:
                        logger.error(f"Message processing error: {e}")
                        break

        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            if runner.running:
                logger.info("Reconnecting in 5 seconds...")
                await asyncio.sleep(5)


# Flask application with async background thread
app = Flask(__name__)

# Global background runner
background_runner = AsyncBackgroundRunner(name="DataProcessor")

# Shared state (use thread-safe structures in production)
shared_state = {
    'message_count': 0,
    'last_message': None,
    'status': 'stopped'
}


def handle_incoming_data(data: dict):
    """Handler for data from async background thread.

    This runs in a separate thread and updates shared state.

    Args:
        data: Data received from async source
    """
    shared_state['message_count'] += 1
    shared_state['last_message'] = data
    logger.debug(f"Handled message #{shared_state['message_count']}")


@app.route('/api/start', methods=['POST'])
def start_background():
    """Start the background async worker."""
    if background_runner.is_alive():
        return jsonify({'status': 'already_running'})

    # Start the async worker
    background_runner.start(example_async_worker, background_runner)
    shared_state['status'] = 'running'

    return jsonify({'status': 'started'})


@app.route('/api/stop', methods=['POST'])
def stop_background():
    """Stop the background async worker."""
    background_runner.stop()
    shared_state['status'] = 'stopped'

    return jsonify({'status': 'stopped'})


@app.route('/api/status')
def get_status():
    """Get background worker status and stats."""
    return jsonify({
        'thread_alive': background_runner.is_alive(),
        'running': background_runner.running,
        'status': shared_state['status'],
        'message_count': shared_state['message_count'],
        'last_message': shared_state['last_message']
    })


# Application lifecycle
def initialize_app():
    """Initialize application and start background tasks."""
    logger.info("Initializing application...")

    # Optionally auto-start background task
    # background_runner.start(example_async_worker, background_runner)

    logger.info("Application initialized")


def shutdown_app():
    """Clean shutdown of background tasks."""
    logger.info("Shutting down application...")
    background_runner.stop()
    logger.info("Application shutdown complete")


if __name__ == '__main__':
    # Initialize
    initialize_app()

    try:
        # Run Flask app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        shutdown_app()


# Alternative pattern: Multiple background tasks
class MultiAsyncRunner:
    """Manage multiple async background tasks in a single event loop."""

    def __init__(self):
        self.runner = AsyncBackgroundRunner(name="MultiTaskRunner")
        self.tasks = []

    async def run_multiple_tasks(self, *coro_funcs):
        """Run multiple async functions concurrently.

        Args:
            *coro_funcs: Async functions to run concurrently
        """
        # Create tasks for all coroutines
        self.tasks = [asyncio.create_task(coro()) for coro in coro_funcs]

        try:
            # Wait for all tasks
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            logger.info("Tasks cancelled")

    def start(self, *coro_funcs):
        """Start multiple async tasks in background thread.

        Args:
            *coro_funcs: Async functions to run concurrently
        """
        self.runner.start(self.run_multiple_tasks, *coro_funcs)

    def stop(self):
        """Stop all background tasks."""
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        self.runner.stop()


# Example usage of MultiAsyncRunner
async def task1():
    """Example async task 1."""
    while True:
        logger.info("Task 1 running")
        await asyncio.sleep(3)


async def task2():
    """Example async task 2."""
    while True:
        logger.info("Task 2 running")
        await asyncio.sleep(5)


if __name__ == '__main__':
    # Example: Run multiple tasks
    multi_runner = MultiAsyncRunner()
    multi_runner.start(task1, task2)

    # Keep main thread alive
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    finally:
        multi_runner.stop()
