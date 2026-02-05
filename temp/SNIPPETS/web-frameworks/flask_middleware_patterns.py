"""
Flask Middleware and Request/Response Hooks

Description: Comprehensive patterns for Flask middleware using before_request, after_request,
and custom middleware classes. Includes analytics tracking, authentication, request timing,
and CORS handling. Production-ready patterns for cross-cutting concerns.

Use Cases:
- API request analytics and monitoring
- Authentication and authorization
- Request/response timing and logging
- Custom CORS handling for specific origins
- Background task triggering (analytics, logging)
- Request ID tracking and correlation

Dependencies:
- flask
- requests (for analytics posting)
- logging
- threading (for background tasks)

Notes:
- Middleware runs before/after every request
- Use threading for non-blocking analytics
- Request context provides storage for request-scoped data
- Skip middleware for specific endpoints (static files, health checks)
- Middleware execution order matters
- Error handling prevents middleware from breaking app

Related Snippets:
- web-frameworks/flask_authentication_decorators.py - Auth patterns
- configuration-management/multi_source_config.py - Configuration
- error-handling/graceful_import_fallbacks.py - Optional dependencies

Source Attribution:
- Extracted from: /home/coolhand/servers/analytics/flask_middleware.py
- Related patterns: /home/coolhand/html/storyblocks/api_proxy.py
- Production deployment: https://dr.eamer.dev/analytics
"""

import time
import logging
import threading
from typing import Optional, Callable
from functools import wraps

from flask import Flask, request, g
import requests


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Analytics Middleware Class
# ============================================================================
class AnalyticsMiddleware:
    """
    Flask middleware for automatic API endpoint usage tracking.

    Tracks every request with response time, status code, endpoint,
    and sends analytics to a separate analytics service in background.

    Usage:
        from flask import Flask
        from analytics_middleware import AnalyticsMiddleware

        app = Flask(__name__)
        AnalyticsMiddleware(app, app_name='my-api')
    """

    def __init__(self, app: Flask, app_name: str = 'flask-app',
                 analytics_url: str = 'http://localhost:5014'):
        """
        Initialize analytics middleware.

        Args:
            app: Flask application instance
            app_name: Name to identify this app in analytics
            analytics_url: URL of analytics service
        """
        self.app = app
        self.app_name = app_name
        self.analytics_url = analytics_url

        # Register before and after request handlers
        app.before_request(self._before_request)
        app.after_request(self._after_request)

    def _before_request(self):
        """Record request start time."""
        request._analytics_start_time = time.time()

    def _after_request(self, response):
        """
        Track API call after request completes.

        Calculates response time and sends analytics in background thread
        to avoid blocking the response.
        """
        # Skip tracking for static files and health checks
        if request.endpoint in ['static', 'health'] or request.path.startswith('/static'):
            return response

        # Calculate response time
        response_time = (time.time() - getattr(request, '_analytics_start_time', time.time())) * 1000

        # Prepare tracking data
        data = {
            'endpoint': request.path,
            'method': request.method,
            'status_code': response.status_code,
            'response_time': round(response_time, 2),
            'ip': self._get_client_ip(),
            'user_agent': request.headers.get('User-Agent', ''),
            'app_name': self.app_name
        }

        # Send analytics in background thread to avoid blocking response
        threading.Thread(target=self._send_analytics, args=(data,), daemon=True).start()

        return response

    def _get_client_ip(self) -> str:
        """
        Get client IP, handling proxies.

        Checks X-Forwarded-For header for proxied requests.
        """
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        return request.remote_addr or 'unknown'

    def _send_analytics(self, data: dict):
        """
        Send analytics data (runs in background thread).

        Silently fails if analytics service is unavailable.
        """
        try:
            requests.post(
                f'{self.analytics_url}/track/api',
                json=data,
                timeout=2
            )
        except Exception:
            # Silently fail - don't let analytics break the app
            pass


