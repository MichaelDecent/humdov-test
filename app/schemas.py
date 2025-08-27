from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    content: str


class PostCreate(PostBase):
    author_id: int


class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LikeCreate(BaseModel):
    user_id: int


class LikeRead(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FeedItem(BaseModel):
    post: PostRead
    score: float
    reason: str
