import httpx, json, logging
from app.core.config import get_settings

settings = get_settings()
log = logging.getLogger(__name__)

async def tweet(text: str, media_url: str | None = None):
    if not settings.TWITTER_BEARER_TOKEN:
        log.warning("Twitter token not configured")
        return
    headers = {"Authorization": f"Bearer {settings.TWITTER_BEARER_TOKEN}", "Content-Type": "application/json"}
    payload = {"text": text}
    async with httpx.AsyncClient() as client:
        r = await client.post("https://api.twitter.com/2/tweets", headers=headers, json=payload)
        r.raise_for_status()
        return r.json()
