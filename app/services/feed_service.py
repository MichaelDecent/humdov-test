from __future__ import annotations

from typing import List, Tuple
from datetime import datetime
from math import log2

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app import models


def _recency_score(dt: datetime) -> float:
    age_seconds = max(0.0, (datetime.utcnow() - dt).total_seconds())
    age_days = age_seconds / 86400.0
    return 1.0 / (1.0 + age_days)


def _author_pref_score(authors_liked: set[int], author_id: int) -> float:
    return 1.0 if author_id in authors_liked else 0.0


def _popularity_score(db: Session, post_id: int) -> float:
    count = db.execute(
        select(func.count(models.Like.id)).where(models.Like.post_id == post_id)
    ).scalar_one()
    if count <= 0:
        return 0.0
    return 1.0 + log2(count)


def get_feed(
    db: Session, user_id: int, limit: int = 20, offset: int = 0
) -> List[Tuple[models.Post, float, str]]:
    authors = set(
        db.execute(
            select(models.Post.author_id)
            .join(models.Like, models.Like.post_id == models.Post.id)
            .where(models.Like.user_id == user_id)
        ).scalars()
    )
    liked_post_ids = set(
        db.execute(
            select(models.Like.post_id).where(models.Like.user_id == user_id)
        ).scalars()
    )
    candidates = (
        db.execute(
            select(models.Post)
            .where(models.Post.author_id != user_id)
            .order_by(models.Post.created_at.desc())
        )
        .scalars()
        .all()
    )
    scored: List[Tuple[models.Post, float, str]] = []
    for p in candidates:
        if p.id in liked_post_ids:
            continue
        rec = _recency_score(p.created_at)
        auth = _author_pref_score(authors, p.author_id)
        pop = _popularity_score(db, p.id)
        score = 0.6 * rec + 0.3 * auth + 0.1 * min(pop / 5.0, 1.0)
        reason = f"recency={rec:.2f}, author_pref={auth:.2f}, popularity={pop:.2f}"
        scored.append((p, score, reason))
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored[offset : offset + limit]
