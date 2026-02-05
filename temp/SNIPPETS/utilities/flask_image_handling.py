"""
Flask Image Handling Utilities

Description: Robust image decoding, validation, and response formatting for Flask
vision APIs. Handles both JSON (base64) and multipart form uploads. Eliminates
duplicate image handling code across vision services.

Use Cases:
- Flask APIs accepting image uploads for analysis
- Alt text generation services
- Image classification endpoints
- OCR services with image input
- Any vision API that needs to handle multiple input formats

Dependencies:
- Flask (request, jsonify)
- base64 (standard library)
- Python 3.8+ (uses typing hints)

Notes:
- Automatically handles data URI prefixes (data:image/png;base64,...)
- Validates image size before processing (prevents OOM)
- Standardized success/error responses across all endpoints
- Smart text truncation at sentence boundaries
- Works with both JSON POST and multipart form uploads

Related Snippets:
- /web-frameworks/flask_api_blueprint.py
- /accessibility/altflow_accessible_alt_text.py
- /error-handling/flask_error_responses.py
"""

import base64
from typing import Union, Dict, Any, Tuple
from flask import request, jsonify


def decode_image_from_request() -> Tuple[bytes, Dict[str, Any]]:
    """
    Decode image from either JSON (base64) or multipart/form-data.

    This function handles both common ways clients send images:
    1. JSON with base64-encoded image string
    2. Multipart form data with file upload

    Returns:
        Tuple of (image_bytes, request_data_dict)

    Raises:
        ValueError: If no image is provided or format is invalid

    Example:
        @app.route('/analyze', methods=['POST'])
        def analyze():
            try:
                img_bytes, data = decode_image_from_request()
                provider_name = data.get('provider', 'xai')
                # Process image...
            except ValueError as e:
                return create_error_response(str(e), 400)
    """
    # Handle JSON request with base64-encoded image
    if request.is_json:
        data = request.get_json()

        if 'image' not in data:
            raise ValueError('Missing image data in JSON request')

        # Decode base64
        image_data = data['image']

        # Remove data URI prefix if present (e.g., "data:image/png;base64,...")
        if ',' in image_data:
            image_data = image_data.split(',', 1)[1]

        try:
            img_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise ValueError(f'Invalid base64 image data: {e}')

        return img_bytes, data

    # Handle multipart/form-data (file upload)
    elif 'image' in request.files:
        img_bytes = request.files['image'].read()
        data = request.form.to_dict()
        return img_bytes, data

    else:
        raise ValueError(
            'No image provided. Send either JSON with "image" field '
            'or multipart/form-data with "image" file.'
        )


def create_success_response(data: Dict[str, Any], status_code: int = 200):
    """
    Create a standardized success response.

    Args:
        data: Dictionary of response data to include
        status_code: HTTP status code (default: 200)

    Returns:
        Flask response tuple (json, status_code)

    Example:
        return create_success_response({
            'alt_text': 'A beautiful sunset',
            'provider': 'xai',
            'tokens_used': 150
        })

        # Response:
        # {
        #     "success": true,
        #     "alt_text": "A beautiful sunset",
        #     "provider": "xai",
        #     "tokens_used": 150
        # }
    """
    return jsonify({
        'success': True,
        **data
    }), status_code


def create_error_response(error: Union[str, Exception], status_code: int = 500):
    """
    Create a standardized error response.

    Args:
        error: Error message or exception
        status_code: HTTP status code (default: 500)

    Returns:
        Flask response tuple (json, status_code)

    Example:
        return create_error_response('Image too large', 400)
        return create_error_response(ValueError('Invalid format'), 400)

        # Response:
        # {
        #     "success": false,
        #     "error": "Image too large"
        # }
    """
    return jsonify({
        'success': False,
        'error': str(error)
    }), status_code


def truncate_text(text: str, max_length: int, prefer_sentence: bool = True) -> str:
    """
    Truncate text to maximum length, preferring sentence boundaries.

    Args:
        text: Text to truncate
        max_length: Maximum length in characters
        prefer_sentence: Try to truncate at sentence boundary if True

    Returns:
        Truncated text

    Example:
        # Sentence boundary truncation
        long_text = "First sentence. Second sentence. Third sentence."
        result = truncate_text(long_text, 30, prefer_sentence=True)
        # Result: "First sentence."

        # Hard truncation
        result = truncate_text(long_text, 30, prefer_sentence=False)
        # Result: "First sentence. Second se..."
    """
    if len(text) <= max_length:
        return text

    if prefer_sentence and '. ' in text[:max_length]:
        # Truncate at last sentence boundary before max_length
        truncated = text[:text[:max_length].rfind('. ') + 1]
        return truncated
    else:
        # Hard truncate with ellipsis
        return text[:max_length - 3] + '...'