# ============================================================================
# Request Timing Middleware
# ============================================================================
def timing_middleware(app: Flask):
    """
    Add request timing to all endpoints.

    Logs request duration and adds X-Response-Time header.

    Usage:
        app = Flask(__name__)
        timing_middleware(app)
    """

    @app.before_request
    def before_request():
        """Record request start time."""
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        """Calculate and log response time."""
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            response.headers['X-Response-Time'] = f"{elapsed * 1000:.2f}ms"
            logger.info(f"{request.method} {request.path} - {response.status_code} - {elapsed * 1000:.2f}ms")
        return response


# ============================================================================
# Request ID Middleware
# ============================================================================
def request_id_middleware(app: Flask):
    """
    Add unique request ID to each request.

    Useful for tracking requests across distributed systems.

    Usage:
        app = Flask(__name__)
        request_id_middleware(app)
    """
    import uuid

    @app.before_request
    def before_request():
        """Generate or extract request ID."""
        request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
        g.request_id = request_id

    @app.after_request
    def after_request(response):
        """Add request ID to response headers."""
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        return response


# ============================================================================
# CORS Middleware with Origin Validation
# ============================================================================
def cors_middleware(app: Flask, allowed_origins: list):
    """
    Custom CORS middleware with origin validation.

    More control than flask-cors extension for complex CORS requirements.

    Args:
        app: Flask application
        allowed_origins: List of allowed origin patterns

    Usage:
        app = Flask(__name__)
        cors_middleware(app, [
            'https://example.com',
            'http://localhost',
            'http://127.0.0.1'
        ])
    """

    @app.after_request
    def after_request(response):
        """Add CORS headers to response."""
        origin = request.headers.get('Origin')

        if origin and any(origin.startswith(allowed) for allowed in allowed_origins):
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add('Access-Control-Allow-Headers',
                                 'Content-Type,Authorization,X-Requested-With,X-Request-ID')
            response.headers.add('Access-Control-Allow-Methods',
                                 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Max-Age', '3600')
            response.headers.add('Access-Control-Expose-Headers',
                                 'X-Response-Time,X-Request-ID')

        return response


# ============================================================================
# Authentication Middleware
# ============================================================================
def auth_middleware(app: Flask, exempt_endpoints: Optional[list] = None):
    """
    Simple token-based authentication middleware.

    Args:
        app: Flask application
        exempt_endpoints: List of endpoint names to skip auth

    Usage:
        app = Flask(__name__)
        auth_middleware(app, exempt_endpoints=['health', 'static'])
    """
    from flask import jsonify

    if exempt_endpoints is None:
        exempt_endpoints = ['health', 'static']

    @app.before_request
    def before_request():
        """Check authentication before request."""
        # Skip auth for exempt endpoints
        if request.endpoint in exempt_endpoints or request.path.startswith('/static'):
            return None

        # Check for API key in headers
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "No API key provided"}), 401

        # Validate API key (implement your validation logic)
        if not _validate_api_key(api_key):
            return jsonify({"error": "Invalid API key"}), 401

        # Store user info in g for use in endpoints
        g.user = _get_user_from_api_key(api_key)
        return None


def _validate_api_key(api_key: str) -> bool:
    """Validate API key (implement your logic)."""
    # Example: check against database or environment variable
    import os
    valid_keys = os.environ.get('VALID_API_KEYS', '').split(',')
    return api_key in valid_keys


def _get_user_from_api_key(api_key: str) -> dict:
    """Get user info from API key (implement your logic)."""
    return {'api_key': api_key, 'user_id': 'example_user'}


