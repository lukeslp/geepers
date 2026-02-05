"""
Flask Authentication and Authorization Decorators

Description: Production-ready authentication patterns using decorators for Flask routes.
Includes API key validation, JWT tokens, role-based access control, and license validation.
Demonstrates reusable decorator patterns for securing endpoints.

Use Cases:
- API key authentication for public APIs
- JWT token-based authentication
- Role-based access control (RBAC)
- License key validation for premium features
- Multi-factor authentication
- Rate limiting per user/API key

Dependencies:
- flask
- functools (wraps)
- os (environment variables)
- Optional: PyJWT for JWT tokens

Notes:
- Decorators run before route handlers
- Use @wraps to preserve function metadata
- Store user info in request context (g object)
- Return tuple (response, status_code) for errors
- Chain decorators for multiple checks
- Environment variables for secrets
- Graceful error messages for better DX

Related Snippets:
- web-frameworks/flask_middleware_patterns.py - Request/response hooks
- configuration-management/multi_source_config.py - API key storage
- error-handling/graceful_import_fallbacks.py - Optional JWT support

Source Attribution:
- Extracted from: /home/coolhand/projects/apis/omni-api/api/core/decorators.py
- Related patterns: /home/coolhand/projects/apis/omni-api/app.py
- Production deployment: https://api.assisted.space
"""

import os
import logging
from functools import wraps
from typing import Callable, Optional, List
from flask import request, jsonify, g

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Basic API Key Authentication
# ============================================================================
# Load API keys from environment
DEFAULT_API_KEY = os.getenv('DEFAULT_API_KEY', "test-key-local-dev-2024")
VALID_API_KEYS = os.getenv('VALID_API_KEYS', '').split(',')


def require_api_key(f: Callable) -> Callable:
    """
    Decorator to require valid API key in X-API-Key header.

    Usage:
        @app.route('/protected')
        @require_api_key
        def protected_endpoint():
            return jsonify({'message': 'Access granted'})

    Headers:
        X-API-Key: your-api-key-here

    Returns:
        401 if no API key provided
        401 if invalid API key
        Calls wrapped function if valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if not api_key:
            logger.warning(f"Missing API key for {request.path}")
            return jsonify({"error": "No API key provided"}), 401

        # Validate against default key or list of valid keys
        if api_key != DEFAULT_API_KEY and (not VALID_API_KEYS or api_key not in VALID_API_KEYS):
            logger.warning(f"Invalid API key attempt for {request.path}")
            return jsonify({"error": "Invalid API key"}), 401

        # Store API key in request context for logging/analytics
        g.api_key = api_key

        logger.info(f"Valid API key for {request.path}")
        return f(*args, **kwargs)

    return decorated


# ============================================================================
# JWT Token Authentication
# ============================================================================
def require_jwt_token(f: Callable) -> Callable:
    """
    Decorator to require valid JWT token in Authorization header.

    Requires PyJWT: pip install PyJWT

    Usage:
        @app.route('/protected')
        @require_jwt_token
        def protected_endpoint():
            user_id = g.user['user_id']
            return jsonify({'message': f'Hello user {user_id}'})

    Headers:
        Authorization: Bearer <jwt-token>

    Environment:
        JWT_SECRET_KEY: Secret key for JWT signing

    Returns:
        401 if no token provided
        401 if invalid/expired token
        Calls wrapped function if valid, with g.user set
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            import jwt
        except ImportError:
            logger.error("PyJWT not installed. Install with: pip install PyJWT")
            return jsonify({"error": "JWT support not available"}), 500

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({"error": "No authorization token provided"}), 401

        try:
            # Extract token from "Bearer <token>"
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header

            # Decode and validate token
            secret_key = os.getenv('JWT_SECRET_KEY')
            if not secret_key:
                logger.error("JWT_SECRET_KEY not configured")
                return jsonify({"error": "Authentication not configured"}), 500

            payload = jwt.decode(token, secret_key, algorithms=["HS256"])

            # Store user info in request context
            g.user = payload
            logger.info(f"Valid JWT token for user {payload.get('user_id')}")

            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            logger.warning("Expired JWT token")
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            logger.error(f"JWT validation error: {e}")
            return jsonify({"error": "Authentication failed"}), 401

    return decorated


