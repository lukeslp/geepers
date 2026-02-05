"""
Flask Blueprint with URL Prefix Pattern

Description: Proper Flask Blueprint configuration for hosting applications under
a sub-path (e.g., /io/studio, /api/v1). Handles session cookies, static files,
and URL generation correctly.

Use Cases:
- Multi-service monorepo with shared domain (dr.eamer.dev/service1, /service2)
- API versioning (/api/v1, /api/v2)
- Reverse proxy sub-path routing
- Microservices behind a gateway

Dependencies:
- flask

Notes:
- SESSION_COOKIE_PATH must match url_prefix for proper cookie scoping
- url_for('blueprint.route') automatically includes prefix
- Static files need static_url_path to avoid conflicts
- Blueprint name becomes namespace for routes

Related Snippets:
- caddy_reverse_proxy_handle_path.conf
- flask_authentication_session.py
"""

from flask import Flask, Blueprint, url_for, session, render_template, jsonify

# Configuration
BASE_PATH = "/io/studio"  # Adjust to your sub-path

# Create Blueprint with URL prefix
app_bp = Blueprint(
    'studio',                    # Blueprint name (used in url_for)
    __name__,
    url_prefix=BASE_PATH,        # All routes get this prefix
    static_folder='static',      # Static files location
    static_url_path='/static',   # URL path for static files
    template_folder='templates'  # Templates location
)


# Routes automatically get the prefix
@app_bp.route("/")
def index():
    """Route accessible at: /io/studio/"""
    # Use url_for with blueprint name
    api_url = url_for('studio.api_endpoint')  # Generates: /io/studio/api
    logout_url = url_for('studio.logout')     # Generates: /io/studio/logout

    return render_template(
        'index.html',
        api_url=api_url,
        logout_url=logout_url
    )


@app_bp.route("/api", methods=["POST"])
def api_endpoint():
    """Route accessible at: /io/studio/api"""
    # Session works correctly because cookie path is scoped
    user = session.get('user')
    return jsonify({"status": "ok", "user": user})


@app_bp.route("/logout")
def logout():
    """Route accessible at: /io/studio/logout"""
    session.pop('user', None)
    return jsonify({"status": "logged_out"})


# Application setup
def create_app():
    app = Flask(__name__)
    app.secret_key = "your-secret-key"

    # CRITICAL: Set session cookie path to match blueprint prefix
    # Without this, cookies won't work correctly on sub-paths
    app.config['SESSION_COOKIE_PATH'] = BASE_PATH

    # Optional: Additional session security
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Register the blueprint
    app.register_blueprint(app_bp)

    return app


# Usage example
if __name__ == "__main__":
    app = create_app()

    # Verify routes are registered correctly
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")

    # Example output:
    # /io/studio/ -> studio.index
    # /io/studio/api -> studio.api_endpoint
    # /io/studio/logout -> studio.logout
    # /io/studio/static/<path:filename> -> studio.static

    app.run(host="0.0.0.0", port=5000, debug=True)
