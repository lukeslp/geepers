"""
Flask Multi-Provider API Proxy Pattern

Description: Production-ready Flask proxy server for multiple AI/LLM providers with comprehensive
error handling, rate limiting, CORS configuration, and provider abstraction. Supports multiple
providers (OpenAI, Anthropic, xAI, etc.) with unified request/response interface.

Use Cases:
- Building AI proxy services to centralize API key management
- Creating unified interfaces across multiple LLM providers
- Implementing rate limiting and request tracking
- Proxying external APIs with CORS handling for frontend applications
- Supporting provider failover and load balancing

Dependencies:
- flask
- flask-cors
- requests
- python-dotenv
- logging

Notes:
- Provider configuration uses dictionary pattern for extensibility
- Rate limiting uses in-memory list (consider Redis for production)
- API keys loaded from environment variables with fallback support
- CORS configured for specific origins with credentials support
- Request timeouts prevent hung connections (60s default)
- Comprehensive error handling with proper HTTP status codes

Related Snippets:
- error-handling/graceful_import_fallbacks.py - Optional dependency handling
- configuration-management/multi_source_config.py - Advanced configuration
- streaming-patterns/sse_streaming_responses.py - Streaming AI responses

Source Attribution:
- Extracted from: /home/coolhand/html/storyblocks/api_proxy.py
- Related patterns: /home/coolhand/servers/viewer/alt_text_server.py
- Production deployment: https://dr.eamer.dev/storyblocks
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, Tuple, Optional, Any
import uuid

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# ============================================================================
# CORS Configuration
# ============================================================================
# Enhanced CORS for cross-origin requests
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://dr.eamer.dev",
            "https://*.dr.eamer.dev",
            "https://d.reamwalker.com",
            "https://*.reamwalker.com",
            "http://localhost:*",
            "http://127.0.0.1:*",
            "file://*"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True,
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "max_age": 3600
    }
}, supports_credentials=True)


@app.after_request
def after_request(response):
    """
    Handle CORS headers for all responses.
    Provides explicit origin validation for enhanced security.
    """
    origin = request.headers.get('Origin')
    allowed_origins = [
        'https://dr.eamer.dev',
        'https://d.reamwalker.com',
        'https://reamwalker.com',
        'http://localhost',
        'http://127.0.0.1'
    ]

    if origin and any(origin.startswith(allowed) for allowed in allowed_origins):
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Max-Age', '3600')

    return response


# ============================================================================
# Provider Configuration
# ============================================================================
# Multi-provider configuration with environment variable support
PROVIDERS = {
    'xai': {
        'base_url': os.getenv('XAI_API_BASE', 'https://api.x.ai/v1'),
        'api_key': os.getenv('XAI_API_KEY', ''),
        'models': {
            'text': 'grok-3',
            'image': 'grok-2-image-1212',
            'video': 'grok-2-image-1212'
        }
    },
    'openai': {
        'base_url': os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1'),
        'api_key': os.getenv('OPENAI_API_KEY', ''),
        'models': {
            'text': 'gpt-4o',
            'image': 'dall-e-3',
            'video': 'dall-e-3'
        }
    },
    'anthropic': {
        'base_url': 'https://api.anthropic.com/v1',
        'api_key': os.getenv('ANTHROPIC_API_KEY', ''),
        'models': {
            'text': 'claude-3-5-sonnet-20241022',
            'image': 'claude-3-5-sonnet-20241022',
            'video': 'claude-3-5-sonnet-20241022'
        }
    }
}

DEFAULT_PROVIDER = 'xai'


# ============================================================================
# Rate Limiting
# ============================================================================
# Simple in-memory rate limiting
request_history = []
MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', 20))


def check_rate_limit() -> bool:
    """
    Basic rate limiting implementation.

    Returns:
        bool: True if request is allowed, False if rate limit exceeded

    Note: For production, use Redis-based rate limiting for distributed systems
    """
    current_time = time.time()
    global request_history

    # Remove requests older than 1 minute
    request_history = [req_time for req_time in request_history if current_time - req_time < 60]

    if len(request_history) >= MAX_REQUESTS_PER_MINUTE:
        return False

    request_history.append(current_time)
    return True


# ============================================================================
# API Request Handler
# ============================================================================
def make_llm_request(
    endpoint: str,
    method: str = "POST",
    data: Optional[Dict[str, Any]] = None,
    stream: bool = False,
    provider: Optional[str] = None
) -> Tuple[Optional[requests.Response], int, Optional[str]]:
    """
    Make a request to LLM API with proper error handling.

    Args:
        endpoint: API endpoint path (e.g., 'chat/completions')
        method: HTTP method (POST or GET)
        data: Request payload
        stream: Whether to stream the response
        provider: Provider name (defaults to DEFAULT_PROVIDER)

    Returns:
        Tuple of (response, status_code, error_message)
        - response: requests.Response object or None on failure
        - status_code: HTTP status code
        - error_message: Error description or None on success
    """
    if provider is None:
        provider = DEFAULT_PROVIDER

    if provider not in PROVIDERS:
        return None, 400, f"Unknown provider: {provider}"

    provider_config = PROVIDERS[provider]
    url = f"{provider_config['base_url']}/{endpoint}"

    headers = {
        "Authorization": f"Bearer {provider_config['api_key']}",
        "Content-Type": "application/json"
    }

    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=data, stream=stream, timeout=60)
        else:
            response = requests.get(url, headers=headers, stream=stream, timeout=60)

        logger.info(f"{provider} API call: {endpoint} - Status: {response.status_code}")

        if not response.ok:
            logger.error(f"{provider} API error: {response.status_code} - {response.text}")
            return None, response.status_code, response.text

        return response, 200, None

    except requests.exceptions.Timeout:
        logger.error(f"{provider} API request timed out")
        return None, 408, "Request timed out"
    except requests.exceptions.RequestException as e:
        logger.error(f"{provider} API request failed: {str(e)}")
        return None, 500, str(e)


# ============================================================================
# Core Endpoints
# ============================================================================
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Multi-Provider API Proxy"
    })


@app.route('/api/providers', methods=['GET'])
def list_providers():
    """Get available LLM providers and their configurations."""
    try:
        provider_info = {}
        for name, config in PROVIDERS.items():
            provider_info[name] = {
                'name': name,
                'models': config['models'],
                'available': bool(config['api_key'])
            }

        return jsonify({
            'providers': provider_info,
            'default': DEFAULT_PROVIDER
        })

    except Exception as e:
        logger.error(f"Provider list error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/test', methods=['GET'])
def test_connection():
    """Test LLM API connections for all providers."""
    provider = request.args.get('provider', DEFAULT_PROVIDER)

    try:
        if provider not in PROVIDERS:
            return jsonify({
                "success": False,
                "error": f"Unknown provider: {provider}"
            }), 400

        # Test with a simple chat completion
        test_data = {
            "model": PROVIDERS[provider]['models']['text'],
            "messages": [
                {"role": "user", "content": "Hello, this is a connection test. Please respond with 'Connection successful'."}
            ],
            "max_tokens": 20
        }

        response, status_code, error = make_llm_request("chat/completions", "POST", test_data, provider=provider)

        if response is None:
            return jsonify({
                "success": False,
                "error": error,
                "status_code": status_code,
                "provider": provider
            }), status_code

        result = response.json()

        return jsonify({
            "success": True,
            "message": f"{provider} API connection successful",
            "test_response": result.get('choices', [{}])[0].get('message', {}).get('content', 'No response'),
            "model": result.get('model'),
            "provider": provider,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Connection test error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/chat/completions', methods=['POST'])
def chat_completions():
    """
    Proxy for LLM chat completions API (supports multiple providers).

    Request body should include:
    - messages: Array of message objects
    - model: (optional) Model to use (defaults to provider's text model)
    - provider: (optional) Provider name (defaults to DEFAULT_PROVIDER)
    """
    if not check_rate_limit():
        return jsonify({"error": "Rate limit exceeded"}), 429

    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'messages' not in data:
            return jsonify({"error": "Missing required field: messages"}), 400

        # Extract provider from request
        provider = data.pop('provider', DEFAULT_PROVIDER)

        # Validate and set model for provider
        if 'model' not in data and provider in PROVIDERS:
            data['model'] = PROVIDERS[provider]['models']['text']

        # Add request ID for tracking
        request_id = str(uuid.uuid4())
        logger.info(f"Chat completion request {request_id}: {data.get('model', 'default')}")

        # Make request to selected provider
        response, status_code, error = make_llm_request("chat/completions", "POST", data, provider=provider)

        if response is None:
            return jsonify({"error": error or f"{provider} API request failed"}), status_code

        # Return the response
        result = response.json()
        result['request_id'] = request_id

        logger.info(f"Chat completion {request_id} completed successfully")
        return jsonify(result)

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in request body"}), 400
    except Exception as e:
        logger.error(f"Chat completion error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/images/generations', methods=['POST'])
def image_generation():
    """
    Proxy for LLM image generation API (supports multiple providers).

    Request body should include:
    - prompt: Image generation prompt
    - model: (optional) Model to use
    - provider: (optional) Provider name
    - n: (optional) Number of images (default: 1)
    """
    if not check_rate_limit():
        return jsonify({"error": "Rate limit exceeded"}), 429

    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing required field: prompt"}), 400

        # Extract provider from request
        provider = data.pop('provider', DEFAULT_PROVIDER)

        # Set defaults based on provider
        if 'model' not in data and provider in PROVIDERS:
            data['model'] = PROVIDERS[provider]['models']['image']
        if 'n' not in data:
            data['n'] = 1

        request_id = str(uuid.uuid4())
        logger.info(f"Image generation request {request_id}: {data['prompt'][:50]}...")

        # Make request to selected provider
        response, status_code, error = make_llm_request("images/generations", "POST", data, provider=provider)

        if response is None:
            return jsonify({"error": error or f"{provider} API request failed"}), status_code

        result = response.json()
        result['request_id'] = request_id

        logger.info(f"Image generation {request_id} completed successfully")
        return jsonify(result)

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON in request body"}), 400
    except Exception as e:
        logger.error(f"Image generation error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# Error Handlers
# ============================================================================
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# Application Entry Point
# ============================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting Multi-Provider API Proxy on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Available providers: {', '.join(PROVIDERS.keys())}")

    # Log API key status (without revealing keys)
    for provider, config in PROVIDERS.items():
        if config['api_key']:
            logger.info(f"{provider} API key configured")
        else:
            logger.warning(f"{provider} API key not configured")

    app.run(host='0.0.0.0', port=port, debug=debug)


# ============================================================================
# Usage Examples
# ============================================================================
if __name__ == "__main__" and False:  # Set to True to run examples
    """
    Example 1: Basic chat completion

    curl -X POST http://localhost:8000/api/chat/completions \
      -H "Content-Type: application/json" \
      -d '{
        "messages": [
          {"role": "user", "content": "Hello!"}
        ],
        "provider": "xai"
      }'

    Example 2: Image generation

    curl -X POST http://localhost:8000/api/images/generations \
      -H "Content-Type: application/json" \
      -d '{
        "prompt": "A serene mountain landscape",
        "provider": "openai",
        "n": 1
      }'

    Example 3: Test connection

    curl http://localhost:8000/api/test?provider=anthropic

    Example 4: List providers

    curl http://localhost:8000/api/providers

    Example 5: Health check

    curl http://localhost:8000/health

    Example 6: Python client

    import requests

    # Chat completion
    response = requests.post('http://localhost:8000/api/chat/completions', json={
        'messages': [
            {'role': 'user', 'content': 'What is Flask?'}
        ],
        'provider': 'xai',
        'max_tokens': 100
    })
    print(response.json())

    # Test all providers
    providers_response = requests.get('http://localhost:8000/api/providers')
    providers = providers_response.json()['providers']

    for provider_name in providers:
        test_response = requests.get(f'http://localhost:8000/api/test?provider={provider_name}')
        print(f"{provider_name}: {test_response.json()}")
    """
    pass
