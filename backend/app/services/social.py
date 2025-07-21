import logging, httpx, datetime
from app.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from app.models.social_limit import SocialLimit
import tweepy, json

settings = get_settings()
log = logging.getLogger(__name__)

TW_LIMIT_DEFAULT = 300    # tweets / day
IG_LIMIT_DEFAULT = 25     # posts / day

# ---------- LIMIT HANDLING ----------
async def _increment(db: AsyncSession, service: str, limit_default: int):
    today = datetime.date.today()
    q = await db.execute(select(SocialLimit).where(SocialLimit.service==service, SocialLimit.date==today))
    row = q.scalars().first()
    if row is None:
        row = SocialLimit(service=service, date=today, count=0, limit=limit_default)
        db.add(row)
        await db.commit()
        await db.refresh(row)
    if row.count >= row.limit:
        raise RuntimeError(f"Daily limit for {service} reached")
    await db.execute(update(SocialLimit).where(SocialLimit.id==row.id).values(count=row.count+1))
    await db.commit()

async def get_limits(db: AsyncSession):
    today = datetime.date.today()
    res = await db.execute(select(SocialLimit).where(SocialLimit.date==today))
    limits = {r.service: {"count": r.count, "limit": r.limit} for r in res.scalars()}
    # ensure keys
    for svc, lim in [("twitter", TW_LIMIT_DEFAULT), ("instagram", IG_LIMIT_DEFAULT)]:
        limits.setdefault(svc, {"count": 0, "limit": lim})
    return limits

# ---------- TWITTER ----------
async def tweet(db: AsyncSession, text: str, media_url: str | None = None):
    await _increment(db, "twitter", TW_LIMIT_DEFAULT)
    if not settings.TWITTER_BEARER_TOKEN or not settings.TWITTER_API_KEY_SECRET or not settings.TWITTER_ACCESS_TOKEN or not settings.TWITTER_ACCESS_TOKEN_SECRET or not settings.TWITTER_API_KEY:
        log.warning("Twitter credentials missing")
        return {"status": "disabled"}
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET,
        settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    media_ids = None
    if media_url:
        async with httpx.AsyncClient() as client:
            img = await client.get(media_url)
            img.raise_for_status()
            filename = "/tmp/media.jpg"
            with open(filename, "wb") as f:
                f.write(img.content)
        media = api.media_upload(filename)
        media_ids = [media.media_id_string]
    status = api.update_status(status=text, media_ids=media_ids)
    return {"id": status.id}

# ---------- INSTAGRAM ----------
async def ig_post(db: AsyncSession, caption: str, image_url: str):
    await _increment(db, "instagram", IG_LIMIT_DEFAULT)
    if not settings.IG_ACCESS_TOKEN or not settings.IG_USER_ID:
        log.warning("Instagram creds missing")
        return {"status": "disabled"}
    async with httpx.AsyncClient() as client:
        # 1) create container
        create = await client.post(
            f"https://graph.facebook.com/v19.0/{settings.IG_USER_ID}/media",
            data={
                "image_url": image_url,
                "caption": caption,
                "access_token": settings.IG_ACCESS_TOKEN
            }
        )
        create.raise_for_status()
        creation_id = create.json()["id"]
        # 2) publish
        publish = await client.post(
            f"https://graph.facebook.com/v19.0/{settings.IG_USER_ID}/media_publish",
            data={
                "creation_id": creation_id,
                "access_token": settings.IG_ACCESS_TOKEN
            }
        )
        publish.raise_for_status()
        return publish.json()
