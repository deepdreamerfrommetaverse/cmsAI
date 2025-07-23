import json
import base64
import openai
from fastapi import HTTPException

from core.settings import settings

# Configure OpenAI API key
openai.api_key = settings.openai_api_key

def generate_article(topic: str) -> dict:
    """Use OpenAI ChatCompletion to generate an article (title, content, meta, image prompt) for the given topic."""
    # System and user instructions for the AI
    system_prompt = "You are an expert blog writer."
    user_prompt = (
        f"Write a detailed article about \"{topic}\". The article should be at least 800 words long, well-structured with headings and paragraphs, and may include lists if appropriate.\n\n"
        "Also provide:\n"
        "- A suitable title for the article.\n"
        "- A concise SEO meta description (max 155 characters).\n"
        "- A creative prompt for an image that would serve as a good illustration (hero image) for the article.\n\n"
        "Output all results in JSON format with keys: title, content, meta_description, image_prompt. Do NOT include any text outside the JSON."
    )
    try:
        response = openai.ChatCompletion.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
    except Exception as e:
        # Catch any OpenAI API errors
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(e)}")
    # Extract and parse the assistant's JSON response
    content = response.choices[0].message.content.strip()
    # Remove any markdown formatting (e.g., ```json blocks)
    if content.startswith("```"):
        content = content.strip("`\n ")
        if content.lower().startswith("json"):
            content = content[4:].strip()
        if content.endswith("```"):
            content = content[:content.rfind("```")].strip()
    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        # If JSON parsing fails
        raise HTTPException(status_code=502, detail="OpenAI response parsing failed")
    return result

def generate_image(prompt: str):
    """Generate an image using OpenAI's DALL-E for the given prompt. Returns (bytes, mime_type, extension)."""
    if not settings.openai_api_key:
        raise HTTPException(status_code=503, detail="OpenAI API key not configured")
    try:
        response = openai.Image.create(prompt=prompt, n=1, size=settings.openai_image_size, response_format="b64_json")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI image generation failed: {str(e)}")
    b64_data = response["data"][0]["b64_json"]
    image_bytes = base64.b64decode(b64_data)
    # Determine image format
    if image_bytes[:4] == b'\x89PNG':
        content_type = "image/png"
        ext = "png"
    elif image_bytes[:2] == b'\xff\xd8':
        content_type = "image/jpeg"
        ext = "jpg"
    else:
        content_type = "image/png"
        ext = "png"
    return image_bytes, content_type, ext
