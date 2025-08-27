from __future__ import annotations

import random
from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models


def seed(db: Session) -> None:
    # Clear existing data (simple approach for demo)
    db.query(models.Like).delete()
    db.query(models.Post).delete()
    db.query(models.User).delete()
    db.commit()

    # Create users
    users = [models.User(username=f"user{i}") for i in range(1, 11)]
    db.add_all(users)
    db.commit()
    for u in users:
        db.refresh(u)

    # Create posts with varying recency
    now = datetime.utcnow()
    posts: List[models.Post] = []
    pid = 1
    for author in users:
        for _ in range(3):
            days_ago = random.randint(0, 30)
            p = models.Post(
                author_id=author.id,
                content=f"Post {pid} by {author.username}",
                created_at=now - timedelta(days=days_ago, hours=random.randint(0, 23)),
            )
            posts.append(p)
            pid += 1
    db.add_all(posts)
    db.commit()
    for p in posts:
        db.refresh(p)

    # Likes with skewed preferences:
    # user1 strongly likes posts by user3 and user5
    def like(u: models.User, p: models.Post):
        db.add(models.Like(user_id=u.id, post_id=p.id))

    author3_posts = [p for p in posts if p.author_id == users[2].id]
    author5_posts = [p for p in posts if p.author_id == users[4].id]

    for p in author3_posts + author5_posts:
        like(users[0], p)  # user1

    # Other random likes
    for u in users[1:]:
        liked = random.sample(posts, k=random.randint(5, 15))
        for p in liked:
            if p.author_id == u.id:
                continue
            like(u, p)

    db.commit()
    print("Seeded:")
    print(f"  Users: {len(users)}")
    print(f"  Posts: {len(posts)}")
    likes_count = db.query(models.Like).count()
    print(f"  Likes: {likes_count}")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()

