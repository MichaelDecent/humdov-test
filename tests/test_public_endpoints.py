def test_public_users_and_posts_list(client):
    # Users list is public
    r = client.get("/api/v1/users")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # Posts list is public
    r = client.get("/api/v1/posts")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
