"""
Flask-SocketIO Real-Time Broadcasting Pattern

Description: Flask application with SocketIO for real-time bidirectional communication.
Demonstrates server-to-client broadcasting, client connection handling, and integration
with background data processing threads.

Use Cases:
- Real-time dashboards updating live data
- Live notifications and alerts
- Collaborative applications with multi-user updates
- Streaming data visualization
- Progress tracking for long-running tasks

Dependencies:
- Flask (pip install Flask)
- Flask-SocketIO (pip install Flask-SocketIO)
- Flask-CORS (pip install Flask-CORS)
- python-socketio (pip install python-socketio)

Notes:
- Uses async_mode='threading' for compatibility with standard Flask
- For production, use async_mode='eventlet' with gunicorn --worker-class eventlet
- SocketIO.emit() can be called from any thread (thread-safe)
- Namespace support allows organizing events by topic
- Room support enables targeted broadcasting to subsets of clients
- CORS configured for cross-origin requests

Related Snippets:
- async-patterns/asyncio_background_thread.py
- web-frameworks/flask_background_thread.py
- real-time-dashboards/websocket_firehose_reconnection.py
"""

import logging
import threading
import time
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
CORS(app)

# Initialize SocketIO
# async_mode='threading' for development, 'eventlet' for production
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


class DataBroadcaster:
    """Manages broadcasting data to connected SocketIO clients."""

    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.active_clients = set()
        self.rooms = {}  # room_name -> set of client_ids

    def broadcast_event(self, event_name: str, data: Dict[str, Any], room: str = None):
        """Broadcast an event to all clients or a specific room.

        Args:
            event_name: Name of the SocketIO event
            data: Dictionary of data to send
            room: Optional room name to broadcast to specific clients
        """
        if room:
            self.socketio.emit(event_name, data, room=room)
            logger.debug(f"Broadcast {event_name} to room {room}: {data}")
        else:
            self.socketio.emit(event_name, data)
            logger.debug(f"Broadcast {event_name} to all: {data}")

    def broadcast_to_all(self, event_name: str, data: Dict[str, Any]):
        """Convenience method to broadcast to all connected clients."""
        self.broadcast_event(event_name, data)

    def get_client_count(self) -> int:
        """Get the number of active clients."""
        return len(self.active_clients)


# Global broadcaster instance
broadcaster = DataBroadcaster(socketio)


# SocketIO Event Handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    client_id = request.sid
    broadcaster.active_clients.add(client_id)
    logger.info(f'Client connected: {client_id} (total: {broadcaster.get_client_count()})')

    # Send initial connection response
    emit('connection_response', {
        'status': 'connected',
        'client_id': client_id,
        'timestamp': time.time()
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    client_id = request.sid
    broadcaster.active_clients.discard(client_id)

    # Remove from all rooms
    for room_name, clients in list(broadcaster.rooms.items()):
        clients.discard(client_id)
        if not clients:
            del broadcaster.rooms[room_name]

    logger.info(f'Client disconnected: {client_id} (total: {broadcaster.get_client_count()})')


@socketio.on('join')
def handle_join(data):
    """Handle client joining a room.

    Args:
        data: Dict with 'room' key specifying room name
    """
    room = data.get('room')
    if room:
        join_room(room)
        client_id = request.sid

        if room not in broadcaster.rooms:
            broadcaster.rooms[room] = set()
        broadcaster.rooms[room].add(client_id)

        logger.info(f'Client {client_id} joined room: {room}')
        emit('room_joined', {'room': room, 'status': 'success'})


@socketio.on('leave')
def handle_leave(data):
    """Handle client leaving a room.

    Args:
        data: Dict with 'room' key specifying room name
    """
    room = data.get('room')
    if room:
        leave_room(room)
        client_id = request.sid

        if room in broadcaster.rooms:
            broadcaster.rooms[room].discard(client_id)
            if not broadcaster.rooms[room]:
                del broadcaster.rooms[room]

        logger.info(f'Client {client_id} left room: {room}')
        emit('room_left', {'room': room, 'status': 'success'})


@socketio.on('message')
def handle_message(data):
    """Handle custom messages from clients.

    Args:
        data: Message data from client
    """
    logger.info(f'Received message from {request.sid}: {data}')
    # Echo back or process as needed
    emit('message_received', {'status': 'received', 'original': data})


# Flask HTTP Routes
@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/broadcast', methods=['POST'])
def trigger_broadcast():
    """HTTP endpoint to trigger a broadcast (for testing or external triggers).

    Request Body:
        event (str): Event name
        data (dict): Data to broadcast
        room (str, optional): Room to broadcast to
    """
    payload = request.get_json()
    event_name = payload.get('event', 'update')
    data = payload.get('data', {})
    room = payload.get('room')

    broadcaster.broadcast_event(event_name, data, room)

    return jsonify({
        'status': 'broadcasted',
        'event': event_name,
        'clients': broadcaster.get_client_count()
    })


@app.route('/api/stats')
def get_stats():
    """Get current connection statistics."""
    return jsonify({
        'active_clients': broadcaster.get_client_count(),
        'rooms': {name: len(clients) for name, clients in broadcaster.rooms.items()}
    })


# Example: Background thread broadcasting periodic updates
def background_data_generator():
    """Example background thread that broadcasts data periodically."""
    counter = 0
    while True:
        time.sleep(5)  # Update every 5 seconds
        counter += 1

        # Broadcast update to all clients
        broadcaster.broadcast_to_all('periodic_update', {
            'counter': counter,
            'timestamp': time.time(),
            'message': f'Update #{counter}'
        })

        logger.info(f'Broadcasted periodic update #{counter}')


# Start background thread (optional)
def start_background_tasks():
    """Start background tasks for data generation."""
    thread = threading.Thread(target=background_data_generator, daemon=True)
    thread.start()
    logger.info("Background data generator started")


if __name__ == '__main__':
    # Optionally start background tasks
    # start_background_tasks()

    logger.info("Starting Flask-SocketIO server")
    logger.info("Navigate to http://localhost:5000")

    # For development
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)

    # For production, use gunicorn with eventlet:
    # gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
