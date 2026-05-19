from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.llm.client import LLMClient
from app.services.agent_service import AgentService

router = APIRouter()
llm = LLMClient()
agent = AgentService()


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


class AgentRequest(BaseModel):
    text: str

@router.post("/agent")
def agent_route(req: AgentRequest):
    try:
        return agent.run_once(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))