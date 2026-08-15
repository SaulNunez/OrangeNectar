from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from config import get_settings
from routers import auth, export, reddit

app = FastAPI(title="OrangeNectar")
# Backs Authlib's short-lived CSRF "state" marker during the login redirect.
# The Reddit access token itself lives in Redis, not this cookie.
app.add_middleware(SessionMiddleware, secret_key=get_settings().session_secret_key)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(reddit.router, prefix="/reddit", tags=["reddit"])
app.include_router(export.router, tags=["export"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
