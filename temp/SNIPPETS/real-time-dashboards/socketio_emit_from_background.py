"""
SocketIO Emission from Background Threads

Description: Pattern for emitting SocketIO events from background asyncio tasks or threads
to update real-time dashboards. Critical for separating data processing from presentation.

Use Cases:
- Real-time dashboards with background data collection
- Live monitoring systems
- Streaming data visualization
- WebSocket-to-SocketIO bridges
- Background task status updates

Dependencies:
- Flask-SocketIO>=5.3.0
- threading (standard library)

Notes:
- Use socketio.emit() directly (NOT emit() from flask_socketio)
- Works from any thread, including asyncio background loops
- Can broadcast to all clients or target specific rooms
- Namespace defaults to '/' if not specified
- Combine with deque for efficient buffering

Related Snippets:
- async-patterns/asyncio_background_thread.py
- web-frameworks/flask_socketio_setup.py
- real-time-dashboards/dashboard_state_management.py
"""

import threading
import asyncio
import logging
from collections import deque
from typing import Dict, Any
from flask import Flask
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)


class RealtimeDataEmitter:
    """
    Manages real-time data emission from background threads to SocketIO clients.

    Example Usage:
        app = Flask(__name__)
        socketio = SocketIO(app)
        emitter = RealtimeDataEmitter(socketio)

        # From background thread
        emitter.emit_update('new_data', {'value': 42})

        # From asyncio coroutine
        async def process_stream():
            async for item in stream:
                emitter.emit_update('stream_item', item)
    """

    def __init__(self, socketio: SocketIO, namespace: str = '/'):
        """
        Initialize emitter.

        Args:
            socketio: Flask-SocketIO instance
            namespace: SocketIO namespace (default: '/')
        """
        self.socketio = socketio
        self.namespace = namespace

    def emit_update(self, event: str, data: Dict[str, Any], room: str = None):
        """
        Emit update to clients from any thread.

        Args:
            event: Event name
            data: Data to send
            room: Optional room to target (broadcasts to all if None)
        """
        try:
            self.socketio.emit(
                event,
                data,
                namespace=self.namespace,
                room=room
            )
        except Exception as e:
            logger.error(f"Error emitting {event}: {e}")

    def emit_to_all(self, event: str, data: Dict[str, Any]):
        """Broadcast to all connected clients"""
        self.emit_update(event, data, room=None)

    def emit_to_room(self, event: str, data: Dict[str, Any], room: str):
        """Emit to specific room"""
        self.emit_update(event, data, room=room)


class BufferedEmitter:
    """
    Buffers events and emits periodically to reduce SocketIO overhead.

    Example Usage:
        emitter = BufferedEmitter(socketio, flush_interval=1.0)
        emitter.start()

        # Queue events (won't emit immediately)
        emitter.queue_event('metric', {'value': 1})
        emitter.queue_event('metric', {'value': 2})

        # Events will be flushed every 1 second
    """

    def __init__(
        self,
        socketio: SocketIO,
        flush_interval: float = 1.0,
        namespace: str = '/'
    ):
        """
        Initialize buffered emitter.

        Args:
            socketio: Flask-SocketIO instance
            flush_interval: Seconds between flushes
            namespace: SocketIO namespace
        """
        self.socketio = socketio
        self.namespace = namespace
        self.flush_interval = flush_interval
        self.buffer = deque()
        self.running = False
        self.thread = None

    def queue_event(self, event: str, data: Dict[str, Any], room: str = None):
        """Add event to buffer"""
        self.buffer.append({
            'event': event,
            'data': data,
            'room': room
        })

    def start(self):
        """Start background flushing"""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._flush_loop, daemon=True)
        self.thread.start()
        logger.info("BufferedEmitter started")

    def stop(self):
        """Stop background flushing"""
        self.running = False
        self._flush_buffer()  # Flush remaining events
        if self.thread:
            self.thread.join(timeout=5.0)
        logger.info("BufferedEmitter stopped")

    def _flush_loop(self):
        """Background loop to flush buffer periodically"""
        import time

        while self.running:
            time.sleep(self.flush_interval)
            self._flush_buffer()

    def _flush_buffer(self):
        """Emit all buffered events"""
        while self.buffer:
            event_data = self.buffer.popleft()
            try:
                self.socketio.emit(
                    event_data['event'],
                    event_data['data'],
                    namespace=self.namespace,
                    room=event_data['room']
                )
            except Exception as e:
                logger.error(f"Error flushing event: {e}")


# Simple pattern from Bluesky dashboard
def emit_from_background_thread(socketio, event_name: str, data: dict):
    """
    Simple function to emit SocketIO event from background thread.

    Args:
        socketio: Flask-SocketIO instance
        event_name: Name of event
        data: Data to send

    Example:
        # In background async function
        async def process_data():
            while True:
                item = await get_data()
                emit_from_background_thread(socketio, 'new_item', item)
    """
    socketio.emit(event_name, data)


# Example integration with asyncio background task
async def stream_processor_with_emit(socketio, stream_url: str, running_flag):
    """
    Example: Process async stream and emit to SocketIO.

    Args:
        socketio: Flask-SocketIO instance
        stream_url: WebSocket URL to connect to
        running_flag: Object with .running attribute
    """
    import websockets
    import json

    emitter = RealtimeDataEmitter(socketio)

    async with websockets.connect(stream_url) as websocket:
        while running_flag.running:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                data = json.loads(message)

                # Emit to all connected clients
                emitter.emit_to_all('stream_update', data)

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Stream processing error: {e}")
                continue


if __name__ == "__main__":
    # Example usage
    from flask import Flask
    from flask_socketio import SocketIO
    import time

    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")

    # Example 1: Simple emitter
    emitter = RealtimeDataEmitter(socketio)

    def background_worker():
        """Simulate background data generation"""
        for i in range(10):
            time.sleep(1)
            emitter.emit_to_all('counter', {'value': i})

    # Example 2: Buffered emitter
    buffered = BufferedEmitter(socketio, flush_interval=2.0)
    buffered.start()

    def fast_worker():
        """Generate many events quickly - will be batched"""
        for i in range(100):
            buffered.queue_event('fast_metric', {'value': i})
            time.sleep(0.01)

    # Start background workers
    threading.Thread(target=background_worker, daemon=True).start()
    threading.Thread(target=fast_worker, daemon=True).start()

    @app.route('/')
    def index():
        return "Real-time emitter demo"

    socketio.run(app, port=5000)
