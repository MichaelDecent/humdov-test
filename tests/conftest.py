import os
import sys
import uuid
from pathlib import Path
import pytest


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))

    data_dir = tmp_path_factory.mktemp("data")
    db_path = data_dir / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["JWT_SECRET"] = "test-secret"

    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def unique_username():
    return f"user_{uuid.uuid4().hex[:8]}"


@pytest.fixture()
def auth_headers(client, unique_username):
    r = client.post(
        "/api/v1/auth/register",
        json={"username": unique_username, "password": "secret"},
    )
    assert r.status_code == 201
    r = client.post(
        "/api/v1/auth/login", json={"username": unique_username, "password": "secret"}
    )
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
