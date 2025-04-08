# app/routers/browse.py
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from ..config import STORAGE_FOLDER
from ..services.file_database_service import list_file_records

router = APIRouter(tags=["browse"])

# Endpoint for listing files using the database records
@router.get("/db")
def get_files_from_db():
    try:
        files = list_file_records()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching files from DB: {e}")

# Optional: You can also keep the root endpoint for DB listing if you prefer
@router.get("/")
def get_files():
    return get_files_from_db()

# Endpoint for listing files directly from the storage folder
@router.get("/folder")
def get_files_from_folder():
    if not os.path.exists(STORAGE_FOLDER):
        return {"files": []}
    files = [
        f for f in os.listdir(STORAGE_FOLDER)
        if os.path.isfile(os.path.join(STORAGE_FOLDER, f))
    ]
    return {"files": files}

# The download endpoint remains unchanged.
@router.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(STORAGE_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
