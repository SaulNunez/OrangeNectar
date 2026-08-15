from typing import Optional

from authlib.integrations.starlette_client import OAuth

from config import get_settings
from redis_client import get_async_redis_client

_oauth: Optional[OAuth] = None


async def get_oauth() -> OAuth:
    global _oauth
    if _oauth is None:
        settings = get_settings()
        redis_client = await get_async_redis_client()

        # Reddit requires: HTTP Basic auth for the token exchange, and a custom
        # User-Agent on every request (including the token exchange) or it may
        # reject/throttle the client.
        oauth = OAuth(cache=redis_client)
        oauth.register(
            name="reddit",
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            authorize_url="https://www.reddit.com/api/v1/authorize",
            access_token_url="https://www.reddit.com/api/v1/access_token",
            client_kwargs={
                "scope": "identity history",
                "token_endpoint_auth_method": "client_secret_basic",
                "headers": {"User-Agent": settings.reddit_user_agent},
            },
        )
        _oauth = oauth
    return _oauth
