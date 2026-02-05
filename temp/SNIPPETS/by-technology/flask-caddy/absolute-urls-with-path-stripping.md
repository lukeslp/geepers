# Flask + Caddy: Absolute URLs with Path Stripping

**Problem**: When Caddy uses `handle_path` to strip route prefixes, Flask receives different paths than the browser sees, causing relative fetch() URLs to fail.

**Scenario**:
- Caddy config: `handle_path /myapp/*` strips `/myapp` prefix
- Browser URL: `https://example.com/myapp/page`
- Flask receives: `/page`
- Relative fetch to `/api/data` becomes: `https://example.com/api/data` (WRONG)
- Should be: `https://example.com/myapp/api/data` (CORRECT)

## Solution Patterns

### 1. JavaScript: Construct from window.location.origin

```javascript
// Get the base path from current URL
const basePath = window.location.pathname.split('/').slice(0, 2).join('/'); // "/myapp"

// Construct absolute URL
fetch(`${window.location.origin}${basePath}/api/analyze`, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### 2. Flask Template: Use url_for with _external=True

```html
<!-- In Jinja2 template -->
<script>
function analyzeWord() {
    const word = document.getElementById('wordInput').value;

    fetch("{{ url_for('api.analyze', _external=True) }}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ word: word })
    })
    .then(response => response.json())
    .then(data => displayResults(data))
    .catch(error => console.error('Error:', error));
}
</script>
```

### 3. Flask: Define base URL in template context

```python
# In Flask app.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.context_processor
def inject_base_url():
    """Make base URL available in all templates"""
    return {
        'base_url': request.url_root.rstrip('/') + '/myapp',
        'api_base': request.url_root.rstrip('/') + '/myapp/api'
    }

@app.route('/')
def index():
    return render_template('index.html')
```

```html
<!-- In template -->
<script>
const API_BASE = "{{ api_base }}";

function callAPI(endpoint, data) {
    return fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
}

// Usage
callAPI('/analyze', { word: 'biology' })
    .then(response => response.json())
    .then(data => console.log(data));
</script>
```

### 4. Flask Blueprint: Register with url_prefix

```python
# In Flask app with blueprint
from flask import Flask, Blueprint

app = Flask(__name__)

# Create blueprint with url_prefix matching Caddy route
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    # This route will be at /api/analyze
    # When Caddy strips /myapp, Flask still sees /api/analyze
    data = request.get_json()
    return jsonify({'result': 'success'})

app.register_blueprint(api_bp)
```

```caddyfile
# Caddy config
handle_path /myapp/* {
    reverse_proxy localhost:5000
}
```

## Comparison: WRONG vs RIGHT

### WRONG: Relative URL
```javascript
// Browser is at: https://example.com/myapp/page
fetch('/api/data', { method: 'POST' })
// Requests: https://example.com/api/data ❌
// Flask never receives this (not under /myapp route)
```

### RIGHT: Absolute URL
```javascript
// Browser is at: https://example.com/myapp/page
fetch(`${window.location.origin}/myapp/api/data`, { method: 'POST' })
// Requests: https://example.com/myapp/api/data ✓
// Caddy strips /myapp, Flask receives /api/data ✓
```

## Debugging Checklist

When fetch() fails with Flask + Caddy path stripping:

1. **Check browser Network tab**: See actual URL being requested
2. **Check Flask logs**: See what path Flask receives after Caddy strips prefix
3. **Verify Caddy config**: Confirm using `handle_path` (strips) vs `handle` (keeps)
4. **Test absolute URL**: Construct full URL from `window.location.origin`
5. **Check Flask routes**: Ensure registered routes match what Flask receives after stripping

## Example: Etymology Visualizer Fix

### Before (BROKEN)
```html
<!-- templates/index.html -->
<script>
function analyzeWord() {
    const word = document.getElementById('wordInput').value;

    fetch('/api/analyze', {  // ❌ Relative URL
        method: 'POST',
        body: JSON.stringify({ word: word })
    })
    .then(response => response.json())
    .then(data => displayResults(data));
}
</script>
```

**Error in browser console**:
```
POST https://dr.eamer.dev/api/analyze 404 (Not Found)
```

### After (FIXED)
```html
<!-- templates/index.html -->
<script>
function analyzeWord() {
    const word = document.getElementById('wordInput').value;

    fetch(`${window.location.origin}/etymology/api/analyze`, {  // ✓ Absolute URL
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ word: word })
    })
    .then(response => response.json())
    .then(data => displayResults(data));
}
</script>
```

**Success**:
```
POST https://dr.eamer.dev/etymology/api/analyze 200 OK
```

## Related Patterns

- **Caddy handle vs handle_path**: Know when to strip paths and when to keep them
- **Flask url_for with blueprints**: Generate URLs correctly in multi-blueprint apps
- **API base URL configuration**: Store base URLs in environment variables for different environments

## Tags

`flask` `caddy` `routing` `path-stripping` `fetch` `javascript` `url-construction` `absolute-urls` `reverse-proxy`

## References

- Caddy documentation: https://caddyserver.com/docs/caddyfile/directives/handle_path
- Flask url_for: https://flask.palletsprojects.com/en/3.0.x/api/#flask.url_for
- MDN fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

---

**Source**: Etymology Visualizer session (2025-12-17)
**Tested**: dr.eamer.dev/etymology
**Status**: Production-verified
