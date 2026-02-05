# Flask Input Validation Pattern

**Language**: Python (Flask)
**Pattern**: Request Validation Middleware
**Use Case**: API security, XSS/SQL injection prevention
**Source**: COCA corpus API (2025-12-17)

## Implementation

```python
from flask import Blueprint, request
from werkzeug.exceptions import BadRequest
import re

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.before_request
def validate_input():
    """Validate and sanitize request parameters for security."""
    # Validate query parameter (if present)
    if 'q' in request.args:
        query = request.args.get('q', '')

        if len(query) > 200:
            raise BadRequest("Query too long (max 200 characters)")

        # Block potentially malicious patterns (SQL injection prevention)
        if re.search(r'[;<>]', query):
            raise BadRequest("Invalid characters in query")

    # Validate limit parameter
    if 'limit' in request.args:
        try:
            limit = int(request.args.get('limit'))
            if limit < 1 or limit > 1000:
                raise BadRequest("Limit must be between 1 and 1000")
        except ValueError:
            raise BadRequest("Limit must be a valid integer")

    # Validate offset parameter
    if 'offset' in request.args:
        try:
            offset = int(request.args.get('offset'))
            if offset < 0:
                raise BadRequest("Offset must be non-negative")
        except ValueError:
            raise BadRequest("Offset must be a valid integer")
```

## Key Features

1. **Blueprint-level middleware**: Runs before every request in the blueprint
2. **Length validation**: Prevents resource exhaustion attacks
3. **Character sanitization**: Blocks common injection characters
4. **Range validation**: Ensures numeric parameters are within acceptable bounds
5. **Type validation**: Converts and validates numeric inputs
6. **Descriptive errors**: Returns clear error messages for debugging

## Adaptations

```python
# For JSON body validation
@bp.before_request
def validate_json():
    if request.method in ['POST', 'PUT', 'PATCH']:
        if not request.is_json:
            raise BadRequest("Content-Type must be application/json")

        data = request.get_json()
        required_fields = ['field1', 'field2']

        for field in required_fields:
            if field not in data:
                raise BadRequest(f"Missing required field: {field}")

# For stricter regex validation
SAFE_QUERY_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_]+$')

if not SAFE_QUERY_PATTERN.match(query):
    raise BadRequest("Query contains invalid characters")
```

## Security Considerations

- Adjust character blocklist based on backend (SQL vs NoSQL vs full-text search)
- Consider rate limiting in addition to input validation
- Log validation failures for security monitoring
- Use parameterized queries even with input validation

## Related Patterns

- Rate limiting: Flask-Limiter
- CORS configuration: Flask-CORS
- Response compression: Flask-Compress (Brotli)
