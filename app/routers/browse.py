# app/routers/browse.py
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from ..config import STORAGE_FOLDER

router = APIRouter(tags=["browse"])

@router.get("/")
def get_files():
    if not os.path.exists(STORAGE_FOLDER):
        return JSONResponse(content={"files": []})
    files = [
        f for f in os.listdir(STORAGE_FOLDER)
        if os.path.isfile(os.path.join(STORAGE_FOLDER, f))
    ]
    return {"files": files}

@router.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(STORAGE_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
