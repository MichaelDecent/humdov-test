from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.get(models.User, user_id)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    stmt = select(models.User).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())


def create_post(db: Session, post: schemas.PostCreate) -> models.Post:
    db_post = models.Post(author_id=post.author_id, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db: Session, post_id: int) -> Optional[models.Post]:
    return db.get(models.Post, post_id)


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Post]:
    stmt = select(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())


def like_post(db: Session, user_id: int, post_id: int) -> Optional[models.Like]:
    stmt = select(models.Like).where(models.Like.user_id == user_id, models.Like.post_id == post_id)
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        return existing
    like = models.Like(user_id=user_id, post_id=post_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


def unlike_post(db: Session, user_id: int, post_id: int) -> bool:
    stmt = select(models.Like).where(models.Like.user_id == user_id, models.Like.post_id == post_id)
    like = db.execute(stmt).scalar_one_or_none()
    if not like:
        return False
    db.delete(like)
    db.commit()
    return True


def count_likes_for_post(db: Session, post_id: int) -> int:
    return db.execute(
        select(func.count(models.Like.id)).where(models.Like.post_id == post_id)
    ).scalar_one()


def authors_user_liked(db: Session, user_id: int) -> List[int]:
    stmt = (
        select(models.Post.author_id)
        .join(models.Like, models.Like.post_id == models.Post.id)
        .where(models.Like.user_id == user_id)
        .distinct()
    )
    return [row[0] for row in db.execute(stmt).all()]


def recent_posts(db: Session, exclude_author_id: Optional[int] = None) -> List[models.Post]:
    stmt = select(models.Post)
    if exclude_author_id is not None:
        stmt = stmt.where(models.Post.author_id != exclude_author_id)
    stmt = stmt.order_by(models.Post.created_at.desc())
    return list(db.execute(stmt).scalars())