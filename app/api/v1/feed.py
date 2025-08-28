from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import schemas
from app.services import user_service
from app.services.feed_service import get_feed


router = APIRouter()


@router.get("/{user_id}", response_model=List[schemas.FeedItem])
def personalized_feed(user_id: int, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    if not user_service.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    items = get_feed(db, user_id=user_id, limit=limit, offset=offset)
    return [
        schemas.FeedItem(post=schemas.PostRead.model_validate(p), score=score, reason=reason)
        for (p, score, reason) in items
    ]
