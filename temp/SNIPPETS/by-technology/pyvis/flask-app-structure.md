# Pyvis Flask App: Standard Structure

**Problem**: Pyvis generates self-contained HTML files that reference `/lib/` directory for vis.js and tom-select dependencies. Files must be web-accessible and properly configured.

**Solution**: Standard directory structure with correct permissions, Caddy routing, and Flask static file serving.

## Directory Structure

```
/myapp/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies (include pyvis)
├── start.sh                    # Service startup script
├── lib/                        # Static JavaScript libraries (CRITICAL)
│   ├── vis-9.1.2/              # vis-network for graph rendering
│   │   ├── vis-network.min.js
│   │   └── vis-network.css
│   ├── tom-select/             # Dropdown library
│   │   ├── tom-select.complete.min.js
│   │   └── tom-select.css
│   └── bindings/               # Pyvis bindings
│       └── utils.js
├── static/                     # Flask static files
│   └── output/                 # Pyvis generated HTML output
│       ├── lib -> ../../lib    # Symlink to lib/ (optional)
│       ├── network_viz.html    # Generated visualizations
│       └── *.html
├── templates/                  # Jinja2 templates
│   ├── base.html
│   └── index.html
├── models/                     # Business logic
│   ├── __init__.py
│   └── graph_builder.py
└── visualization/              # Visualization generators
    ├── __init__.py
    └── network_viz.py
```

## File Permissions

```bash
# Make all files web-readable
chmod 644 lib/**/*.js
chmod 644 lib/**/*.css
chmod 644 static/output/*.html

# Flask app should be executable
chmod 755 app.py
chmod 755 start.sh
```

## Flask Configuration

### app.py

```python
from flask import Flask, render_template, jsonify, request, send_from_directory
from pyvis.network import Network
import os

app = Flask(__name__)

# Configure paths
OUTPUT_DIR = os.path.join(app.static_folder, 'output')
LIB_DIR = os.path.join(os.path.dirname(__file__), 'lib')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    """Main page with visualization controls"""
    return render_template('index.html')

@app.route('/api/visualize', methods=['POST'])
def create_visualization():
    """Generate pyvis network visualization"""
    data = request.get_json()

    # Create pyvis network
    net = Network(
        height='600px',
        width='100%',
        bgcolor='#ffffff',
        font_color='#000000',
        directed=False
    )

    # Add nodes and edges from data
    for node in data.get('nodes', []):
        net.add_node(node['id'], label=node['label'])

    for edge in data.get('edges', []):
        net.add_edge(edge['from'], edge['to'])

    # Configure physics
    net.set_options("""
    {
        "physics": {
            "barnesHut": {
                "gravitationalConstant": -30000,
                "centralGravity": 0.3,
                "springLength": 200
            }
        }
    }
    """)

    # Save to static/output/
    output_file = 'network_viz.html'
    output_path = os.path.join(OUTPUT_DIR, output_file)
    net.save_graph(output_path)

    # Return URL to generated visualization
    return jsonify({
        'status': 'success',
        'url': f'/static/output/{output_file}'
    })

@app.route('/lib/<path:filename>')
def serve_lib(filename):
    """Serve library files (vis.js, tom-select, etc.)"""
    return send_from_directory(LIB_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5013, debug=False)
```

### requirements.txt

```txt
Flask==3.0.0
pyvis==0.3.2
networkx==3.2.1
```

### start.sh

```bash
#!/bin/bash

# Start pyvis Flask app
cd "$(dirname "$0")"

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start Flask app
python3 app.py
```

## Caddy Configuration

```caddyfile
dr.eamer.dev {
    # Pyvis app with iframe support
    handle_path /myapp/* {
        # Remove X-Frame-Options to allow iframe embedding
        header -X-Frame-Options

        reverse_proxy localhost:5013
    }

    # Ensure lib/ files are served correctly
    # Flask handles this via /lib/<path> route
}
```

## Template Example

