from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import schemas
from app.services import user_service
from app.core.security import get_current_user


router = APIRouter()


@router.get("/me", response_model=schemas.UserRead)
def me(current_user=Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    u = user_service.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u


@router.get("", response_model=List[schemas.UserRead])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.list_users(db, skip=skip, limit=limit)
