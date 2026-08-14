from typing import List, Union

from fastapi import APIRouter, Depends

from config import Settings, get_settings
from models.saved_models import Comment, Submission
from services.reddit_service import RedditService

router = APIRouter()


def get_reddit_service(settings: Settings = Depends(get_settings)) -> RedditService:
    return RedditService(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent=settings.reddit_user_agent,
    )


@router.get("/saved", response_model=List[Union[Comment, Submission]])
def get_saved_posts(reddit_service: RedditService = Depends(get_reddit_service)):
    return reddit_service.fetch_saved_posts()
