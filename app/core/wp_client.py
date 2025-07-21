import httpx, logging
from app.core.config import get_settings

settings = get_settings()
log = logging.getLogger(__name__)

async def _get_jwt_token() -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{settings.WP_URL}/wp-json/jwt-auth/v1/token", data={
            "username": settings.WP_JWT_USER,
            "password": settings.WP_JWT_PASSWORD
        })
        r.raise_for_status()
        return r.json()["token"]

async def create_post(title: str, content: str, slug: str, meta: dict, layout_json: dict):
    token = await _get_jwt_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "title": title,
        "slug": slug,
        "status": "publish",
        "content": content,
        "meta": meta,
        "bricks": layout_json
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{settings.WP_URL}/wp-json/wp/v2/posts", headers=headers, json=payload)
        r.raise_for_status()
        return r.json()
