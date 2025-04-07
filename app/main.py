# /app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="My FastAPI App")

# Include your API routers with specific prefixes.
from .routers.browse import router as browse_router
from .routers.upload import router as upload_router
from .routers.llm import router as llm_router
from .routers.dbexplorer import router as dbexplorer_router
from .routers.login import router as login_router  # newly added

app.include_router(browse_router, prefix="/api/browse")
app.include_router(upload_router, prefix="/api/upload")
app.include_router(llm_router, prefix="/api/llm")
app.include_router(dbexplorer_router, prefix="/api/dbexplorer")
app.include_router(login_router, prefix="/api/login")  # add login endpoints

# Mount the static folder at the root.
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
