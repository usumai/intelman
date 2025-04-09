from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from .routing import router
app = FastAPI(title="My FastAPI App")
app.include_router(router)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")