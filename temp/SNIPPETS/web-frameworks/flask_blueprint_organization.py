"""
Flask Blueprint Organization Patterns

Description: Comprehensive patterns for organizing Flask applications using blueprints.
Demonstrates route organization, service layer pattern, caching decorators, error handling,
and modular architecture for large-scale applications.

Use Cases:
- Organizing routes by domain/resource (users, products, orders)
- Creating RESTful API structures
- Implementing caching at route level
- Separating business logic from route handlers (service layer)
- Building modular, testable applications
- Supporting multiple API versions

Dependencies:
- flask
- flask-caching
- logging

Notes:
- Blueprints provide namespace isolation
- URL prefixes organize API structure
- Service layer separates business logic from routes
- Factory functions for service instantiation per-request
- Cache decorators support query string parameters
- Error handlers can be blueprint-specific
- Blueprint registration order doesn't matter

Related Snippets:
- web-frameworks/flask_factory_pattern_with_blueprints.py - App factory
- web-frameworks/flask_middleware_patterns.py - Middleware
- api-clients/multi_provider_abstraction.py - Service patterns

Source Attribution:
- Extracted from: /home/coolhand/servers/coca/app/routes/corpus.py
- Related patterns: /home/coolhand/servers/coca/app/routes/ngrams.py
- Production deployment: https://dr.eamer.dev/coca/api/corpus
"""

import logging
from typing import List, Optional, Dict, Any
from flask import Blueprint, jsonify, request
from app import cache  # Assuming cache is initialized in app/__init__.py

# Configure logging
logger = logging.getLogger(__name__)


# ============================================================================
# Blueprint Definition Pattern
# ============================================================================
# Create blueprint with URL prefix
bp = Blueprint('corpus', __name__, url_prefix='/api/corpus')

# Alternative: No URL prefix (set when registering)
# bp = Blueprint('corpus', __name__)
# app.register_blueprint(corpus_bp, url_prefix='/api/corpus')


# ============================================================================
# Service Layer Pattern
# ============================================================================
class CorpusService:
    """
    Service layer for business logic.

    Separates data access and business logic from route handlers.
    Makes code testable and reusable.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize service with optional configuration."""
        self.config = config or {}
        logger.info("CorpusService initialized")

    def search(self, query: str, genre: str = '', search_type: str = 'word',
               limit: int = 100, window: int = 20) -> List[Dict[str, Any]]:
        """
        Search corpus for matching entries.

        Args:
            query: Search term
            genre: Filter by genre
            search_type: Type of search (word, lemma, pos)
            limit: Maximum results
            window: Context window size

        Returns:
            List of search results
        """
        logger.info(f"Searching for '{query}' (type={search_type}, genre={genre})")

        # Business logic here
        results = []  # Implement actual search

        return results

    def count_occurrences(self, query: str, genre: str = '',
                          search_type: str = 'word') -> int:
        """Count total occurrences of query."""
        logger.info(f"Counting occurrences for '{query}'")
        # Implement counting logic
        return 0

    def get_collocations(self, word: str, genre: str = '', window_size: int = 5,
                         limit: int = 50, max_contexts: int = 100) -> List[Dict[str, Any]]:
        """Get collocations for a word."""
        logger.info(f"Getting collocations for '{word}'")
        # Implement collocation logic
        return []

    def get_available_genres(self) -> List[str]:
        """Get list of available genres."""
        return ['academic', 'fiction', 'news', 'spoken', 'web']


# Factory function for service instantiation
def get_corpus_service() -> CorpusService:
    """
    Get corpus service instance.

    Factory pattern allows different implementations for testing.
    Can also read configuration from app.config.
    """
    return CorpusService()


