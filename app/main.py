from fastapi import FastAPI
from sqlalchemy import text

from .core.db import engine, Base, SessionLocal
from .api.v1 import api_router
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personalized Post Feed API")

app.include_router(api_router)


@app.on_event("startup")
def seed_if_empty() -> None:
    # Ensure new auth column exists for SQLite demos
    try:
        with engine.connect() as conn:
            # Works for SQLite; harmless on others if adapted
            res = conn.execute(text("PRAGMA table_info('users')")).mappings().all()
            cols = {r["name"] for r in res}
            if "password_hash" not in cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(256)"))
                conn.commit()
    except Exception:
        pass

    try:
        from scripts.seed import seed
    except Exception:
        return

    db = SessionLocal()
    try:
        has_users = db.query(models.User).count() > 0
        if not has_users:
            seed(db)
    finally:
        db.close()
