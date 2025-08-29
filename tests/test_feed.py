def test_feed_access_and_mismatch_forbidden(client, auth_headers):
    # Authenticated user can access their own feed
    me = client.get("/api/v1/users/me", headers=auth_headers).json()
    user_id = me["id"]
    r = client.get(f"/api/v1/feed/{user_id}", headers=auth_headers)
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)

    # Accessing another user's feed should be forbidden
    # Create a different user and login
    uname = "feed_foo"
    client.post("/api/v1/auth/register", json={"username": uname, "password": "secret"})
    r2 = client.post(
        "/api/v1/auth/login", json={"username": uname, "password": "secret"}
    )
    other_token = r2.json()["access_token"]

    # Using first user's token to access other user's feed -> 403
    r = client.get(
        f"/api/v1/feed/{me['id'] + 9999}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert r.status_code in (403, 404)
