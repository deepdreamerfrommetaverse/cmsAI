"""
OpenAI helper – generuje artykuł oraz obraz hero.

Kompatybilny z openai‑python ≥ 1.0.
"""

from datetime import datetime
import json
import base64
from typing import TypedDict

from openai import OpenAI, OpenAIError
from fastapi import HTTPException

from core.settings import settings


# ──────────────────────────────────────────────
client = OpenAI(api_key=settings.openai_api_key)


class ArticleJSON(TypedDict):
    title: str
    content: str
    meta_description: str
    image_prompt: str


# ─────────── helpers ───────────
def _strip_md(txt: str) -> str:
    """Usuń ```json … ``` z odpowiedzi modelu, jeśli je dodał."""
    txt = txt.strip()
    if txt.startswith("```"):
        txt = txt.strip("`\n ")
        if txt.lower().startswith("json"):
            txt = txt[4:].strip()
        if txt.endswith("```"):
            txt = txt[: txt.rfind("```")].strip()
    return txt


# ─────────── API ───────────
def generate_article(topic: str) -> ArticleJSON:
    """
    Zwraca dict:
    {title, content, meta_description, image_prompt}
    """
    sys_msg = "You are an expert blog writer."
    usr_msg = (
        f'Write a detailed article about "{topic}". '
        "Return JSON with keys: title, content (min 800 words), "
        "meta_description (≤155 chars), image_prompt."
    )

    try:
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": usr_msg},
            ],
            temperature=0.7,
        )
    except OpenAIError as e:
        raise HTTPException(502, f"OpenAI API error: {e}")

    raw = resp.choices[0].message.content
    try:
        data: ArticleJSON = json.loads(_strip_md(raw))
    except json.JSONDecodeError:
        raise HTTPException(502, "OpenAI response parsing failed")
    return data


def generate_image(prompt: str):
    """
    Zwraca (bytes, mime_type, ext)
    """
    if not settings.openai_api_key:
        raise HTTPException(503, "OpenAI API key not configured")

    try:
        img_resp = client.images.generate(
            prompt=prompt,
            n=1,
            size=settings.openai_image_size,
            response_format="b64_json",
        )
    except OpenAIError as e:
        raise HTTPException(502, f"OpenAI image generation failed: {e}")

    b64_data = img_resp.data[0].b64_json
    img_bytes = base64.b64decode(b64_data)

    if img_bytes.startswith(b"\x89PNG"):
        return img_bytes, "image/png", "png"
    if img_bytes.startswith(b"\xff\xd8"):
        return img_bytes, "image/jpeg", "jpg"
    return img_bytes, "application/octet-stream", "bin"
