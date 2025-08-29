from sqlalchemy.orm import Session

from app import models, schemas
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from fastapi import HTTPException


def register(db: Session, payload: schemas.RegisterRequest) -> models.User:
    existing = (
        db.query(models.User).filter(models.User.username == payload.username).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = models.User(
        username=payload.username, password_hash=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, payload: schemas.LoginRequest) -> schemas.Token:
    user = (
        db.query(models.User).filter(models.User.username == payload.username).first()
    )
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(
        {"sub": str(user.id), "username": user.username},
        expires_in_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return schemas.Token(access_token=token)
