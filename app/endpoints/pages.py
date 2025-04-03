from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

pages_bp = Blueprint('pages', __name__)

# You can add any specific routes here if needed.
# For example, if you want a dedicated route for the home page:
@pages_bp.route('/')
def home():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

# Catch-all route: attempts to serve a template based on the URL.
@pages_bp.route('/<path:page>')
def serve_page(page):
    # If the requested path doesn't end with '.html', append it.
    if not page.endswith('.html'):
        page = f"{page}.html"
    try:
        return render_template(page)
    except TemplateNotFound:
        abort(404)
