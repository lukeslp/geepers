# Gunicorn + Eventlet Deployment Guide for Flask-SocketIO

## Overview

This guide covers production deployment of Flask-SocketIO applications using Gunicorn with the eventlet worker class.

## Quick Start

### Basic Command

```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

### With All Recommended Options

```bash
gunicorn \
  --worker-class eventlet \
  -w 1 \
  --bind 0.0.0.0:5000 \
  --timeout 120 \
  --keepalive 5 \
  --log-level info \
  --access-logfile access.log \
  --error-logfile error.log \
  app:app
```

## Configuration Breakdown

### Worker Class
```bash
--worker-class eventlet
```
**Required** for SocketIO. Uses greenlets for async I/O and WebSocket support.

### Worker Count
```bash
-w 1
```
**Single worker recommended** to avoid session affinity issues. One worker can handle thousands of concurrent connections.

For multi-worker (advanced):
```bash
-w 4  # Requires Redis/RabbitMQ message queue
```

### Binding
```bash
--bind 0.0.0.0:5000          # Listen on all interfaces, port 5000
--bind 127.0.0.1:5000         # Localhost only (with reverse proxy)
--bind unix:/tmp/app.sock     # Unix socket (nginx integration)
```

### Timeouts
```bash
--timeout 120                 # Worker timeout (seconds)
--keepalive 5                 # Keep-alive connections timeout
--graceful-timeout 30         # Graceful shutdown timeout
```

### Logging
```bash
--log-level info              # debug, info, warning, error, critical
--access-logfile access.log   # HTTP access logs
--error-logfile error.log     # Application errors
--capture-output              # Capture stdout/stderr to error log
```

### Process Management
```bash
--daemon                      # Run as background daemon
--pid gunicorn.pid           # Write PID file
--user www-data              # Run as specific user
--group www-data             # Run as specific group
```

## Startup Scripts

### Simple Startup Script (start.sh)

```bash
#!/bin/bash
set -e

echo "Starting Flask-SocketIO application..."

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -q -r requirements.txt

# Start with gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

### Production Startup Script with Logging

```bash
#!/bin/bash
set -e

APP_NAME="my-socketio-app"
PORT=5000
WORKERS=1
LOG_DIR="logs"
PID_FILE="${APP_NAME}.pid"

# Create log directory
mkdir -p ${LOG_DIR}

# Activate virtual environment
source venv/bin/activate

echo "Starting ${APP_NAME} on port ${PORT}..."

# Start gunicorn
gunicorn \
  --worker-class eventlet \
  -w ${WORKERS} \
  --bind 0.0.0.0:${PORT} \
  --timeout 120 \
  --keepalive 5 \
  --log-level info \
  --access-logfile ${LOG_DIR}/access.log \
  --error-logfile ${LOG_DIR}/error.log \
  --pid ${PID_FILE} \
  --daemon \
  app:app

echo "${APP_NAME} started with PID $(cat ${PID_FILE})"
```

### Stop Script

```bash
#!/bin/bash
PID_FILE="my-socketio-app.pid"

if [ -f ${PID_FILE} ]; then
    PID=$(cat ${PID_FILE})
    echo "Stopping process ${PID}..."
    kill -TERM ${PID}
    rm ${PID_FILE}
    echo "Stopped."
else
    echo "PID file not found. Trying pkill..."
    pkill -f "gunicorn.*app:app"
fi
```

## Systemd Service (Recommended for Production)

Create `/etc/systemd/system/socketio-app.service`:

```ini
[Unit]
Description=Flask-SocketIO Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/app
Environment="PATH=/path/to/app/venv/bin"

ExecStart=/path/to/app/venv/bin/gunicorn \
    --worker-class eventlet \
    -w 1 \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --log-level info \
    --access-logfile /var/log/socketio-app/access.log \
    --error-logfile /var/log/socketio-app/error.log \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable socketio-app
sudo systemctl start socketio-app
sudo systemctl status socketio-app
```

## Reverse Proxy Configuration

### Nginx

```nginx
upstream socketio_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://socketio_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeouts for long-lived connections
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

### Caddy (Simplest)

```
example.com {
    reverse_proxy localhost:5000
}
```

Caddy automatically handles WebSocket upgrades and HTTPS.

## Multi-Worker Setup with Redis

For horizontal scaling across multiple workers or servers.

### Install Redis Message Queue

```bash
pip install redis
```

### Update Flask App

```python
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Use Redis message queue for multi-worker
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    message_queue='redis://localhost:6379/0'
)
```

### Start Multiple Workers

```bash
gunicorn --worker-class eventlet -w 4 --bind 0.0.0.0:5000 app:app
```

## Monitoring and Health Checks

### Add Health Check Endpoint

```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

### Monitor Gunicorn

```bash
# View logs
tail -f logs/error.log

# Check process
ps aux | grep gunicorn

# Monitor connections
ss -tnp | grep :5000
```

## Troubleshooting

### WebSocket Connection Fails

**Check async_mode matches worker class:**
```python
# app.py
socketio = SocketIO(app, async_mode='eventlet')  # Must match --worker-class
```

**Run with:**
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

### High Memory Usage

- Monitor per-connection memory: `ps aux | grep gunicorn`
- Consider connection limits in nginx/caddy
- Use single worker unless message queue configured

### Connections Drop After Timeout

- Increase gunicorn timeout: `--timeout 300`
- Configure reverse proxy timeouts (nginx/caddy)
- Enable keepalive: `--keepalive 5`

### Workers Timeout

- Check for blocking operations in request handlers
- Offload CPU-intensive tasks to background workers
- Increase `--timeout` if processing long requests

## Performance Tuning

### Recommended Settings for Different Scales

**Small (< 100 concurrent connections):**
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:app
```

**Medium (100-1000 connections):**
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 \
  --timeout 120 --keepalive 5 app:app
```

**Large (1000-5000 connections):**
```bash
gunicorn --worker-class eventlet -w 2 --bind 0.0.0.0:5000 \
  --timeout 300 --keepalive 10 \
  --message-queue redis://localhost:6379/0 \
  app:app
```

**Very Large (5000+ connections):**
- Use Redis message queue
- Multiple workers (2-4)
- Multiple servers with load balancer
- Connection pooling in reverse proxy
- Consider upgrading to dedicated WebSocket server (e.g., Socket.IO standalone)

## Requirements File

```txt
Flask==3.0.0
Flask-SocketIO==5.3.6
Flask-CORS==4.0.0
gunicorn==21.2.0
eventlet==0.35.2
redis==5.0.0  # For multi-worker
```

## References

- Flask-SocketIO: https://flask-socketio.readthedocs.io/
- Gunicorn: https://docs.gunicorn.org/
- Eventlet: https://eventlet.net/
