from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import jwt
from .config import SECRET_KEY, ALGORITHM

app = FastAPI(title="My FastAPI App")

# Middleware to enforce auth for API endpoints (except login)
@app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    # Only protect API endpoints except those related to login.
    if request.url.path.startswith("/api/") and not request.url.path.startswith("/api/login"):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return JSONResponse(status_code=401, content={"detail": "Invalid authentication header"})
        token = parts[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
    return await call_next(request)

# Include your API routers.
from .routers.browse import router as browse_router
from .routers.upload import router as upload_router
from .routers.llm import router as llm_router
from .routers.dbexplorer import router as dbexplorer_router
from .routers.login import router as login_router
from .routers.file import router as file_router 

app.include_router(browse_router, prefix="/api/browse")
app.include_router(upload_router, prefix="/api/upload")
app.include_router(llm_router, prefix="/api/llm")
app.include_router(dbexplorer_router, prefix="/api/dbexplorer")
app.include_router(login_router, prefix="/api/login")
app.include_router(file_router, prefix="/api/file") 

# Mount the static folder at the root.
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
