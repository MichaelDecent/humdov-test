from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.recommendation import get_personalized_feed


router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("/{user_id}", response_model=List[schemas.FeedItem])
def personalized_feed(user_id: int, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    if not crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    items = get_personalized_feed(db, user_id=user_id, limit=limit, offset=offset)
    return [
        schemas.FeedItem(post=schemas.PostRead.model_validate(p), score=score, reason=reason)
        for (p, score, reason) in items
    ]