### templates/base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Pyvis Visualizations{% endblock %}</title>

    <!-- Bootstrap for styling -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

    {% block head %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">
                <i class="bi bi-diagram-3"></i> Network Visualizer
            </a>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### templates/index.html

```html
{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h1>Interactive Network Visualization</h1>
        <button id="generateBtn" class="btn btn-primary" onclick="generateViz()">
            <i class="bi bi-lightning"></i> Generate Network
        </button>

        <div id="vizContainer" class="mt-4" style="display:none;">
            <iframe id="vizFrame"
                    style="width:100%; height:600px; border:1px solid #ddd; border-radius:5px;"
                    src="about:blank">
            </iframe>
        </div>

        <div id="loading" class="mt-3" style="display:none;">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <span class="ms-2">Generating visualization...</span>
        </div>
    </div>
</div>

<script>
function generateViz() {
    const loadingDiv = document.getElementById('loading');
    const vizContainer = document.getElementById('vizContainer');
    const generateBtn = document.getElementById('generateBtn');

    // Show loading indicator
    loadingDiv.style.display = 'block';
    vizContainer.style.display = 'none';
    generateBtn.disabled = true;

    // Sample data
    const data = {
        nodes: [
            { id: 1, label: 'Node 1' },
            { id: 2, label: 'Node 2' },
            { id: 3, label: 'Node 3' },
            { id: 4, label: 'Node 4' }
        ],
        edges: [
            { from: 1, to: 2 },
            { from: 1, to: 3 },
            { from: 2, to: 4 },
            { from: 3, to: 4 }
        ]
    };

    // Call API to generate visualization
    fetch(`${window.location.origin}/myapp/api/visualize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Hide loading, show visualization
        loadingDiv.style.display = 'none';
        vizContainer.style.display = 'block';
        generateBtn.disabled = false;

        // Load generated HTML in iframe
        document.getElementById('vizFrame').src = result.url;
    })
    .catch(error => {
        console.error('Error:', error);
        loadingDiv.style.display = 'none';
        generateBtn.disabled = false;
        alert('Failed to generate visualization');
    });
}
</script>
{% endblock %}
```

## Python Visualization Module

### visualization/network_viz.py

```python
from pyvis.network import Network
import networkx as nx
import os

