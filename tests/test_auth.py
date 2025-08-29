def test_register_and_login_and_me(client, unique_username):
    # Register
    r = client.post(
        "/api/v1/auth/register",
        json={"username": unique_username, "password": "secret"},
    )
    assert r.status_code == 201
    user = r.json()
    assert user["username"] == unique_username
    assert "id" in user

    # Login
    r = client.post(
        "/api/v1/auth/login", json={"username": unique_username, "password": "secret"}
    )
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    # Access protected endpoint
    r = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    me = r.json()
    assert me["username"] == unique_username


def test_login_rejects_bad_credentials(client, unique_username):
    # Ensure the user exists
    client.post(
        "/api/v1/auth/register",
        json={"username": unique_username, "password": "secret"},
    )

    # Wrong password
    r = client.post(
        "/api/v1/auth/login", json={"username": unique_username, "password": "wrong"}
    )
    assert r.status_code == 401
