# Caddy: Remove Security Headers for iframe Support

**Problem**: Need to embed third-party or self-generated HTML in iframes, but security headers like `X-Frame-Options` and `Content-Security-Policy` block the embedding.

**Use Case**: Pyvis network visualizations, embedded reports, third-party widgets, self-contained HTML exports.

## Solution: Selective Header Removal

### 1. Remove X-Frame-Options for Specific Route

```caddyfile
# Allow iframe embedding for specific path
handle_path /myapp/* {
    header -X-Frame-Options  # Minus sign removes the header
    reverse_proxy localhost:5000
}
```

### 2. Remove Multiple Headers

```caddyfile
handle_path /embed/* {
    header {
        -X-Frame-Options
        -Content-Security-Policy
    }
    reverse_proxy localhost:5000
}
```

### 3. Replace Header Instead of Removing

```caddyfile
# Allow embedding only from same origin
handle_path /widgets/* {
    header X-Frame-Options "SAMEORIGIN"
    reverse_proxy localhost:5000
}
```

### 4. Conditional Header Removal

```caddyfile
# Only remove header for iframe-friendly endpoints
handle /api/export/* {
    header -X-Frame-Options
    reverse_proxy localhost:5000
}

# Keep security headers for everything else
handle /* {
    header {
        X-Frame-Options "DENY"
        X-Content-Type-Options "nosniff"
        X-XSS-Protection "1; mode=block"
    }
    reverse_proxy localhost:5000
}
```

## Complete Example: Pyvis Visualizations

### Caddy Configuration

```caddyfile
dr.eamer.dev {
    # Global security headers (applied to all routes by default)
    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"  # Prevent clickjacking
        X-XSS-Protection "1; mode=block"
        Referrer-Policy "strict-origin-when-cross-origin"
    }

    # Etymology app with iframe support for pyvis
    handle_path /etymology/* {
        # Remove X-Frame-Options to allow pyvis iframe embedding
        header -X-Frame-Options

        # Keep other security headers
        # (they're already set globally above)

        reverse_proxy localhost:5013
    }

    # Other routes maintain strict security
    handle_path /api/* {
        # X-Frame-Options "DENY" still active here
        reverse_proxy localhost:5000
    }
}
```

### Flask App Structure

```python
# app.py
from flask import Flask, render_template
from pyvis.network import Network

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/visualize', methods=['POST'])
def visualize():
    # Generate pyvis network
    net = Network(height='600px', width='100%')
    net.add_node(1, label='Node 1')
    net.add_node(2, label='Node 2')
    net.add_edge(1, 2)

    # Save to static/output/
    net.save_graph('static/output/network.html')

    return {'url': '/static/output/network.html'}
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Network Visualization</title>
</head>
<body>
    <h1>Interactive Network</h1>
    <button onclick="generateNetwork()">Generate</button>

    <iframe id="vizFrame"
            style="width:100%; height:600px; border:1px solid #ccc;"
            src="about:blank">
    </iframe>

    <script>
    function generateNetwork() {
        fetch('/api/visualize', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                // Load pyvis HTML in iframe
                document.getElementById('vizFrame').src = data.url;
            });
    }
    </script>
</body>
</html>
```

## Security Considerations

### When to Remove Headers

**SAFE to remove X-Frame-Options**:
- Self-contained visualizations (pyvis, plotly, D3 exports)
- Internal tools with authentication
- Public widgets designed for embedding
- Content you fully control

**UNSAFE to remove X-Frame-Options**:
- User authentication pages (login, password reset)
- Payment processing pages
- Admin dashboards
- Any page with sensitive user actions

### Alternative: CSP frame-ancestors

Instead of removing `X-Frame-Options`, use `Content-Security-Policy` with `frame-ancestors`:

```caddyfile
handle_path /widgets/* {
    header {
        -X-Frame-Options  # Remove legacy header
        Content-Security-Policy "frame-ancestors 'self' https://trusted-site.com"
    }
    reverse_proxy localhost:5000
}
```

**Benefits**:
- More granular control (specify allowed parent domains)
- Modern standard (X-Frame-Options is legacy)
- Better security (whitelist instead of blacklist)

## Debugging iframe Blocking

### 1. Check Browser Console

Blocked by `X-Frame-Options`:
```
Refused to display 'https://example.com/page' in a frame because it set
'X-Frame-Options' to 'DENY'.
```

Blocked by CSP:
```
Refused to frame 'https://example.com/page' because an ancestor violates
the following Content Security Policy directive: "frame-ancestors 'none'".
```

### 2. Check Response Headers

```bash
# Check what headers are being sent
curl -I https://example.com/etymology/

# Look for:
HTTP/2 200
x-frame-options: DENY  # ← This blocks iframes
```

### 3. Verify Caddy Config

```bash
# Validate Caddyfile syntax
sudo caddy validate --config /etc/caddy/Caddyfile

# Reload after changes
sudo systemctl reload caddy
```

### 4. Test with Simple HTML

```html
<!-- test-iframe.html -->
<!DOCTYPE html>
<html>
<body>
    <h1>iframe Test</h1>
    <iframe src="https://example.com/etymology/"
            width="800" height="600">
    </iframe>
</body>
</html>
```

Open in browser and check console for errors.

## Common Patterns

### Pattern 1: Visualization Endpoints Only

```caddyfile
# Remove headers only for /viz/* endpoints
handle /app/viz/* {
    header -X-Frame-Options
    reverse_proxy localhost:5000
}

# Keep strict security for app pages
handle /app/* {
    # X-Frame-Options "DENY" from global config
    reverse_proxy localhost:5000
}
```

### Pattern 2: Static Exports Directory

```caddyfile
# Allow embedding of generated exports
handle_path /exports/* {
    header -X-Frame-Options
    root * /var/www/exports
    file_server
}
```

### Pattern 3: Trusted Domains Whitelist

```caddyfile
handle_path /embed/* {
    header {
        -X-Frame-Options
        Content-Security-Policy "frame-ancestors 'self' https://partner1.com https://partner2.com"
    }
    reverse_proxy localhost:5000
}
```

## Related Patterns

- **Flask + Caddy absolute URLs**: Use with path stripping
- **Pyvis Flask app structure**: Directory layout for network visualizations
- **CSP headers**: Modern alternative to X-Frame-Options

## Tags

`caddy` `security-headers` `x-frame-options` `iframe` `csp` `content-security-policy` `pyvis` `embedding` `clickjacking` `frame-ancestors`

## References

- MDN X-Frame-Options: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
- MDN CSP frame-ancestors: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors
- Caddy header directive: https://caddyserver.com/docs/caddyfile/directives/header

---

**Source**: Etymology Visualizer session (2025-12-17)
**Issue**: Pyvis visualizations blocked by X-Frame-Options header
**Solution**: Selective header removal for /etymology/* routes
**Status**: Production-verified at dr.eamer.dev/etymology
