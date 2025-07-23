import requests
from fastapi import HTTPException

from core.settings import settings

def is_configured():
    """Check if WordPress integration is configured."""
    return bool(settings.wordpress_url and settings.wordpress_username and settings.wordpress_password)

def publish_to_wordpress(article, image_bytes=None, image_type=None, image_ext=None):
    """Create a WordPress post (and upload media if provided). Returns (post_id, post_url, image_url)."""
    if not is_configured():
        raise HTTPException(status_code=503, detail="WordPress integration not configured")
    base_url = settings.wordpress_url.rstrip("/")
    # Authenticate via JWT
    try:
        token_resp = requests.post(f"{base_url}/wp-json/jwt-auth/v1/token", json={
            "username": settings.wordpress_username,
            "password": settings.wordpress_password
        })
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail="Could not connect to WordPress")
    if token_resp.status_code != 200:
        raise HTTPException(status_code=502, detail="WordPress authentication failed")
    token = token_resp.json().get("token")
    if not token:
        raise HTTPException(status_code=502, detail="WordPress JWT token not obtained")
    headers = {"Authorization": f"Bearer {token}"}
    media_id = None
    media_url = None
    # Upload featured image if provided
    if image_bytes:
        files = {"file": (f"hero.{image_ext}", image_bytes, image_type)}
        try:
            media_resp = requests.post(f"{base_url}/wp-json/wp/v2/media", headers=headers, files=files)
        except requests.RequestException as e:
            raise HTTPException(status_code=502, detail="WordPress media upload failed")
        if media_resp.status_code == 201:
            media_data = media_resp.json()
            media_id = media_data.get("id")
            media_url = media_data.get("source_url")
        else:
            # Log but do not raise (allow posting without image)
            media_id = None
            media_url = None
    # Create the post
    post_payload = {
        "title": article.title,
        "content": article.content,
        "status": "publish",
    }
    if article.meta_description:
        post_payload["excerpt"] = article.meta_description
    if media_id:
        post_payload["featured_media"] = media_id
    try:
        post_resp = requests.post(f"{base_url}/wp-json/wp/v2/posts", headers=headers, json=post_payload)
    except requests.RequestException as e:
        # If post creation fails, attempt cleanup of media (optional)
        if media_id:
            try:
                requests.delete(f"{base_url}/wp-json/wp/v2/media/{media_id}?force=true", headers=headers)
            except:
                pass
        raise HTTPException(status_code=502, detail="WordPress post creation failed")
    if post_resp.status_code not in (200, 201):
        if media_id:
            try:
                requests.delete(f"{base_url}/wp-json/wp/v2/media/{media_id}?force=true", headers=headers)
            except:
                pass
        raise HTTPException(status_code=502, detail="Failed to create WordPress post")
    post_data = post_resp.json()
    wp_id = post_data.get("id")
    wp_link = post_data.get("link")
    return wp_id, wp_link, media_url
