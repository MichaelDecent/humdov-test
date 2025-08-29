from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app import schemas
from app.services import user_service
from app.services.feed_service import get_feed
from app.core.security import get_current_user


router = APIRouter()


@router.get("/{user_id}", response_model=List[schemas.FeedItem])
def personalized_feed(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not user_service.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: mismatched user")
    items = get_feed(db, user_id=user_id, limit=limit, offset=offset)
    return [
        schemas.FeedItem(post=schemas.PostRead.model_validate(p), score=score, reason=reason)
        for (p, score, reason) in items
    ]
