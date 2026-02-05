"""
Flask Application Factory Pattern with Blueprints

Description: Production-grade Flask application using factory pattern for testing and configuration
flexibility. Demonstrates blueprint organization, caching configuration with Redis fallback, response
compression, and modular route registration.

Use Cases:
- Building scalable Flask applications with multiple modules
- Supporting multiple deployment environments (dev, test, prod)
- Implementing caching with graceful degradation
- Organizing routes into logical blueprints
- Creating testable Flask applications

Dependencies:
- flask
- flask-cors
- flask-caching
- flask-compress
- redis (optional, falls back to SimpleCache)

Notes:
- Factory pattern allows multiple app instances with different configs
- Auto-detects Redis availability and falls back gracefully
- Blueprint pattern organizes routes by domain (corpus, ngrams, analysis)
- Template and static folders configured with absolute paths
- Cache timeout configurable per-route with decorator
- Environment-based configuration using Config class

Related Snippets:
- error-handling/graceful_import_fallbacks.py - Optional Redis handling
- configuration-management/multi_source_config.py - Advanced configuration
- web-frameworks/flask_blueprint_organization.py - Blueprint patterns

Source Attribution:
- Extracted from: /home/coolhand/servers/coca/app/__init__.py
- Related patterns: /home/coolhand/servers/analytics/app.py
- Production deployment: https://dr.eamer.dev/coca
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from flask_compress import Compress

# Initialize extensions at module level
cache = Cache()
compress = Compress()


class Config:
    """
    Base configuration class.

    Override these values with environment variables or subclass for
    different environments (DevelopmentConfig, ProductionConfig, etc.)
    """
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

    # Template settings
    TEMPLATES_AUTO_RELOAD = True

    # Cache settings
    CACHE_TYPE = 'SimpleCache'  # Will be overridden if Redis available
    CACHE_DEFAULT_TIMEOUT = 3600  # 1 hour
    CACHE_REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    CACHE_REDIS_DB = int(os.environ.get('REDIS_DB', 0))

    # Application-specific settings
    MAX_RESULTS = 1000
    DEFAULT_LIMIT = 100


def create_app(config_class=Config):
    """
    Application factory for creating Flask instances.

    Args:
        config_class: Configuration class to use (defaults to Config)

    Returns:
        Flask: Configured Flask application instance

    Example:
        app = create_app(ProductionConfig)
        app.run()
    """
    # Create Flask app with properly configured directories
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
                static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))

    # Load configuration
    app.config.from_object(config_class)

    # Enable CORS for all routes
    CORS(app)

    # Enable response compression (gzip)
    compress.init_app(app)

    # Configure caching with Redis fallback
    _configure_cache(app)

    # Ensure required directories exist
    _ensure_directories(app)

    # Register blueprints
    _register_blueprints(app)

    return app


def _configure_cache(app):
    """
    Configure caching with automatic Redis detection and fallback.

    Tries to connect to Redis first. If Redis is not available, falls back
    to SimpleCache (in-memory). This provides graceful degradation without
    requiring Redis in development.
    """
    try:
        import redis

        # Test Redis connection
        redis_client = redis.Redis(
            host=app.config['CACHE_REDIS_HOST'],
            port=app.config['CACHE_REDIS_PORT'],
            db=app.config['CACHE_REDIS_DB'],
            socket_timeout=1
        )
        redis_client.ping()

        # Redis available - use it
        cache.init_app(app, config={
            'CACHE_TYPE': 'RedisCache',
            'CACHE_REDIS_HOST': app.config['CACHE_REDIS_HOST'],
            'CACHE_REDIS_PORT': app.config['CACHE_REDIS_PORT'],
            'CACHE_REDIS_DB': app.config['CACHE_REDIS_DB'],
            'CACHE_DEFAULT_TIMEOUT': app.config['CACHE_DEFAULT_TIMEOUT']
        })
        print("✓ Using Redis cache for better performance")

    except Exception:
        # Fall back to SimpleCache if Redis not available
        cache.init_app(app, config={
            'CACHE_TYPE': 'SimpleCache',
            'CACHE_DEFAULT_TIMEOUT': app.config['CACHE_DEFAULT_TIMEOUT']
        })
        print("⚠ Redis not available, using SimpleCache (restart with Redis for better performance)")


def _ensure_directories(app):
    """Ensure required directories exist."""
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'), exist_ok=True)


def _register_blueprints(app):
    """
    Register all application blueprints.

    Blueprints organize routes by domain. Each blueprint is registered
    with a URL prefix for clean separation.
    """
    # Import blueprints (lazy import to avoid circular dependencies)
    from app.routes.corpus import bp as corpus_bp
    from app.routes.ngrams import bp as ngrams_bp
    from app.routes.analysis import bp as analysis_bp
    from app.routes.dashboard import bp as dashboard_bp
    from app.routes.index import bp as index_bp

    # Register blueprints with URL prefixes
    app.register_blueprint(index_bp)  # Root routes (no prefix)
    app.register_blueprint(corpus_bp, url_prefix='/api/corpus')
    app.register_blueprint(ngrams_bp, url_prefix='/api/ngrams')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    print(f"✓ Registered {len(app.blueprints)} blueprints")


# ============================================================================
# Example Blueprint Structure
# ============================================================================
# This would be in app/routes/corpus.py
"""
from flask import Blueprint, jsonify, request
from app import cache  # Import cache from __init__.py

