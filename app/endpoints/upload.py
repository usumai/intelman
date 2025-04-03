# /app/endpoints/upload.py
import os
from flask import Blueprint, request, jsonify, current_app
from config import STORAGE_FOLDER
from services.markitdown_service import convert_file_to_markdown
from services.file_database_service import insert_file_record, update_file_record

upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')

@upload_bp.route('/', methods=['POST'])
def process_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Extract original filename and file extension.
        original_filename = file.filename
        _, ext = os.path.splitext(original_filename)
        
        # Set additional metadata; for instance, you might use session data instead of "test_user".
        create_user = "test_user"
        status = "uploaded"

        # Insert a new record into the database to get the file_id.
        file_id = insert_file_record(create_user, original_filename, status)

        # Construct the new filename as "<file_id><extension>"
        new_filename = f"{file_id}{ext}"
        new_file_path = os.path.join(STORAGE_FOLDER, new_filename)

        # Save the uploaded file under the new filename.
        file.save(new_file_path)

        # Process the file with MarkItDown to generate markdown content.
        markdown_content = convert_file_to_markdown(new_file_path, enable_plugins=False)
        current_app.logger.info(f"Conversion result: {markdown_content}")

        # Update the record with the allocated filename and additional metadata.
        update_file_record(file_id, new_filename, markdown_content)

    except Exception as e:
        current_app.logger.error(f"Error processing upload: {e}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

    return jsonify({
        'record_id': file_id,
        'allocated_filename': new_filename,
        'markdown': markdown_content
    })