# ============================================================================
# Role-Based Access Control (RBAC)
# ============================================================================
def require_role(*allowed_roles: str) -> Callable:
    """
    Decorator to require specific user roles.

    Must be used after @require_jwt_token or similar auth decorator
    that sets g.user with 'roles' field.

    Usage:
        @app.route('/admin')
        @require_jwt_token
        @require_role('admin', 'superuser')
        def admin_endpoint():
            return jsonify({'message': 'Admin access granted'})

    Args:
        *allowed_roles: One or more role names that are allowed

    Returns:
        403 if user doesn't have required role
        Calls wrapped function if user has required role
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(g, 'user'):
                logger.error("require_role used without authentication")
                return jsonify({"error": "Authentication required"}), 401

            user_roles = g.user.get('roles', [])
            if not isinstance(user_roles, list):
                user_roles = [user_roles]

            # Check if user has any of the allowed roles
            if not any(role in user_roles for role in allowed_roles):
                logger.warning(f"User {g.user.get('user_id')} lacks required role for {request.path}")
                return jsonify({"error": "Insufficient permissions"}), 403

            logger.info(f"Role check passed for {request.path}")
            return f(*args, **kwargs)

        return decorated
    return decorator


# ============================================================================
# License Key Validation
# ============================================================================
def require_valid_license(validator: Callable[[str], dict]) -> Callable:
    """
    Decorator to require valid license key.

    Usage:
        def validate_license(license_key):
            # Your license validation logic
            # Return dict with license info or raise exception
            return {'valid': True, 'tier': 'premium'}

        @app.route('/premium-feature')
        @require_valid_license(validator=validate_license)
        def premium_endpoint():
            tier = request.license_info['tier']
            return jsonify({'message': f'Access granted for {tier} tier'})

    Headers:
        X-License-Key: your-license-key-here

    Args:
        validator: Function that takes license key and returns license info dict

    Returns:
        403 if no license key provided
        403 if invalid license
        Calls wrapped function if valid, with request.license_info set
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            license_key = request.headers.get('X-License-Key')

            if not license_key:
                logger.warning(f"Missing license key for {request.path}")
                return jsonify({"error": "License key required"}), 403

            try:
                # Validate license
                license_info = validator(license_key)

                # Store license info in request context
                request.license_info = license_info
                g.license_info = license_info

                logger.info(f"Valid license for {request.path}")
                return f(*args, **kwargs)

            except Exception as e:
                logger.warning(f"Invalid license key: {e}")
                return jsonify({"error": "Invalid or expired license"}), 403

        return decorated
    return decorator


# ============================================================================
# Rate Limiting Decorator
# ============================================================================
def rate_limit(max_requests: int = 100, window_seconds: int = 60) -> Callable:
    """
    Decorator for rate limiting endpoints.

    Usage:
        @app.route('/api/search')
        @require_api_key
        @rate_limit(max_requests=10, window_seconds=60)
        def search():
            return jsonify({'results': []})

    Args:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds

    Returns:
        429 if rate limit exceeded
        Calls wrapped function if within limit

    Note: This is a simple in-memory implementation.
    For production, use Redis with proper distributed rate limiting.
    """
    import time
    from collections import defaultdict

    # In-memory storage (use Redis in production)
    request_counts = defaultdict(list)

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            # Identify user by API key or IP
            identifier = getattr(g, 'api_key', None) or request.remote_addr
            current_time = time.time()

            # Clean old requests
            request_counts[identifier] = [
                req_time for req_time in request_counts[identifier]
                if current_time - req_time < window_seconds
            ]

            # Check rate limit
            if len(request_counts[identifier]) >= max_requests:
                logger.warning(f"Rate limit exceeded for {identifier}")
                return jsonify({
                    "error": "Rate limit exceeded",
                    "retry_after": window_seconds
                }), 429

            # Record this request
            request_counts[identifier].append(current_time)

            return f(*args, **kwargs)

        return decorated
    return decorator


