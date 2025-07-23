import io
import requests
import tweepy

from core.settings import settings

# Daily post limits
MAX_TWITTER_POSTS_PER_DAY = 5
MAX_IG_POSTS_PER_DAY = 25

def is_twitter_configured():
    return all([settings.twitter_api_key, settings.twitter_api_secret, settings.twitter_access_token, settings.twitter_access_secret])

def is_instagram_configured():
    return bool(settings.instagram_access_token and settings.instagram_user_id)

def post_to_twitter(image_bytes, text: str):
    """Post a tweet with optional image."""
    if not is_twitter_configured():
        raise RuntimeError("Twitter API not configured")
    # Authenticate with Twitter (X) API using OAuth1
    auth = tweepy.OAuth1UserHandler(
        settings.twitter_api_key, settings.twitter_api_secret,
        settings.twitter_access_token, settings.twitter_access_secret
    )
    api = tweepy.API(auth)
    if image_bytes:
        # Upload media
        media_obj = api.media_upload(filename="hero_image", file=io.BytesIO(image_bytes))
        api.update_status(status=text, media_ids=[media_obj.media_id_string])
    else:
        api.update_status(status=text)

def post_to_instagram(image_url: str, caption: str):
    """Publish an image post to Instagram via Graph API."""
    if not is_instagram_configured():
        raise RuntimeError("Instagram API not configured")
    ig_user_id = settings.instagram_user_id
    token = settings.instagram_access_token
    # Create media container
    create_url = f"https://graph.facebook.com/v16.0/{ig_user_id}/media"
    params = {"image_url": image_url, "caption": caption, "access_token": token}
    resp = requests.post(create_url, params=params)
    if resp.status_code != 200:
        raise RuntimeError(f"Instagram media upload failed: {resp.text}")
    creation_id = resp.json().get("id")
    if not creation_id:
        raise RuntimeError("Instagram media creation_id not returned")
    # Publish media
    publish_url = f"https://graph.facebook.com/v16.0/{ig_user_id}/media_publish"
    resp2 = requests.post(publish_url, params={"creation_id": creation_id, "access_token": token})
    if resp2.status_code != 200:
        raise RuntimeError(f"Instagram publish failed: {resp2.text}")
