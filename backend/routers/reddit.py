from typing import List, Union

from fastapi import APIRouter, Depends, Request

from config import Settings, get_settings
from models.saved_models import Comment, Submission
from redis_client import get_async_redis_client
from services.reddit_service import RedditService
from session import get_session_access_token

router = APIRouter()


async def get_reddit_service(
    request: Request,
    settings: Settings = Depends(get_settings),
    redis_client=Depends(get_async_redis_client),
) -> RedditService:
    access_token, expires_in = await get_session_access_token(request, redis_client)
    return RedditService(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent=settings.reddit_user_agent,
        access_token=access_token,
        expires_in=expires_in,
    )


@router.get("/saved", response_model=List[Union[Comment, Submission]])
def get_saved_posts(reddit_service: RedditService = Depends(get_reddit_service)):
    return reddit_service.fetch_saved_posts()
