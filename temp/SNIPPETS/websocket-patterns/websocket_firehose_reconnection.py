"""
WebSocket Firehose Connection with Auto-Reconnection

Description: Robust asyncio-based WebSocket client for consuming real-time data streams
(firehoses) with automatic reconnection, timeout handling, and graceful error recovery.

Use Cases:
- Consuming real-time data streams (Bluesky, Twitter, etc.)
- Long-running WebSocket connections requiring high reliability
- Event-driven data processing pipelines
- Real-time monitoring systems

Dependencies:
- websockets (pip install websockets)
- asyncio (standard library)

Notes:
- Uses asyncio.wait_for() for timeout handling to detect stale connections
- Implements exponential backoff for reconnection (configurable)
- Separates connection management from message processing for clarity
- State management allows graceful shutdown via external flag
- JSON decoding errors handled separately to avoid breaking connection

Related Snippets:
- async-patterns/asyncio_background_thread.py
- streaming-patterns/real_time_data_processor.py
- error-handling/retry_with_backoff.py
"""

import asyncio
import json
import logging
from typing import Callable, Optional

import websockets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketFirehoseClient:
    """WebSocket client for consuming real-time data streams with auto-reconnection."""

    def __init__(
        self,
        uri: str,
        message_handler: Callable[[dict], None],
        timeout: float = 30.0,
        reconnect_delay: int = 5,
        max_reconnect_delay: int = 60,
    ):
        """Initialize the WebSocket firehose client.

        Args:
            uri: WebSocket URI to connect to
            message_handler: Callback function to process each message (receives dict)
            timeout: Timeout in seconds for receiving messages (default: 30.0)
            reconnect_delay: Initial delay in seconds before reconnecting (default: 5)
            max_reconnect_delay: Maximum delay for exponential backoff (default: 60)
        """
        self.uri = uri
        self.message_handler = message_handler
        self.timeout = timeout
        self.reconnect_delay = reconnect_delay
        self.max_reconnect_delay = max_reconnect_delay
        self.running = False

    async def start(self):
        """Start consuming the firehose. Runs until stopped."""
        self.running = True
        current_delay = self.reconnect_delay

        while self.running:
            try:
                logger.info(f"Connecting to firehose: {self.uri}")
                async with websockets.connect(self.uri) as websocket:
                    logger.info("Connected to firehose")
                    # Reset delay on successful connection
                    current_delay = self.reconnect_delay

                    while self.running:
                        try:
                            # Wait for message with timeout
                            message = await asyncio.wait_for(
                                websocket.recv(), timeout=self.timeout
                            )

                            # Parse JSON
                            try:
                                data = json.loads(message)
                                # Process message via callback
                                self.message_handler(data)
                            except json.JSONDecodeError as e:
                                logger.warning(f"Invalid JSON: {e}")
                                continue

                        except asyncio.TimeoutError:
                            logger.warning(
                                f"WebSocket timeout after {self.timeout}s, checking connection..."
                            )
                            # Send ping to check if connection is alive
                            try:
                                pong = await websocket.ping()
                                await asyncio.wait_for(pong, timeout=5)
                            except Exception:
                                logger.error("Connection appears dead, reconnecting...")
                                break
                            continue

                        except websockets.exceptions.ConnectionClosed:
                            logger.warning("WebSocket connection closed")
                            break

                        except Exception as e:
                            logger.error(f"Error processing message: {e}")
                            continue

            except Exception as e:
                logger.error(f"Firehose connection error: {e}")
                if self.running:
                    logger.info(f"Reconnecting in {current_delay} seconds...")
                    await asyncio.sleep(current_delay)
                    # Exponential backoff
                    current_delay = min(current_delay * 2, self.max_reconnect_delay)
                else:
                    break

        logger.info("Firehose client stopped")

    def stop(self):
        """Stop the firehose client gracefully."""
        self.running = False


# Example usage with Bluesky firehose
if __name__ == "__main__":

    def handle_post(data: dict):
        """Example message handler for Bluesky posts."""
        if data.get("kind") == "commit":
            commit = data.get("commit", {})
            if commit.get("collection") == "app.bsky.feed.post":
                record = commit.get("record", {})
                text = record.get("text", "")
                if text:
                    print(f"New post: {text[:100]}")

    # Initialize client
    client = WebSocketFirehoseClient(
        uri="wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post",
        message_handler=handle_post,
        timeout=30.0,
        reconnect_delay=5,
    )

    # Run until Ctrl+C
    try:
        asyncio.run(client.start())
    except KeyboardInterrupt:
        print("\nStopping firehose client...")
        client.stop()
