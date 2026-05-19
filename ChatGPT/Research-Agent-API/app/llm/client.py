import json
from tenacity import retry, stop_after_attempt, wait_fixed
from google import genai

from app.core.config import settings
from app.core.logger import logger
from app.llm.prompts import SYSTEM_PROMPT
from app.schemas.analysis import AnalysisResponse

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class LLMClient:
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def analyze(self, text: str) -> AnalysisResponse:
        logger.info("Sending structured analysis request to Gemini")

        response = client.models.generate_content(
            model=settings.MODEL,
            contents=text,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "response_format": {
                    "text": {
                        "mime_type": "application/json",
                        "schema": AnalysisResponse.model_json_schema(),
                    }
                },
            },
        )

        logger.info("Raw Gemini output: %s", response.text)
        return AnalysisResponse.model_validate_json(response.text)