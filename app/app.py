from flask import Flask, session, request, redirect, url_for
from endpoints import blueprints

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'  # Replace with a strong secret in production

    # Enforce login on every request except for login routes and static files.
    @app.before_request
    def require_login():
        # Allow access to static files and login page without being logged in.
        if request.endpoint is None:
            return  # some endpoints (like favicon) might be None
        if request.endpoint.startswith('static'):
            return
        if request.endpoint.startswith('login'):
            return
        # If the user is not logged in, redirect them to the login page.
        if not session.get('logged_in'):
            return redirect(url_for('login.login'))

    # Register all blueprints from the endpoints package.
    for bp in blueprints:
        app.register_blueprint(bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
