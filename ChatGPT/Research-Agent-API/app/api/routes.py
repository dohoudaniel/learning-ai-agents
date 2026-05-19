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
    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
    )