# app/routers/upload.py
import os
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from ..config import STORAGE_FOLDER
from ..services.markitdown_service import convert_file_to_markdown
from ..services.file_database_service import insert_file_record, update_file_record

router = APIRouter(tags=["upload"])

@router.post("/")
async def process_upload(file: UploadFile = File(...)):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        original_filename = file.filename
        _, ext = os.path.splitext(original_filename)

        create_user = "test_user"  # Or get from token/headers in real usage
        status = "uploaded"

        # Insert a new record to get the file_id
        file_id = insert_file_record(create_user, original_filename, status)
        new_filename = f"{file_id}{ext}"
        new_file_path = os.path.join(STORAGE_FOLDER, new_filename)

        # Ensure storage folder exists
        os.makedirs(STORAGE_FOLDER, exist_ok=True)

        # Save the file to disk
        with open(new_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Convert to markdown
        markdown_content = convert_file_to_markdown(new_file_path, enable_plugins=False)

        # Update the DB record
        update_file_record(file_id, new_filename, markdown_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing upload: {e}")

    return {
        "record_id": file_id,
        "allocated_filename": new_filename,
        "markdown": markdown_content
    }
