**Personalized Post Feed API**

- **Stack:** Python, FastAPI, SQLite, SQLAlchemy, Alembic
- **Features:** Users, posts, likes, personalized feed, seed data.

**Quick Start (Local)**
- Create venv: `python -m venv .venv && source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt`
- Run migrations: `alembic upgrade head`
- Seed demo data: `python scripts/seed.py`
- Start API: `uvicorn app.main:app --reload`

By default, the app uses `sqlite:///./app.db`. Override with `DATABASE_URL`.

**Docker (Local)**
- Using Makefile (recommended):
  - Start: `make compose-up`
  - Logs: `make logs`
  - Stop: `make compose-down`
  - Clean (also remove volumes): `make clean`
- Directly with Compose: `docker compose up --build`
- App URL: `http://localhost:8000`
- Persistence: SQLite at `/data/app.db` via the `app_data` volume.
- Dev tip: For live reload, uncomment the bind mount and `--reload` command in `docker-compose.yml`.

**Endpoints**
- Public:
  - `POST /api/v1/auth/register` — Create user with password (`{"username","password"}`).
  - `POST /api/v1/auth/login` — Obtain JWT token.
  - `GET /api/v1/users` — List users.
  - `GET /api/v1/users/{id}` — Get a user.
  - `GET /api/v1/posts` — List posts (newest first).
  - `GET /api/v1/posts/{id}` — Get a post.
- Secured (Authorization: `Bearer <token>`):
  - `GET /api/v1/users/me` — Current user info.
  - `POST /api/v1/posts` — Create post. Body: `{ "author_id": <your_id>, "content": "..." }` (author must match token).
  - `POST /api/v1/posts/{post_id}/like` — Like post. Body: `{ "user_id": <your_id> }` (must match token).
  - `DELETE /api/v1/posts/{post_id}/like?user_id=<your_id>` — Unlike post (must match token).
  - `GET /api/v1/feed/{user_id}?limit=20&offset=0` — Personalized feed for the authenticated user only.

Interactive docs live at `/docs` when the server is running.
Hosted Swagger UI: https://humdov-test.onrender.com/docs

**Pesonalized Feed Recommendation Approach**
- We compute a simple weighted score per post and sort descending:
  - Recency: `1 / (1 + age_days)` — fresher posts score higher.
  - Author preference: `1.0` if the user has previously liked any post by the post’s author, else `0.0`.
  - Popularity: `1 + log2(like_count)`, lightly normalized.
- Final score: `0.6*recency + 0.3*author_pref + 0.1*popularity_normalized`.
- Exclusions: We hide posts authored by the viewing user and posts they already liked.

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

**Authentication (JWT)**
- Register: `POST /api/v1/auth/register` with `{ "username": "alice", "password": "secret" }`
- Login: `POST /api/v1/auth/login` with `{ "username": "alice", "password": "secret" }` ⇒ returns `{ "access_token": "...", "token_type": "bearer" }`
- Me: `GET /api/v1/users/me` with header `Authorization: Bearer <token>`

Config:
- `JWT_SECRET` (default `dev-secret-change-me`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (default `60`)

**Testing**
- Run tests: `make test` (or `pytest`)
- Notes: Tests use a temporary SQLite database and a fixed `JWT_SECRET` so they do not affect local dev data.
