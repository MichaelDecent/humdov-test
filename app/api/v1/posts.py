from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("", response_model=schemas.PostRead, status_code=201)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    if not crud.get_user(db, post.author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_post(db, post)


@router.get("/{post_id}", response_model=schemas.PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    p = crud.get_post(db, post_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post not found")
    return p


@router.get("", response_model=List[schemas.PostRead])
def list_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)


@router.post("/{post_id}/like", response_model=schemas.LikeRead, status_code=201)
def like(post_id: int, payload: schemas.LikeCreate, db: Session = Depends(get_db)):
    if not crud.get_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    if not crud.get_user(db, payload.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    like = crud.like_post(db, payload.user_id, post_id)
    return like


@router.delete("/{post_id}/like", status_code=204)
def unlike(post_id: int, user_id: int, db: Session = Depends(get_db)):
    if not crud.get_post(db, post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    if not crud.get_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    ok = crud.unlike_post(db, user_id, post_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Like not found")
    return None

