from fastapi import APIRouter

from . import users, posts, feed


api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["user"])
api_router.include_router(posts.router, prefix="/posts", tags=["post"])
api_router.include_router(feed.router, prefix="/feed", tags=["feed"])
