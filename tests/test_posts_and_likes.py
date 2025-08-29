def test_create_like_unlike_flow(client, auth_headers):
    # Who am I?
    me = client.get("/api/v1/users/me", headers=auth_headers).json()
    user_id = me["id"]

    # Create a post as me
    payload = {"author_id": user_id, "content": "hello world"}
    r = client.post("/api/v1/posts", json=payload, headers=auth_headers)
    assert r.status_code == 201
    post = r.json()
    post_id = post["id"]

    r = client.post(
        f"/api/v1/posts/{post_id}/like", json={"user_id": user_id}, headers=auth_headers
    )
    assert r.status_code == 201
    like = r.json()
    assert like["post_id"] == post_id
    assert like["user_id"] == user_id

    # Unlike the post as me
    r = client.delete(
        f"/api/v1/posts/{post_id}/like",
        params={"user_id": user_id},
        headers=auth_headers,
    )
    assert r.status_code == 204


def test_security_enforcement_on_posts_and_likes(client, auth_headers, unique_username):
    # Create another distinct user and login to obtain a second token
    other_username = unique_username + "_other"
    client.post(
        "/api/v1/auth/register", json={"username": other_username, "password": "secret"}
    )
    r = client.post(
        "/api/v1/auth/login", json={"username": other_username, "password": "secret"}
    )
    token2 = r.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    me = client.get("/api/v1/users/me", headers=auth_headers).json()
    user1_id = me["id"]

    # Unauthenticated create post should fail
    r = client.post("/api/v1/posts", json={"author_id": user1_id, "content": "x"})
    assert r.status_code == 401

    # Authenticated but creating for another user should fail
    other_me = client.get("/api/v1/users/me", headers=headers2).json()
    other_id = other_me["id"]
    r = client.post(
        "/api/v1/posts",
        json={"author_id": other_id, "content": "x"},
        headers=auth_headers,
    )
    assert r.status_code == 403

    # Create a post as user1
    r = client.post(
        "/api/v1/posts",
        json={"author_id": user1_id, "content": "p"},
        headers=auth_headers,
    )
    post_id = r.json()["id"]

    # User2 tries to like as user1 -> forbidden
    r = client.post(
        f"/api/v1/posts/{post_id}/like", json={"user_id": user1_id}, headers=headers2
    )
    assert r.status_code == 403
