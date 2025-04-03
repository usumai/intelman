# /app/endpoints/browse_api.py
import os
from flask import Blueprint, jsonify, current_app, send_from_directory
from config import STORAGE_FOLDER

browse_api_bp = Blueprint('browse_api', __name__, url_prefix='/api/browse')

@browse_api_bp.route('/')
def get_files():
    if not os.path.exists(STORAGE_FOLDER):
        files = []
    else:
        files = [f for f in os.listdir(STORAGE_FOLDER)
                 if os.path.isfile(os.path.join(STORAGE_FOLDER, f))]
    return jsonify({'files': files})


@browse_api_bp.route('/download/<path:filename>')
def download_file(filename):
    # Ensure that the file exists and is safe to serve if necessary.
    return send_from_directory(STORAGE_FOLDER, filename, as_attachment=True)
