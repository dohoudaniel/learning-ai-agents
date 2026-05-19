from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.llm.client import LLMClient

router = APIRouter()
llm = LLMClient()


class AnalyzeRequest(BaseModel):
    text: str


@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        return llm.analyze(req.text)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process request")