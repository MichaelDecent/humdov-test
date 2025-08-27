**Personalized Post Feed API**

- **Stack:** Python, FastAPI, SQLite, SQLAlchemy, Alembic
- **Features:** Users, posts, likes, personalized feed, seed data.

**Quick Start**
- Create venv: `python -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt`
- Run migrations: `alembic upgrade head`
- Seed demo data: `python scripts/seed.py`
- Start API: `uvicorn app.main:app --reload`

By default, the app uses `sqlite:///./app.db`. Override with `DATABASE_URL`.

**Endpoints**
- `POST /api/v1/users` — Create user. Body: `{ "username": "alice" }`
- `GET /api/v1/users` — List users.
- `GET /api/v1/users/{id}` — Get a user.
- `POST /api/v1/posts` — Create post. Body: `{ "author_id": 1, "content": "hello" }`
- `GET /api/v1/posts` — List posts (newest first).
- `GET /api/v1/posts/{id}` — Get a post.
- `POST /api/v1/posts/{post_id}/like` — Like a post. Body: `{ "user_id": 1 }`.
- `DELETE /api/v1/posts/{post_id}/like?user_id=1` — Unlike a post.
- `GET /api/v1/feed/{user_id}?limit=20&offset=0` — Personalized feed.

Interactive docs live at `/docs` when the server is running.

**Recommendation Approach**
- We compute a simple weighted score per post and sort descending:
  - Recency: `1 / (1 + age_days)` — fresher posts score higher.
  - Author preference: `1.0` if the user has previously liked any post by the post’s author, else `0.0`.
  - Popularity: `1 + log2(like_count)`, lightly normalized.
- Final score: `0.6*recency + 0.3*author_pref + 0.1*popularity_normalized`.
- Exclusions: We hide posts authored by the viewing user and posts they already liked.

**Trade-offs**
- Very simple, transparent ranking that’s fast on SQLite and easy to inspect.
- Not collaborative yet; could extend with user–user similarity, topic tags, or embeddings.
- Popularity is lightly weighted to avoid runaway feedback loops.

**Dev Notes**
- Migrations are pre-baked in `alembic/versions/0001_initial.py` and use metadata from `app.models`.
- Change DB path via `DATABASE_URL` (e.g., `sqlite:///./dev.db`).
- To regenerate DB from scratch: delete `app.db`, run `alembic upgrade head`, then re-run the seed script.

**Project Structure**
- `app/main.py`: FastAPI app and router mounting.
- `app/api/v1/*`: Versioned API routers.
- `app/core/config.py`: App settings (e.g., `DATABASE_URL`).
- `app/core/db.py`: Engine, `SessionLocal`, `Base`, and `get_db` dependency.
- `app/models/*.py`: ORM models split by entity (`user.py`, `post.py`, `like.py`); `app/models.py` aggregates.
- `app/repositories/*.py`: Data access per entity (`user_repo.py`, `post_repo.py`, `like_repo.py`).
- `app/services/*.py`: Business logic (`user_service.py`, `post_service.py`, `interaction_service.py`, `feed_service.py`).

**Sanity Check (after seeding)**
1. `GET /api/v1/users` — note user IDs.
2. `GET /api/v1/posts` — observe posts.
3. `GET /api/v1/feed/1` — user1 prefers authors 3 and 5; you should see their posts boosted while still reflecting recency and light popularity.
