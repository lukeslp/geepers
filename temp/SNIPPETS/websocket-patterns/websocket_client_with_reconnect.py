"""
WebSocket Client with Auto-Reconnection

Description: Robust WebSocket client pattern with automatic reconnection, timeout handling,
and graceful error recovery. Based on the websockets library for async Python.

Use Cases:
- Connecting to real-time data streams (Bluesky firehose, crypto exchanges, etc.)
- Building resilient WebSocket clients for production environments
- Consuming server-sent events or streaming APIs
- Long-running WebSocket connections with automatic recovery

Dependencies:
- websockets>=12.0
- asyncio (standard library)

Notes:
- Implements exponential backoff for reconnection attempts
- Handles timeout, connection errors, and JSON parsing errors
- Graceful shutdown with state management
- Message processing can emit to SocketIO, write to database, or process data

Related Snippets:
- async-patterns/asyncio_background_thread.py
- web-frameworks/flask_socketio_setup.py
- real-time-dashboards/socketio_emit_from_background.py
"""

import asyncio
import json
import logging
from typing import Optional, Callable
import websockets
from websockets.exceptions import WebSocketException

logger = logging.getLogger(__name__)


class WebSocketClient:
    """
    Auto-reconnecting WebSocket client with robust error handling.

    Example Usage:
        async def message_handler(data):
            print(f"Received: {data}")

        client = WebSocketClient(
            uri="wss://example.com/stream",
            message_handler=message_handler
        )

        await client.connect()
    """

    def __init__(
        self,
        uri: str,
        message_handler: Callable,
        reconnect_delay: int = 5,
        timeout: float = 30.0,
        max_reconnect_attempts: Optional[int] = None
    ):
        """
        Initialize WebSocket client.

        Args:
            uri: WebSocket URL to connect to
            message_handler: Async function to process received messages
            reconnect_delay: Seconds to wait before reconnecting (default: 5)
            timeout: Timeout for receiving messages (default: 30.0)
            max_reconnect_attempts: Max reconnection attempts (None = infinite)
        """
        self.uri = uri
        self.message_handler = message_handler
        self.reconnect_delay = reconnect_delay
        self.timeout = timeout
        self.max_reconnect_attempts = max_reconnect_attempts
        self.running = False
        self.reconnect_count = 0

    async def connect(self):
        """
        Connect to WebSocket and process messages with auto-reconnection.
        """
        self.running = True

        while self.running:
            try:
                logger.info(f"Connecting to {self.uri}...")

                async with websockets.connect(self.uri) as websocket:
                    logger.info("WebSocket connected")
                    self.reconnect_count = 0  # Reset on successful connection

                    while self.running:
                        try:
                            # Receive message with timeout
                            message = await asyncio.wait_for(
                                websocket.recv(),
                                timeout=self.timeout
                            )

                            # Parse JSON if applicable
                            try:
                                data = json.loads(message)
                            except json.JSONDecodeError:
                                data = message

                            # Process message
                            await self.message_handler(data)

                        except asyncio.TimeoutError:
                            logger.warning("WebSocket timeout, checking connection...")
                            # Send ping to check if connection is alive
                            try:
                                pong = await websocket.ping()
                                await asyncio.wait_for(pong, timeout=10)
                            except Exception:
                                logger.error("Connection lost, reconnecting...")
                                break
                            continue

                        except json.JSONDecodeError as e:
                            logger.error(f"JSON decode error: {e}")
                            continue

                        except Exception as e:
                            logger.error(f"Error processing message: {e}")
                            continue

            except WebSocketException as e:
                logger.error(f"WebSocket error: {e}")
            except Exception as e:
                logger.error(f"Connection error: {e}")

            # Reconnection logic
            if self.running:
                self.reconnect_count += 1

                if (self.max_reconnect_attempts and
                    self.reconnect_count > self.max_reconnect_attempts):
                    logger.error("Max reconnection attempts reached")
                    break

                logger.info(f"Reconnecting in {self.reconnect_delay} seconds... "
                           f"(attempt {self.reconnect_count})")
                await asyncio.sleep(self.reconnect_delay)
            else:
                break

        logger.info("WebSocket client stopped")

    def stop(self):
        """Stop the WebSocket client"""
        self.running = False


# Simplified pattern from Bluesky dashboard
async def process_websocket_stream(uri: str, running_flag, message_callback):
    """
    Simplified WebSocket stream processing pattern.

    Args:
        uri: WebSocket URL
        running_flag: Object with .running attribute to control the loop
        message_callback: Function to call for each message

    Example:
        class State:
            running = True

        state = State()

        def handle_message(data):
            print(f"Got: {data}")

        await process_websocket_stream(
            "wss://example.com/stream",
            state,
            handle_message
        )
    """
    while running_flag.running:
        try:
            logger.info(f"Connecting to {uri}...")

            async with websockets.connect(uri) as websocket:
                logger.info("Connected to WebSocket stream")

                while running_flag.running:
                    try:
                        # Receive message with timeout
                        message = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                        data = json.loads(message)

                        # Process message
                        message_callback(data)

                    except asyncio.TimeoutError:
                        logger.warning("Timeout, checking connection...")
                        continue
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        continue

        except Exception as e:
            logger.error(f"Connection error: {e}")
            if running_flag.running:
                logger.info("Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            else:
                break


if __name__ == "__main__":
    # Example usage
    async def handle_message(data):
        print(f"Received message: {data}")

    async def main():
        client = WebSocketClient(
            uri="wss://echo.websocket.org",
            message_handler=handle_message,
            reconnect_delay=3,
            timeout=30.0
        )

        # Start client (will run until stopped)
        await client.connect()

    asyncio.run(main())
