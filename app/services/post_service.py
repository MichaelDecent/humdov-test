from sqlalchemy.orm import Session

from app import schemas
from app.repositories import post_repo, user_repo


def create_post(db: Session, post: schemas.PostCreate):
    if not user_repo.get(db, post.author_id):
        return None
    return post_repo.create(db, post)


def get_post(db: Session, post_id: int):
    return post_repo.get(db, post_id)


def list_posts(db: Session, skip: int = 0, limit: int = 100):
    return post_repo.list(db, skip, limit)