# ============================================================================
# Error Handling Middleware
# ============================================================================
def error_handling_middleware(app: Flask):
    """
    Centralized error handling for all requests.

    Catches unhandled exceptions and returns JSON error responses.

    Usage:
        app = Flask(__name__)
        error_handling_middleware(app)
    """
    from flask import jsonify

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request."""
        return jsonify({"error": "Bad request", "message": str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized."""
        return jsonify({"error": "Unauthorized", "message": str(error)}), 401

    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden."""
        return jsonify({"error": "Forbidden", "message": str(error)}), 403

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found."""
        return jsonify({"error": "Not found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server Error."""
        logger.error(f"Internal error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions."""
        logger.exception(f"Unhandled exception: {error}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# ============================================================================
# Combined Middleware Setup
# ============================================================================
def setup_middleware(app: Flask, config: dict):
    """
    Setup all middleware for a Flask application.

    Args:
        app: Flask application
        config: Configuration dictionary with middleware settings

    Example config:
        {
            'analytics': {
                'enabled': True,
                'app_name': 'my-api',
                'url': 'http://localhost:5014'
            },
            'cors': {
                'enabled': True,
                'origins': ['https://example.com', 'http://localhost']
            },
            'auth': {
                'enabled': True,
                'exempt_endpoints': ['health', 'docs']
            }
        }

    Usage:
        app = Flask(__name__)
        setup_middleware(app, config)
    """
    # Always setup timing and request ID
    timing_middleware(app)
    request_id_middleware(app)
    error_handling_middleware(app)

    # Optional middleware based on config
    if config.get('analytics', {}).get('enabled'):
        analytics_config = config['analytics']
        AnalyticsMiddleware(
            app,
            app_name=analytics_config.get('app_name', 'flask-app'),
            analytics_url=analytics_config.get('url', 'http://localhost:5014')
        )

    if config.get('cors', {}).get('enabled'):
        cors_config = config['cors']
        cors_middleware(app, cors_config.get('origins', []))

    if config.get('auth', {}).get('enabled'):
        auth_config = config['auth']
        auth_middleware(app, auth_config.get('exempt_endpoints'))

    logger.info("Middleware setup complete")


# ============================================================================
# Usage Examples
# ============================================================================
if __name__ == "__main__" and False:  # Set to True to run examples
    """
    Example 1: Basic analytics middleware

    from flask import Flask
    from flask_middleware_patterns import AnalyticsMiddleware

    app = Flask(__name__)
    AnalyticsMiddleware(app, app_name='my-api', analytics_url='http://localhost:5014')

    @app.route('/test')
    def test():
        return {'message': 'Hello'}

    app.run()

    Example 2: Multiple middleware

    from flask import Flask
    from flask_middleware_patterns import timing_middleware, request_id_middleware

    app = Flask(__name__)
    timing_middleware(app)
    request_id_middleware(app)

    @app.route('/test')
    def test():
        return {'message': 'Hello', 'request_id': g.request_id}

    app.run()

    Example 3: Full middleware stack

    from flask import Flask
    from flask_middleware_patterns import setup_middleware

    app = Flask(__name__)

    config = {
        'analytics': {
            'enabled': True,
            'app_name': 'production-api',
            'url': 'https://analytics.example.com'
        },
        'cors': {
            'enabled': True,
            'origins': ['https://app.example.com', 'http://localhost:3000']
        },
        'auth': {
            'enabled': True,
            'exempt_endpoints': ['health', 'docs', 'metrics']
        }
    }

    setup_middleware(app, config)

    @app.route('/protected')
    def protected():
        return {'message': 'Protected endpoint', 'user': g.user}

    @app.route('/health')
    def health():
        return {'status': 'healthy'}

    app.run()

    Example 4: Custom middleware

    from flask import Flask, g
    import time

    app = Flask(__name__)

    @app.before_request
    def log_request_info():
        g.start_time = time.time()
        logger.info(f"Request: {request.method} {request.path}")

    @app.after_request
    def log_response_info(response):
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            logger.info(f"Response: {response.status_code} - {elapsed:.3f}s")
        return response

    @app.teardown_request
    def cleanup(error=None):
        if error:
            logger.error(f"Request error: {error}")
        # Cleanup resources

    app.run()
    """
    pass