bp = Blueprint('corpus', __name__)

@bp.route('/search', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def search():
    '''
    Cached search endpoint.

    Cache key includes query string, so different queries are cached separately.
    '''
    query = request.args.get('q', '')
    # ... search logic ...
    return jsonify({'results': []})

@bp.route('/health', methods=['GET'])
def health():
    '''Health check (not cached)'''
    return jsonify({'status': 'healthy'})
"""


# ============================================================================
# Usage Examples
# ============================================================================
if __name__ == "__main__" and False:  # Set to True to run examples
    """
    Example 1: Create app with default config

    from app import create_app

    app = create_app()
    app.run(port=5000)

    Example 2: Create app with custom config

    class DevelopmentConfig(Config):
        DEBUG = True
        CACHE_TYPE = 'SimpleCache'

    app = create_app(DevelopmentConfig)
    app.run(port=5000)

    Example 3: Testing with app factory

    import pytest

    @pytest.fixture
    def app():
        class TestConfig(Config):
            TESTING = True
            CACHE_TYPE = 'NullCache'  # Disable cache for tests

        app = create_app(TestConfig)
        return app

    @pytest.fixture
    def client(app):
        return app.test_client()

    def test_health_check(client):
        response = client.get('/health')
        assert response.status_code == 200

    Example 4: Production deployment with Gunicorn

    # Save factory to run.py:
    from app import create_app

    app = create_app()

    if __name__ == '__main__':
        app.run()

    # Run with Gunicorn:
    # gunicorn -w 4 -b 0.0.0.0:5000 run:app

    Example 5: Environment-specific configuration

    import os

    class ProductionConfig(Config):
        DEBUG = False
        SECRET_KEY = os.environ.get('SECRET_KEY')
        CACHE_TYPE = 'RedisCache'
        CACHE_REDIS_HOST = os.environ.get('REDIS_HOST', 'redis-server')
        CACHE_REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

    class DevelopmentConfig(Config):
        DEBUG = True
        CACHE_TYPE = 'SimpleCache'

    # Select config based on environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }

    app = create_app(configs[config_name])

    Example 6: Using cache in blueprints

    from flask import Blueprint
    from app import cache

    bp = Blueprint('api', __name__)

    @bp.route('/expensive-operation')
    @cache.cached(timeout=300)
    def expensive_operation():
        # This result is cached for 5 minutes
        result = perform_expensive_calculation()
        return jsonify(result)

    @bp.route('/search')
    @cache.cached(timeout=3600, query_string=True)
    def search():
        # Different query strings get different cache keys
        query = request.args.get('q')
        results = search_database(query)
        return jsonify(results)

    # Manual cache operations
    @bp.route('/clear-cache')
    def clear_cache():
        cache.clear()
        return jsonify({'message': 'Cache cleared'})

    Example 7: Multiple app instances (testing)

    # Create multiple apps with different configurations
    dev_app = create_app(DevelopmentConfig)
    test_app = create_app(TestConfig)
    prod_app = create_app(ProductionConfig)

    # Each has independent configuration and state
    """
    pass


# ============================================================================
# Production Deployment Script (run.py)
# ============================================================================
def create_production_app():
    """
    Example production application entry point.

    Save this as run.py in your project root:
    """
    from app import create_app

    class ProductionConfig(Config):
        DEBUG = False
        SECRET_KEY = os.environ.get('SECRET_KEY')
        # Production-specific settings

    app = create_app(ProductionConfig)
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting application on port {port}")
    print(f"Debug mode: {app.config['DEBUG']}")
    print(f"Cache type: {app.config.get('CACHE_TYPE', 'Not configured')}")
    app.run(host='0.0.0.0', port=port)
