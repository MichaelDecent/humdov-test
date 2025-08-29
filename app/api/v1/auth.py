from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import schemas
from app.services import auth_service


router = APIRouter()


@router.post("/register", response_model=schemas.UserRead, status_code=201)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register(db, payload)


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, payload)
