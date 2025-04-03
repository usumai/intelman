# /app/services/file_storage_service.py
import os
import uuid
from werkzeug.utils import secure_filename
from config import STORAGE_FOLDER

def save_file(file):
    """
    Saves the uploaded file to the designated storage folder.
    """
    if not os.path.exists(STORAGE_FOLDER):
        os.makedirs(STORAGE_FOLDER)

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(STORAGE_FOLDER, unique_name)
    file.save(file_path)
    return file_path
