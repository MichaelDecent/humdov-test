from fastapi import FastAPI
from .core.db import engine, Base, SessionLocal
from .api.v1 import api_router
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personalized Post Feed API")

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def seed_if_empty() -> None:
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
