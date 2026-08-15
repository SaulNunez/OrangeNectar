import secrets
from typing import Tuple

from fastapi import HTTPException, Request

SESSION_COOKIE_NAME = "session_id"
SESSION_KEY_PREFIX = "session:"


async def create_session(redis_client, access_token: str, expires_in: int) -> str:
    session_id = secrets.token_urlsafe(32)
    await redis_client.set(f"{SESSION_KEY_PREFIX}{session_id}", access_token, ex=expires_in)
    return session_id


async def delete_session(redis_client, session_id: str) -> None:
    await redis_client.delete(f"{SESSION_KEY_PREFIX}{session_id}")


async def get_session_access_token(request: Request, redis_client) -> Tuple[str, int]:
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id is None:
        raise HTTPException(status_code=401, detail="Not logged in with Reddit")

    key = f"{SESSION_KEY_PREFIX}{session_id}"
    access_token = await redis_client.get(key)
    if access_token is None:
        raise HTTPException(status_code=401, detail="Reddit session expired, please log in again")

    expires_in = await redis_client.ttl(key)
    if expires_in <= 0:
        raise HTTPException(status_code=401, detail="Reddit session expired, please log in again")

    return access_token, expires_in
