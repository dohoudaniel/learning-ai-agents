from pydantic import BaseModel
from typing import List, Literal


class AnalysisResponse(BaseModel):
    summary: str
    keywords: List[str]
    sentiment: Literal["positive", "negative", "neutral"]