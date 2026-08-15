from authlib.integrations.base_client.errors import OAuthError
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from config import Settings, get_settings
from oauth import get_oauth
from redis_client import get_async_redis_client
from session import SESSION_COOKIE_NAME, create_session, delete_session

router = APIRouter()


@router.get("/login")
async def login(request: Request, settings: Settings = Depends(get_settings)):
    oauth = await get_oauth()
    # duration defaults to "temporary": a 1-hour access token with no refresh
    # token, which is enough time for a user to browse and export their data.
    return await oauth.reddit.authorize_redirect(
        request, settings.reddit_redirect_uri, duration="temporary"
    )


@router.get("/callback")
async def callback(request: Request, redis_client=Depends(get_async_redis_client)):
    oauth = await get_oauth()
    try:
        token = await oauth.reddit.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(status_code=400, detail="Reddit authorization failed") from error

    expires_in = int(token.get("expires_in", 3600))
    session_id = await create_session(redis_client, token["access_token"], expires_in)

    response = RedirectResponse(url="/")
    response.set_cookie(
        SESSION_COOKIE_NAME,
        session_id,
        max_age=expires_in,
        httponly=True,
        samesite="lax",
    )
    return response


@router.post("/logout")
async def logout(request: Request, redis_client=Depends(get_async_redis_client)):
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id:
        await delete_session(redis_client, session_id)

    response = RedirectResponse(url="/")
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response
