from fastapi import FastAPI

from .api.v1.users import router as users_router
from .api.v1.posts import router as posts_router
from .api.v1.feed import router as feed_router


app = FastAPI(title="Personalized Post Feed API")

prefix = "/api/v1"

# Mount versioned API at /api/v1
app.include_router(users_router, prefix=prefix)
app.include_router(posts_router, prefix=prefix)
app.include_router(feed_router, prefix=prefix)
