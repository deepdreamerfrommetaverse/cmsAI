import pytest

@pytest.mark.anyio
async def test_article_crud(async_client):
    # register user
    await async_client.post("/api/v1/auth/register", json={
        "email": "author@example.com",
        "password": "secret"
    })
    # login
    r = await async_client.post("/api/v1/auth/login", json={
        "email": "author@example.com",
        "password": "secret"
    })
    token = r.json()["access_token"]
    headers = {"Authorization": f"{token}"}

    # create article
    r = await async_client.post("/api/v1/articles/", json={
        "title": "Test",
        "slug": "test-article",
        "body": "Hello world"
    }, headers=headers)
    assert r.status_code == 201
    art_id = r.json()["id"]

    # list
    r = await async_client.get("/api/v1/articles/")
    assert any(a["id"] == art_id for a in r.json())
