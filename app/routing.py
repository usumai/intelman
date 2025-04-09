from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Response, Request, Form
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List

from .services import *

router = APIRouter()

async def same_origin_only(request: Request):
    """Block requests unless they come from the same origin as the server itself."""
    server_host = request.url.netloc
    request_host = request.headers.get("host", "")
    if request_host.lower() == server_host.lower():
        return
    else:
        raise HTTPException(status_code=403, detail="Cross-origin requests are not allowed.")


# ---------------------------
# LOGIN ENDPOINT
# ---------------------------
@router.post("/api/login/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == "test_user" and password == "dlpi":
        response = JSONResponse({"access_token": "valid_token", "redirect_url": "/index.html"})
        response.set_cookie(key="access_token", value="valid_token", httponly=True)
        return response
    else:
        return JSONResponse({"detail": "Invalid credentials"}, status_code=400)
    
# ---------------------------
# BROWSE ENDPOINTS
# ---------------------------
@router.get("/api/browse/db", dependencies=[Depends(same_origin_only)])
def get_files():
    return get_files_from_db()

@router.get("/api/browse/folder", dependencies=[Depends(same_origin_only)])
def get_files_folder():
    return list_files_service()

@router.get("/api/browse/download/{filename}", dependencies=[Depends(same_origin_only)])
def download_file(filename: str):
    file_path = download_file_service(filename)
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)

@router.get("/api/file/{file_id}")
def get_file_details(file_id: int):
    """
    Return the file details for a given file_id.
    """
    return get_file_details_service(file_id)

# ---------------------------
# UPLOAD ENDPOINT
# ---------------------------
@router.post("/api/upload/", dependencies=[Depends(same_origin_only)])
async def upload_file(file: UploadFile = File(...)):
    return process_upload_service(file)

# ---------------------------
# LLM ENDPOINT
# ---------------------------
class LLMRequest(BaseModel):
    prompt: Optional[str] = None
    messages: Optional[List[dict]] = None

@router.post("/api/llm/", dependencies=[Depends(same_origin_only)])
def query_llm(data: LLMRequest):
    return query_llm_service(data.prompt, data.messages)

# ---------------------------
# DB EXPLORER ENDPOINTS
# ---------------------------
@router.get("/api/dbexplorer/tables", dependencies=[Depends(same_origin_only)])
def list_tables():
    return list_tables_service()

@router.get("/api/dbexplorer/table/{table_name}", dependencies=[Depends(same_origin_only)])
def get_table_snapshot(table_name: str):
    return get_table_snapshot_service(table_name)