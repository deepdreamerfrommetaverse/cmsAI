import httpx, logging, json, mimetypes, os, aiofiles
from app.core.config import get_settings

settings = get_settings()
log = logging.getLogger(__name__)

async def _get_jwt_token() -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(f"{settings.WP_URL}/wp-json/jwt-auth/v1/token", data={
            "username": settings.WP_JWT_USER,
            "password": settings.WP_JWT_PASSWORD
        }, timeout=30)
        r.raise_for_status()
        return r.json()["token"]

async def _upload_media(url: str, token: str) -> int | None:
    filename = url.split("/")[-1].split("?")[0]
    mime, _ = mimetypes.guess_type(filename)
    async with httpx.AsyncClient() as client:
        img = await client.get(url)
        img.raise_for_status()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": mime or "image/jpeg",
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        r = await client.post(f"{settings.WP_URL}/wp-json/wp/v2/media", headers=headers, content=img.content)
        if r.status_code == 201:
            return r.json()["id"]
        log.warning("Media upload failed: %s", r.text)
        return None

async def create_post_full(payload: dict):
    """payload keys: title, slug, content, meta, layout_json, hero_url"""
    token = await _get_jwt_token()
    featured_id = await _upload_media(payload["hero_url"], token) if payload.get("hero_url") else None
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "title": payload["title"],
        "slug": payload["slug"],
        "status": "publish",
        "content": payload["content"],
        "meta": payload["meta"],
        "bricks_layout": json.dumps(payload["layout_json"]),
    }
    if featured_id:
        data["featured_media"] = featured_id

    async with httpx.AsyncClient() as client:
        r = await client.post(f"{settings.WP_URL}/wp-json/wp/v2/posts", headers=headers, json=data, timeout=60)
        r.raise_for_status()
        return r.json()
