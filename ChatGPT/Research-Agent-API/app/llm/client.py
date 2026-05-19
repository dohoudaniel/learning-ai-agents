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
            contents=f"""
            {SYSTEM_PROMPT}

            Analyze this text:

            {text}
            """
        )

        raw = response.text.strip()

        logger.info(f"RAW RESPONSE:\n{raw}")

        # Remove markdown wrappers if present
        raw = raw.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(raw)

        # Normalize sentiment
        if "sentiment" in parsed:
            parsed["sentiment"] = parsed["sentiment"].lower()

        return AnalysisResponse(**parsed)