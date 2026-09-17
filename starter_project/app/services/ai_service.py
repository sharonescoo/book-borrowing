from google import genai

from app.core.config import settings


async def generate_text(prompt: str) -> str:
    if not settings.gemini_api_key or settings.gemini_api_key.startswith(("PASTE_", "replace-", "your-")):
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(api_key=settings.gemini_api_key)
    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )
    return response.text or ""
