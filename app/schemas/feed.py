from pydantic import BaseModel

from .post import PostRead


class FeedItem(BaseModel):
    post: PostRead
    score: float
    reason: str
