"""
WordPress ↔ API helper.
Obsługa Bricks 2.0 = zwykłe WP REST API (layout Bricks trzyma w _meta).
"""

from __future__ import annotations
from pathlib import Path
from typing import Tuple
import logging
import requests

from core.settings import settings

log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
BASE   = settings.wordpress_url.rstrip("/")
AUTH   = (settings.wordpress_username, settings.wordpress_password)
HEADERS_JSON = {"Content-Type": "application/json"}

def is_configured() -> bool:
    return bool(BASE and AUTH[0] and AUTH[1])

# ----------  media  ----------
def _upload_media(image_path: Path | None, image_bytes: bytes | None) -> Tuple[int | None, str | None]:
    """
    Zwraca (media_id, media_url) – oba None, gdy brak pliku.
    """
    if not image_path and not image_bytes:
        return None, None

    filename = (image_path or Path("featured")).with_suffix(".jpg").name
    files    = {"file": (filename, image_bytes or image_path.read_bytes(), "image/jpeg")}

    r = requests.post(
        f"{BASE}/wp-json/wp/v2/media",
        auth=AUTH,
        files=files,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        timeout=30,
    )
    r.raise_for_status()
    js = r.json()
    return js["id"], js["source_url"]


# ----------  create / update  ----------
def _payload(article, media_id: int | None) -> dict:
    return {
        "title":          article.title,
        "content":        article.content,        # Bricks 2.0 zgarnia HTML – OK
        "excerpt":        article.meta_description,
        "status":         "publish",
        "featured_media": media_id or 0,
    }


def create_post(article, img_bytes: bytes | None, img_path: Path | None) -> Tuple[int, str, str]:
    media_id, img_url = _upload_media(img_path, img_bytes)
    r = requests.post(
        f"{BASE}/wp-json/wp/v2/posts",
        auth=AUTH,
        headers=HEADERS_JSON,
        json=_payload(article, media_id),
        timeout=30,
    )
    r.raise_for_status()
    js = r.json()
    return js["id"], js["link"], img_url


def update_post(article, img_bytes: bytes | None, img_path: Path | None) -> Tuple[int, str, str]:
    """
    Aktualizuje istniejący post (article.wordpress_id != None).
    Jeżeli podamy nowe `img_bytes`, podmienia featured image.
    """
    media_id = None
    img_url  = article.image_url
    if img_bytes or img_path:
        media_id, img_url = _upload_media(img_path, img_bytes)

    r = requests.put(
        f"{BASE}/wp-json/wp/v2/posts/{article.wordpress_id}",
        auth=AUTH,
        headers=HEADERS_JSON,
        json=_payload(article, media_id),
        timeout=30,
    )
    r.raise_for_status()
    js = r.json()
    return js["id"], js["link"], img_url
