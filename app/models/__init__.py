from app.core.db import Base  # re-export Base for Alembic discovery

from .user import User  # noqa: F401
from .post import Post  # noqa: F401
from .like import Like  # noqa: F401

