from typing import List, Optional, Union

import praw
import redis

from models.saved_models import Comment, Submission


class RedditService:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        redis_client: Optional[redis.Redis] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.redis_client = redis_client
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def fetch_saved_posts(self) -> List[Union[Comment, Submission]]:
        saved_items: List[Union[Comment, Submission]] = []
        for item in self.reddit.user.me().saved(limit=None):
            if isinstance(item, praw.models.Comment):
                saved_items.append(Comment(
                    author=str(item.author),
                    body=item.body,
                    created_utc=item.created_utc,
                    id=item.id,
                    subreddit=str(item.subreddit),
                    link_id=item.link_id,
                    parent_id=item.parent_id,
                    permalink=item.permalink,
                    submission=item.link_id.removeprefix("t3_"),
                    score=item.score,
                ))
            elif isinstance(item, praw.models.Submission):
                video_url = None
                if item.is_video and item.media:
                    video_url = item.media.get("reddit_video", {}).get("fallback_url")

                saved_items.append(Submission(
                    author=str(item.author),
                    created_utc=item.created_utc,
                    id=item.id,
                    permalink=item.permalink,
                    subreddit=str(item.subreddit),
                    title=item.title,
                    url=item.url,
                    video_url=video_url,
                ))
        return saved_items
