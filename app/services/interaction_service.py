from sqlalchemy.orm import Session

from app.repositories import like_repo, post_repo, user_repo


def like_post(db: Session, user_id: int, post_id: int):
    if not post_repo.get(db, post_id) or not user_repo.get(db, user_id):
        return None
    existing = like_repo.get(db, user_id, post_id)
    if existing:
        return existing
    return like_repo.create(db, user_id, post_id)


def unlike_post(db: Session, user_id: int, post_id: int) -> bool:
    if not post_repo.get(db, post_id) or not user_repo.get(db, user_id):
        return False
    existing = like_repo.get(db, user_id, post_id)
    if not existing:
        return False
    like_repo.delete(db, existing)
    return True

