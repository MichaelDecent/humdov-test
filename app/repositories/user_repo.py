from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app import models, schemas


def create(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get(db: Session, user_id: int) -> Optional[models.User]:
    return db.get(models.User, user_id)


def list(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    stmt = select(models.User).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars())