class NetworkVisualizer:
    """Generate interactive network visualizations with pyvis"""

    def __init__(self, output_dir='static/output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_network(self, nodes, edges, directed=False):
        """
        Create pyvis network from nodes and edges

        Args:
            nodes: List of dicts with 'id' and 'label' keys
            edges: List of dicts with 'from' and 'to' keys
            directed: Boolean for directed/undirected graph

        Returns:
            Network object
        """
        net = Network(
            height='600px',
            width='100%',
            bgcolor='#ffffff',
            font_color='#000000',
            directed=directed
        )

        # Add nodes
        for node in nodes:
            net.add_node(
                node['id'],
                label=node.get('label', str(node['id'])),
                title=node.get('title', ''),  # Tooltip
                color=node.get('color', None),
                size=node.get('size', 25)
            )

        # Add edges
        for edge in edges:
            net.add_edge(
                edge['from'],
                edge['to'],
                weight=edge.get('weight', 1),
                label=edge.get('label', ''),
                color=edge.get('color', None)
            )

        return net

    def set_physics_options(self, net, preset='default'):
        """Configure physics simulation"""
        presets = {
            'default': {
                "physics": {
                    "barnesHut": {
                        "gravitationalConstant": -30000,
                        "centralGravity": 0.3,
                        "springLength": 200,
                        "springConstant": 0.04
                    },
                    "minVelocity": 0.75
                }
            },
            'tight': {
                "physics": {
                    "barnesHut": {
                        "gravitationalConstant": -80000,
                        "centralGravity": 0.5,
                        "springLength": 100
                    }
                }
            },
            'loose': {
                "physics": {
                    "barnesHut": {
                        "gravitationalConstant": -15000,
                        "centralGravity": 0.1,
                        "springLength": 300
                    }
                }
            }
        }

        import json
        net.set_options(json.dumps(presets.get(preset, presets['default'])))

    def save(self, net, filename='network.html'):
        """Save network to HTML file"""
        output_path = os.path.join(self.output_dir, filename)
        net.save_graph(output_path)
        return output_path
```

## Library Files Setup

### Option 1: Copy from pyvis package

```bash
# Find pyvis installation
python3 -c "import pyvis; print(pyvis.__path__[0])"

# Copy lib directory
cp -r /path/to/pyvis/lib /myapp/lib/
```

### Option 2: Download manually

```bash
# Create lib directory structure
mkdir -p lib/vis-9.1.2 lib/tom-select lib/bindings

# Download vis-network
wget https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js -O lib/vis-9.1.2/vis-network.min.js
wget https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.css -O lib/vis-9.1.2/vis-network.css

# Download tom-select
wget https://cdn.jsdelivr.net/npm/tom-select@2.3.1/dist/js/tom-select.complete.min.js -O lib/tom-select/tom-select.complete.min.js
wget https://cdn.jsdelivr.net/npm/tom-select@2.3.1/dist/css/tom-select.css -O lib/tom-select/tom-select.css

# Create minimal utils.js (or copy from pyvis)
echo "// Pyvis bindings utilities" > lib/bindings/utils.js
```

### Option 3: Symlink from system pyvis

```bash
# Find pyvis lib directory
PYVIS_LIB=$(python3 -c "import pyvis, os; print(os.path.join(pyvis.__path__[0], 'lib'))")

# Create symlink
ln -s "$PYVIS_LIB" /myapp/lib
```

## Troubleshooting

### Issue: 404 errors for /lib/*.js files

**Check**:
1. lib/ directory exists and has correct files
2. File permissions are 644 (readable)
3. Flask route `/lib/<path:filename>` is defined
4. Caddy is not blocking static file serving

**Fix**:
```bash
# Set correct permissions
chmod 755 lib/
chmod 644 lib/**/*

# Verify files exist
ls -la lib/vis-9.1.2/
ls -la lib/tom-select/
```

### Issue: Visualizations don't render in iframe

**Check**:
1. X-Frame-Options header removed in Caddy config
2. Generated HTML file exists in static/output/
3. iframe src URL is correct
4. Browser console for JavaScript errors

**Fix Caddy**:
```caddyfile
handle_path /myapp/* {
    header -X-Frame-Options  # CRITICAL for pyvis iframes
    reverse_proxy localhost:5013
}
```

### Issue: Physics simulation not working

**Check**:
1. vis-network.min.js loaded successfully
2. set_options() called with valid JSON
3. Browser console for vis.js errors

**Debug**:
```python
# Print generated HTML to see what vis.js received
net = Network()
# ... add nodes/edges ...
net.save_graph('debug.html')

# Open debug.html and check browser console
```

## Production Checklist

- [ ] lib/ directory with all dependencies
- [ ] File permissions: 644 for static files, 755 for directories
- [ ] Flask /lib/<path> route for serving libraries
- [ ] Caddy config removes X-Frame-Options for iframe support
- [ ] static/output/ directory exists and is writable
- [ ] Error handling for visualization generation failures
- [ ] Loading indicators for async visualization generation
- [ ] Mobile responsive iframe sizing
- [ ] Clear old visualization files periodically (cron job)

## Tags

`pyvis` `flask` `network-visualization` `vis-js` `tom-select` `directory-structure` `static-files` `iframe` `graph-visualization`

## References

- Pyvis documentation: https://pyvis.readthedocs.io/
- vis-network: https://visjs.github.io/vis-network/docs/network/
- tom-select: https://tom-select.js.org/

---

**Source**: Etymology Visualizer session (2025-12-17)
**Production**: dr.eamer.dev/etymology
**Status**: Verified and operational
