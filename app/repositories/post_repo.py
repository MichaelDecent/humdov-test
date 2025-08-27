from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schemas


def create(db: Session, post: schemas.PostCreate) -> models.Post:
    db_post = models.Post(author_id=post.author_id, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get(db: Session, post_id: int) -> Optional[models.Post]:
    return db.get(models.Post, post_id)


def list(db: Session, skip: int = 0, limit: int = 100) -> List[models.Post]:
    stmt = select(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())

