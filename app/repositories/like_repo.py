from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app import models


def get(db: Session, user_id: int, post_id: int) -> Optional[models.Like]:
    stmt = select(models.Like).where(models.Like.user_id == user_id, models.Like.post_id == post_id)
    return db.execute(stmt).scalar_one_or_none()


def create(db: Session, user_id: int, post_id: int) -> models.Like:
    like = models.Like(user_id=user_id, post_id=post_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


def delete(db: Session, like: models.Like) -> None:
    db.delete(like)
    db.commit()


def count_for_post(db: Session, post_id: int) -> int:
    return db.execute(
        select(func.count(models.Like.id)).where(models.Like.post_id == post_id)
    ).scalar_one()

