from sqlalchemy.orm import Session

from app import schemas
from app.repositories import user_repo


def create_user(db: Session, user: schemas.UserCreate):
    return user_repo.create(db, user)


def get_user(db: Session, user_id: int):
    return user_repo.get(db, user_id)


def list_users(db: Session, skip: int = 0, limit: int = 100):
    return user_repo.list_users(db, skip, limit)
