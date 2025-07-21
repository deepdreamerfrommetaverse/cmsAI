import pytest

@pytest.mark.anyio
async def test_register_and_login(async_client):
    # register
    r = await async_client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "secret"
    })
    assert r.status_code == 200
    # login
    r = await async_client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "secret"
    })
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token
