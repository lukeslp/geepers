"""
Gunicorn + Eventlet Configuration for Flask-SocketIO Apps

Description: Production deployment configuration for Flask-SocketIO applications using
Gunicorn with eventlet worker class. This pattern enables WebSocket support, long-polling
fallback, and proper async I/O handling in production environments.

Use Cases:
- Production deployment of Flask-SocketIO applications
- Real-time dashboards and notification systems
- WebSocket-based collaborative applications
- Live data streaming applications
- Any Flask app requiring bidirectional client-server communication

Dependencies:
- gunicorn (pip install gunicorn)
- eventlet (pip install eventlet)
- Flask-SocketIO (pip install Flask-SocketIO)
- Flask (pip install Flask)

Notes:
- Eventlet worker class required for SocketIO WebSocket support
- Use -w 1 (single worker) to avoid session affinity issues
- For multi-worker setup, use Redis/RabbitMQ message queue
- async_mode='eventlet' must match gunicorn worker class
- Eventlet uses greenlets for concurrency (cooperative multitasking)
- Default Flask werkzeug server NOT suitable for production SocketIO

Production Considerations:
- Single worker sufficient for 1000s of concurrent SocketIO connections
- For horizontal scaling, add Redis/RabbitMQ and use sticky sessions
- Monitor memory usage - eventlet is memory efficient but track per-connection overhead
- Use nginx/caddy reverse proxy for SSL, static files, and load balancing
- Set proper timeouts for long-lived connections

Performance:
- Single worker handles ~5000-10000 concurrent WebSocket connections
- CPU-bound tasks should be offloaded to background workers
- Eventlet excels at I/O-bound workloads

Related Snippets:
- real-time-dashboards/flask_socketio_broadcaster.py
- web-frameworks/flask_app_factory.py
- deployment/systemd_service_template.sh
"""

# app.py - Flask-SocketIO Application
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# CRITICAL: async_mode must be 'eventlet' to match gunicorn worker class
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


@app.route('/')
def index():
    return "Flask-SocketIO Server Running"


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# Don't use socketio.run() for production!
# Let gunicorn handle the server
if __name__ == '__main__':
    # Development only
    socketio.run(app, host='0.0.0.0', port=5000)
