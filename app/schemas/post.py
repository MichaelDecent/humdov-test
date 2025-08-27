from datetime import datetime
from pydantic import BaseModel


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

