from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.deps import get_current_user
from app.services.ai_service import generate_text

router = APIRouter(prefix="/api/ai", tags=["ai"])


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)


class GenerateResponse(BaseModel):
    text: str


@router.post("/generate", response_model=GenerateResponse)
async def generate(payload: GenerateRequest, _=Depends(get_current_user)):
    try:
        text = await generate_text(payload.prompt)
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Gemini request failed") from exc
    return GenerateResponse(text=text)
