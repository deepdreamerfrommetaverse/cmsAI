import openai, logging, re
from app.core.config import get_settings

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY
log = logging.getLogger(__name__)

TITLE_MAX = 60
DESC_MAX = 155

def _trim(text: str, limit: int) -> str:
    txt = re.sub('\s+', ' ', text.strip())
    return txt[:limit].rstrip()

async def generate_prompt_agent(prompt: str) -> dict:
    """Returns dict with keys: title, body, meta_title, meta_description, keywords, hero_url, layout_json"""
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing")

    # 1) Generate article + SEO
    system = (
        "You are a senior finance journalist. "
        "Return a JSON with keys title, body (HTML), keywords (comma‑sep). "
        "Keep title ≤60 chars; meta description ≤155 chars."
    )
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=1200
    )
    content = completion.choices[0].message.content
    try:
        payload = json.loads(content)
    except Exception:
        log.error("GPT did not return JSON: %s", content)
        raise

    title = _trim(payload["title"], TITLE_MAX)
    meta_desc = _trim(payload.get("meta_description") or payload["body"][:DESC_MAX], DESC_MAX)

    # 2) Generate hero image via DALL·E 3
    image = await openai.images.generate(
        model="dall-e-3",
        prompt=f"Hero image, concept illustration for article titled '{title}'",
        n=1,
        size="1024x768"
    )
    hero_url = image.data[0].url

    # 3) Basic Bricks 2.0 layout JSON (very simple)
    layout_json = {
        "structure": [
            { "type": "section", "children": [
                { "type": "image", "src": hero_url, "alt": title },
                { "type": "heading", "level": 1, "text": title },
                { "type": "richtext", "html": payload["body"] }
            ]}
        ]
    }

    return {
        "title": title,
        "body": payload["body"],
        "meta_title": title,
        "meta_description": meta_desc,
        "keywords": payload.get("keywords", ""),
        "hero_url": hero_url,
        "layout_json": layout_json
    }