# ============================================================================
# Optional Authentication (Allow Anonymous)
# ============================================================================
def optional_api_key(f: Callable) -> Callable:
    """
    Decorator for optional API key authentication.

    Validates API key if provided, but allows request without one.
    Useful for endpoints with free tier and paid features.

    Usage:
        @app.route('/search')
        @optional_api_key
        def search():
            if hasattr(g, 'api_key'):
                # Authenticated user - no limits
                limit = 1000
            else:
                # Anonymous user - limited results
                limit = 10
            return jsonify({'results': [], 'limit': limit})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')

        if api_key:
            # Validate if provided
            if api_key == DEFAULT_API_KEY or (VALID_API_KEYS and api_key in VALID_API_KEYS):
                g.api_key = api_key
                g.authenticated = True
                logger.info(f"Authenticated access to {request.path}")
            else:
                logger.warning(f"Invalid API key for {request.path}")
                return jsonify({"error": "Invalid API key"}), 401
        else:
            # Allow anonymous access
            g.authenticated = False
            logger.info(f"Anonymous access to {request.path}")

        return f(*args, **kwargs)

    return decorated


# ============================================================================
# Usage Examples
# ============================================================================
if __name__ == "__main__" and False:  # Set to True to run examples
    """
    Example 1: Basic API key protection

    from flask import Flask, jsonify, g
    from auth_decorators import require_api_key

    app = Flask(__name__)

    @app.route('/protected')
    @require_api_key
    def protected():
        return jsonify({'message': 'Access granted', 'api_key': g.api_key})

    # Test:
    # curl -H "X-API-Key: test-key-local-dev-2024" http://localhost:5000/protected

    Example 2: JWT with role-based access

    from flask import Flask
    from auth_decorators import require_jwt_token, require_role

    app = Flask(__name__)

    @app.route('/admin')
    @require_jwt_token
    @require_role('admin')
    def admin_only():
        return jsonify({'message': 'Admin access granted'})

    @app.route('/user')
    @require_jwt_token
    @require_role('user', 'admin')  # Either role allowed
    def user_or_admin():
        return jsonify({'message': 'User access granted'})

    Example 3: License validation

    def my_license_validator(license_key):
        # Check against database or external service
        if license_key.startswith('VALID-'):
            return {'valid': True, 'tier': 'premium', 'expires': '2025-12-31'}
        raise ValueError("Invalid license")

    @app.route('/premium')
    @require_valid_license(validator=my_license_validator)
    def premium_feature():
        tier = request.license_info['tier']
        return jsonify({'tier': tier, 'message': 'Premium access'})

    Example 4: Rate limiting

    from auth_decorators import require_api_key, rate_limit

    @app.route('/search')
    @require_api_key
    @rate_limit(max_requests=10, window_seconds=60)
    def search():
        return jsonify({'results': []})

    Example 5: Optional authentication with tiered limits

    from auth_decorators import optional_api_key

    @app.route('/public')
    @optional_api_key
    def public_endpoint():
        if g.authenticated:
            limit = 1000
            message = "Authenticated user"
        else:
            limit = 10
            message = "Anonymous user"

        return jsonify({'limit': limit, 'message': message})

    Example 6: Combining multiple decorators

    @app.route('/super-protected')
    @require_jwt_token
    @require_role('admin')
    @rate_limit(max_requests=5, window_seconds=60)
    def super_protected():
        return jsonify({'message': 'Super protected endpoint'})

    # Decorators execute bottom-to-top:
    # 1. rate_limit checks rate
    # 2. require_role checks role
    # 3. require_jwt_token validates token
    # 4. Route handler executes

    Example 7: Custom authentication decorator

    def require_custom_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Your custom authentication logic
            auth_token = request.headers.get('X-Custom-Token')

            if not auth_token:
                return jsonify({"error": "Missing custom token"}), 401

            # Validate token (e.g., check database)
            user = validate_custom_token(auth_token)
            if not user:
                return jsonify({"error": "Invalid token"}), 401

            g.user = user
            return f(*args, **kwargs)

        return decorated

    @app.route('/custom-auth')
    @require_custom_auth
    def custom_protected():
        return jsonify({'user': g.user})
    """
    pass
