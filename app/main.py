# /app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from .routing import router

app = FastAPI(title="My FastAPI App")

# Include your routers.
app.include_router(router)

app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Define a list of public paths that don't require authentication.
    public_paths = [
        "/login.html",      # Login page
        "/api/login/login"  # Login API endpoint
    ]
    public_prefixes = ["/static", "/css", "/js", "/images"]
    # Allow access to static assets and documentation endpoints without auth.
    if any(request.url.path.startswith(prefix) for prefix in public_prefixes):
        return await call_next(request)

    # If the request path is public, bypass authentication.
    if request.url.path in public_paths:
        return await call_next(request)

    # Check if the access_token cookie is set.
    token = request.cookies.get("access_token")
    if not token:
        # Redirect to the login page if the token is missing.
        return RedirectResponse(url="/login.html")

    # Otherwise, continue processing the request.
    response = await call_next(request)
    return response
