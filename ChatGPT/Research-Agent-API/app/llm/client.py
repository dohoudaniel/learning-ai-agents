from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_fixed

from app.core.config import settings
from app.core.logger import logger
from app.tools.registry import registry

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class LLMClient:

    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def decide(self, messages):

        logger.info("Gemini deciding next action")

        function_declarations = [
            types.FunctionDeclaration(
                name=tool.schema()["name"],
                description=tool.schema()["description"],
                parameters=tool.schema()["parameters"],
            )
            for tool in registry.tools.values()
        ]

        response = client.models.generate_content(
            model=settings.MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction="""
                You are an AI agent.

                Rules:
                - Use tools whenever needed
                - Continue until the task is complete
                - Do not stop early
                - Use calculator for ALL math
                """,
                tools=[
                    types.Tool(
                        function_declarations=function_declarations
                    )
                ],
                temperature=0,
            ),
        )

        logger.info(f"RAW RESPONSE: {response}")
        logger.info(f"FUNCTION CALLS: {response.function_calls}")
        logger.info(f"FULL RESPONSE: {response}")

        # TOOL CALL
        if response.function_calls:

            fn = response.function_calls[0]

            return {
                "type": "tool_call",
                "tool": fn.name,
                "args": dict(fn.args),
            }

        # FINAL RESPONSE
        return {
            "type": "final",
            "content": response.text,
        }