def validate_image_size(img_bytes: bytes, max_size_mb: int = 10) -> None:
    """
    Validate image size doesn't exceed limit.

    Args:
        img_bytes: Raw image bytes
        max_size_mb: Maximum size in megabytes

    Raises:
        ValueError: If image exceeds size limit

    Example:
        try:
            img_bytes, data = decode_image_from_request()
            validate_image_size(img_bytes, max_size_mb=5)
            # Process image...
        except ValueError as e:
            return create_error_response(str(e), 413)
    """
    size_mb = len(img_bytes) / (1024 * 1024)
    if size_mb > max_size_mb:
        raise ValueError(f'Image too large: {size_mb:.1f}MB (max: {max_size_mb}MB)')


def prepare_image_for_api(
    img_bytes: bytes,
    format: str = 'data_uri'
) -> str:
    """
    Prepare image bytes for API consumption.

    Args:
        img_bytes: Raw image bytes
        format: Output format ('data_uri', 'base64', 'url')

    Returns:
        Formatted image string

    Example:
        img_bytes, _ = decode_image_from_request()
        data_uri = prepare_image_for_api(img_bytes, format='data_uri')
        # Result: "data:image/png;base64,iVBORw0KG..."

        base64_str = prepare_image_for_api(img_bytes, format='base64')
        # Result: "iVBORw0KG..."
    """
    encoded = base64.b64encode(img_bytes).decode('utf-8')

    if format == 'data_uri':
        return f"data:image/png;base64,{encoded}"
    elif format == 'base64':
        return encoded
    elif format == 'url':
        # For APIs that expect URL format
        return f"data:image/png;base64,{encoded}"
    else:
        raise ValueError(f"Unknown format: {format}")


# Complete Flask route example
def example_vision_route():
    """
    Example: Complete vision analysis Flask route.

    This demonstrates all utilities working together.
    """
    from flask import Flask, request

    app = Flask(__name__)

    @app.route('/analyze', methods=['POST'])
    def analyze_image():
        """Analyze image and return description."""
        try:
            # Decode image
            img_bytes, data = decode_image_from_request()

            # Validate size
            validate_image_size(img_bytes, max_size_mb=5)

            # Get parameters
            provider_name = data.get('provider', 'xai')
            max_length = int(data.get('max_length', 500))

            # Prepare for API
            image_data = prepare_image_for_api(img_bytes)

            # Call vision API (pseudo-code)
            # provider = ProviderFactory.get_provider(provider_name)
            # result = provider.analyze_image(image_data, "Describe this image")
            # description = result['content']

            # Simulate result
            description = "A beautiful sunset over mountains. The sky is painted with vibrant oranges and pinks."

            # Truncate if needed
            if len(description) > max_length:
                description = truncate_text(description, max_length)

            # Return success
            return create_success_response({
                'description': description,
                'length': len(description),
                'provider': provider_name
            })

        except ValueError as e:
            return create_error_response(str(e), 400)
        except Exception as e:
            return create_error_response(f'Internal error: {str(e)}', 500)

    return app


if __name__ == "__main__":
    # Test utilities
    import io

    # Create test image data
    test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR...'  # Truncated PNG header

    # Test encoding
    encoded = base64.b64encode(test_image).decode()
    print("Base64 encoded:", encoded[:50] + "...")

    # Test data URI
    data_uri = prepare_image_for_api(test_image, 'data_uri')
    print("Data URI:", data_uri[:50] + "...")

    # Test truncation
    long_text = "First sentence. Second sentence. Third sentence. Fourth sentence."
    truncated = truncate_text(long_text, 30, prefer_sentence=True)
    print(f"Original: {long_text}")
    print(f"Truncated: {truncated}")

    # Test size validation
    try:
        validate_image_size(b'x' * (11 * 1024 * 1024), max_size_mb=10)
    except ValueError as e:
        print(f"Size validation error: {e}")
