import openai, logging
from app.core.config import get_settings

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY
log = logging.getLogger(__name__)

async def generate_article(prompt: str) -> str:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured")
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial journalist writing concise but thorough articles."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024
    )
    return completion.choices[0].message.content.strip()
