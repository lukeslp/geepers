"""
Flask-SocketIO Setup for Real-Time Applications

Description: Complete Flask-SocketIO configuration with CORS, threading mode,
and proper initialization for real-time bidirectional communication.

Use Cases:
- Real-time dashboards with live data updates
- Chat applications
- Notification systems
- Live monitoring and analytics
- Collaborative editing tools

Dependencies:
- Flask>=3.0.0
- Flask-SocketIO>=5.3.0
- Flask-CORS>=4.0.0
- python-socketio>=5.11.0
- eventlet>=0.35.2 (for production with Gunicorn)

Notes:
- Use async_mode='threading' for development
- Use async_mode='eventlet' with Gunicorn in production
- CORS configured for cross-origin requests
- emit() can broadcast to all clients or target specific rooms
- Production deployment requires: gunicorn --worker-class eventlet -w 1 app:app

Related Snippets:
- real-time-dashboards/socketio_emit_from_background.py
- async-patterns/asyncio_background_thread.py
- web-frameworks/flask_cors_configuration.py
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Enable CORS for cross-origin requests
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize SocketIO
# async_mode='threading' for development
# async_mode='eventlet' for production with Gunicorn
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    logger=True,
    engineio_logger=False
)


# ===== WebSocket Event Handlers =====

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f'Client connected: {request.sid}')
    emit('connection_response', {
        'status': 'connected',
        'sid': request.sid
    })


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f'Client disconnected: {request.sid}')


@socketio.on('join')
def handle_join(data):
    """Handle client joining a room"""
    room = data.get('room')
    if room:
        join_room(room)
        logger.info(f'Client {request.sid} joined room: {room}')
        emit('room_joined', {'room': room}, room=request.sid)


@socketio.on('leave')
def handle_leave(data):
    """Handle client leaving a room"""
    room = data.get('room')
    if room:
        leave_room(room)
        logger.info(f'Client {request.sid} left room: {room}')
        emit('room_left', {'room': room}, room=request.sid)


@socketio.on('message')
def handle_message(data):
    """Handle generic message from client"""
    logger.info(f'Message from {request.sid}: {data}')
    # Echo back to sender
    emit('message_response', {'data': data}, room=request.sid)


@socketio.on('broadcast')
def handle_broadcast(data):
    """Handle broadcast message to all clients"""
    logger.info(f'Broadcasting from {request.sid}: {data}')
    # Broadcast to all connected clients
    emit('broadcast_message', data, broadcast=True)


# ===== HTTP Routes =====

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy'}, 200


# ===== Utility Functions for Emitting from Background Threads =====

def emit_to_all(event_name: str, data: dict):
    """
    Emit event to all connected clients from background thread.

    Args:
        event_name: Name of the event
        data: Data to send

    Note:
        This is the correct way to emit from background threads in Flask-SocketIO.
    """
    socketio.emit(event_name, data, namespace='/')


def emit_to_room(event_name: str, data: dict, room: str):
    """
    Emit event to specific room from background thread.

    Args:
        event_name: Name of the event
        data: Data to send
        room: Room identifier
    """
    socketio.emit(event_name, data, room=room, namespace='/')


def emit_to_client(event_name: str, data: dict, sid: str):
    """
    Emit event to specific client from background thread.

    Args:
        event_name: Name of the event
        data: Data to send
        sid: Client session ID
    """
    socketio.emit(event_name, data, room=sid, namespace='/')


# ===== Application Startup =====

if __name__ == '__main__':
    logger.info("Starting Flask-SocketIO application")
    logger.info("Navigate to http://localhost:5000")

    # Development server
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=False,
        allow_unsafe_werkzeug=True  # Only for development
    )


# ===== Production Deployment =====
"""
For production deployment with Gunicorn:

1. Install eventlet:
   pip install eventlet gunicorn

2. Run with Gunicorn:
   gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app

3. Or with daemon mode:
   gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app \\
       --daemon \\
       --pid app.pid \\
       --access-logfile access.log \\
       --error-logfile error.log

4. IMPORTANT: Use only 1 worker (-w 1) for WebSocket support
"""

# ===== Client-Side JavaScript Example =====
"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
</head>
<body>
    <script>
        const socket = io();

        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('connection_response', (data) => {
            console.log('Connection response:', data);
        });

        socket.on('broadcast_message', (data) => {
            console.log('Broadcast:', data);
        });

        // Send message
        socket.emit('message', {text: 'Hello server'});

        // Join room
        socket.emit('join', {room: 'room1'});

        // Broadcast to all
        socket.emit('broadcast', {text: 'Hello everyone'});
    </script>
</body>
</html>
"""
