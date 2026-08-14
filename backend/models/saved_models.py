from pydantic import BaseModel


class Comment(BaseModel):
    # TODO: Parse Redditor model
    author: str
    # TODO: body is markdown, body_html is also an option
    body: str
    created_utc: float
    id: str
    subreddit: str
    link_id: str
    parent_id: str
    permalink: str
    submission: str
    score: int


class Submission(BaseModel):
    # TODO: Parse Redditor model
    author: str
    created_utc: float
    id: str
    permalink: str
    subreddit: str
    title: str
    url: str