# ============================================================================
# RESTful Route Patterns
# ============================================================================
@bp.route('/search', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def search():
    """
    Main search endpoint with caching.

    Query Parameters:
        q (str): Search query (required)
        genre (str): Filter by genre (optional)
        type (str): Search type - word, lemma, or pos (default: word)
        limit (int): Max results (default: 100)
        window (int): Context window size (default: 20)

    Returns:
        JSON response with search results

    Example:
        GET /api/corpus/search?q=linguistics&genre=academic&limit=50
    """
    try:
        # Extract and validate parameters
        query = request.args.get('q', '')
        genre = request.args.get('genre', '')
        search_type = request.args.get('type', 'word')
        limit = int(request.args.get('limit', 100))
        window = int(request.args.get('window', 20))

        # Validation
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400

        if search_type not in ['word', 'lemma', 'pos']:
            return jsonify({'error': 'Invalid search type'}), 400

        # Use service layer
        corpus_service = get_corpus_service()
        results = corpus_service.search(query, genre, search_type, limit, window)
        total_count = corpus_service.count_occurrences(query, genre, search_type)

        # Format response
        response = {
            'query': query,
            'genre': genre if genre else 'all',
            'count': len(results),
            'total_count': total_count,
            'search_type': search_type,
            'context_window': window,
            'results': results
        }

        logger.info(f"Search for '{query}' returned {len(results)} of {total_count} results")
        return jsonify(response)

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': 'Invalid parameters'}), 400
    except Exception as e:
        logger.error(f"Error in search endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@bp.route('/count', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def count():
    """
    Count occurrences endpoint.

    Query Parameters:
        q (str): Search query (required)
        genre (str): Filter by genre (optional)
        type (str): Search type (default: word)

    Returns:
        JSON with count data
    """
    try:
        query = request.args.get('q', '')
        genre = request.args.get('genre', '')
        search_type = request.args.get('type', 'word')

        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400

        corpus_service = get_corpus_service()
        total_count = corpus_service.count_occurrences(query, genre, search_type)

        return jsonify({
            'query': query,
            'genre': genre if genre else 'all',
            'search_type': search_type,
            'total_count': total_count
        })

    except Exception as e:
        logger.error(f"Error in count endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/collocations', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def collocations():
    """
    Get collocations for a word.

    Query Parameters:
        word (str): Target word (required)
        genre (str): Filter by genre (optional)
        window (int): Window size (default: 5)
        limit (int): Max results (default: 50)
        max_contexts (int): Max contexts to analyze (default: 100)

    Returns:
        JSON with collocation data
    """
    try:
        word = request.args.get('word', '')
        genre = request.args.get('genre', '')
        window = int(request.args.get('window', 5))
        limit = int(request.args.get('limit', 50))
        max_contexts = int(request.args.get('max_contexts', 100))

        if not word:
            return jsonify({'error': 'Word parameter is required'}), 400

        corpus_service = get_corpus_service()
        collocations = corpus_service.get_collocations(
            word, genre, window, limit, max_contexts
        )

        return jsonify({
            'word': word,
            'genre': genre if genre else 'all',
            'count': len(collocations),
            'window_size': window,
            'collocations': collocations
        })

    except Exception as e:
        logger.error(f"Error in collocations endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/genres', methods=['GET'])
def genres():
    """
    Get available genres.

    Returns:
        JSON with list of genres
    """
    try:
        corpus_service = get_corpus_service()
        available_genres = corpus_service.get_available_genres()

        return jsonify({'genres': available_genres})

    except Exception as e:
        logger.error(f"Error in genres endpoint: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Blueprint-Specific Error Handlers
# ============================================================================
@bp.errorhandler(400)
def bad_request(error):
    """Handle 400 errors for this blueprint."""
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400


@bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors for this blueprint."""
    return jsonify({'error': 'Resource not found'}), 404


@bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors for this blueprint."""
    logger.error(f"Internal error in corpus blueprint: {error}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# Health Check Endpoint
# ============================================================================
@bp.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint (not cached).

    Returns:
        JSON with health status
    """
    return jsonify({
        'status': 'healthy',
        'blueprint': 'corpus',
        'version': '1.0.0'
    })


# ============================================================================
# Example: Multi-Version Blueprint Pattern
# ============================================================================
# v1/routes.py
bp_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@bp_v1.route('/users', methods=['GET'])
def get_users_v1():
    """Version 1 of users endpoint."""
    return jsonify({'users': [], 'version': 'v1'})


# v2/routes.py
bp_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')


@bp_v2.route('/users', methods=['GET'])
def get_users_v2():
    """Version 2 of users endpoint with additional features."""
    return jsonify({'users': [], 'version': 'v2', 'count': 0})


# Registration in app factory:
# app.register_blueprint(bp_v1)
# app.register_blueprint(bp_v2)


# ============================================================================
# Example: Nested Blueprints Pattern
# ============================================================================
# Parent blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Child blueprint
users_bp = Blueprint('admin_users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
def list_users():
    """List all users."""
    return jsonify({'users': []})


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user."""
    return jsonify({'user_id': user_id})


# Register child to parent
admin_bp.register_blueprint(users_bp)

# Then register parent to app:
# app.register_blueprint(admin_bp)
# Creates routes: /admin/users/ and /admin/users/<id>


# ============================================================================
# Usage Examples
# ============================================================================
if __name__ == "__main__" and False:  # Set to True to run examples
    """
    Example 1: Basic blueprint registration

    from flask import Flask
    from routes.corpus import bp as corpus_bp

    app = Flask(__name__)
    app.register_blueprint(corpus_bp)
    # Creates routes under /api/corpus/*

    Example 2: Multiple blueprints

    from flask import Flask
    from routes.corpus import bp as corpus_bp
    from routes.ngrams import bp as ngrams_bp
    from routes.analysis import bp as analysis_bp

    app = Flask(__name__)
    app.register_blueprint(corpus_bp, url_prefix='/api/corpus')
    app.register_blueprint(ngrams_bp, url_prefix='/api/ngrams')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')

    Example 3: Testing blueprints

    import pytest
    from flask import Flask
    from routes.corpus import bp, CorpusService

    @pytest.fixture
    def app():
        app = Flask(__name__)
        app.register_blueprint(bp)
        return app

    @pytest.fixture
    def client(app):
        return app.test_client()

    def test_search(client):
        response = client.get('/api/corpus/search?q=test')
        assert response.status_code == 200

    def test_missing_query(client):
        response = client.get('/api/corpus/search')
        assert response.status_code == 400

    Example 4: Service layer testing

    def test_corpus_service():
        service = CorpusService()
        results = service.search('test', limit=10)
        assert isinstance(results, list)

    Example 5: Blueprint with dependencies

    from flask import Blueprint
    from database import db
    from cache import cache

    bp = Blueprint('api', __name__)

    @bp.route('/items')
    @cache.cached(timeout=300)
    def get_items():
        items = db.query('SELECT * FROM items')
        return jsonify({'items': items})

    Example 6: Custom error responses

    @bp.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({
            'error': 'Validation failed',
            'details': str(error)
        }), 400

    Example 7: Blueprint with before_request

    @bp.before_request
    def before_request():
        # Runs before each request to this blueprint
        logger.info(f"Request to {request.path}")

    @bp.after_request
    def after_request(response):
        # Runs after each request to this blueprint
        response.headers['X-API-Version'] = '1.0'
        return response
    """
    pass
