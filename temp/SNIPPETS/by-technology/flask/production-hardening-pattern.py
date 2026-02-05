"""Flask Production Hardening Pattern
Implements security, performance, and observability best practices.

Author: Luke Steuber
Date: 2025-12-17
Source: Etymology Visualizer + COCA Corpus API patterns

Features:
- Environment-based configuration (SECRET_KEY from env)
- Input validation (length limits, character restrictions)
- Rate limiting (Flask-Limiter)
- Response compression (gzip)
- CORS with domain restrictions
- Structured logging with rotation
- Custom error handlers (404, 429, 500)
- Path traversal protection

Dependencies:
    pip install flask flask-cors flask-compress flask-limiter

Usage:
    1. Copy this pattern to your Flask app
    2. Customize CORS origins, rate limits, validation rules
    3. Set SECRET_KEY environment variable in production
    4. Configure log directory path
"""
import os
import re
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, abort, send_from_directory
from flask_cors import CORS
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

# Enable CORS with domain restrictions
CORS(app, origins=[
    'https://dr.eamer.dev',
    'https://d.reamwalker.com',
    'https://d.reamwalk.com',
    'http://localhost:*'  # Allow local development
])

# Enable response compression (gzip)
Compress(app)

# Configure rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["1000 per day", "100 per hour"],
    storage_uri="memory://"  # Use Redis for production: "redis://localhost:6379/0"
)

# Configure structured logging with rotation
log_dir = '/var/log/myapp'  # Customize this
os.makedirs(log_dir, exist_ok=True)

file_handler = RotatingFileHandler(
    os.path.join(log_dir, 'app.log'),
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Also configure root logger for module logs
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    handlers=[file_handler]
)
logger = logging.getLogger(__name__)

# Input validation constants
MAX_INPUT_LENGTH = 200
VALID_INPUT_PATTERN = re.compile(r'^[a-zA-Z0-9\-\s]+$')


def validate_input(value: str, field_name: str = 'input') -> tuple[bool, str]:
    """Validate user input and return (is_valid, error_message).

    Args:
        value: Input string to validate
        field_name: Name of field for error messages

    Returns:
        Tuple of (is_valid: bool, error_message: str)

    Example:
        is_valid, error = validate_input(user_input, 'word')
        if not is_valid:
            return jsonify({'error': error}), 400
    """
    if not value:
        return False, f'{field_name} is required'
    if len(value) > MAX_INPUT_LENGTH:
        return False, f'{field_name} too long (max {MAX_INPUT_LENGTH} characters)'
    if not VALID_INPUT_PATTERN.match(value):
        return False, f'{field_name} contains invalid characters'
    return True, ''


# Custom error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 Not Found errors."""
    logger.warning(f"404 Not Found: {e}")
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(429)
def rate_limit_exceeded(e):
    """Handle 429 Rate Limit Exceeded errors."""
    logger.warning(f"Rate limit exceeded: {e}")
    return jsonify({'success': False, 'error': 'Rate limit exceeded'}), 429


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 Internal Server Error."""
    logger.error(f"Internal error: {e}")
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# Path traversal protection
def safe_serve_file(directory: str, filename: str):
    """Safely serve file with path traversal protection.

    Args:
        directory: Base directory to serve from
        filename: Requested filename

    Returns:
        Flask response with file content

    Raises:
        404: If filename contains path traversal attempts

    Example:
        @app.route('/files/<path:filename>')
        def serve_file(filename):
            return safe_serve_file('/var/data', filename)
    """
    safe_filename = secure_filename(filename)
    if '..' in filename or filename != safe_filename:
        abort(404)
    return send_from_directory(directory, safe_filename)


# Example API endpoint with validation
@app.route('/api/example', methods=['POST'])
@limiter.limit("30 per minute")  # Per-endpoint rate limit
def example_endpoint():
    """Example endpoint demonstrating validation and error handling."""
    from flask import request

    if not request.is_json:
        return jsonify({'success': False, 'error': 'JSON required'}), 400

    data = request.get_json()
    user_input = data.get('input', '').strip()

    # Validate input
    is_valid, error = validate_input(user_input, 'input')
    if not is_valid:
        logger.warning(f"Invalid input: {error}")
        return jsonify({'success': False, 'error': error}), 400

    try:
        # Process request
        result = process_request(user_input)
        logger.info(f"Successful request: {user_input}")
        return jsonify({'success': True, 'result': result})

    except Exception as e:
        logger.exception(f"Error processing request: {e}")
        return jsonify({'success': False, 'error': 'Processing failed'}), 500


def process_request(input_value: str):
    """Placeholder for business logic."""
    return {'input': input_value, 'processed': True}


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
