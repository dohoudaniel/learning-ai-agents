# app/llm/client.py

import json

from google import genai
from google.genai import types

from app.core.config import settings
from app.core.logger import logger
from app.tools.registry import registry

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class LLMClient:

    def decide(self, user_input: str):

        logger.info("Gemini deciding next action")

        tools = []

        for tool in registry.tools.values():
            schema = tool.schema()

            tools.append(
                types.FunctionDeclaration(
                    name=schema["name"],
                    description=schema["description"],
                    parameters=schema["parameters"]
                )
            )

        response = client.models.generate_content(
            model=settings.MODEL,
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are an AI agent. "
                    "Use tools when necessary."
                ),
                tools=[types.Tool(function_declarations=tools)],
                temperature=0
            )
        )

        candidate = response.candidates[0]
        content = candidate.content.parts[0]

        # TOOL CALL
        if hasattr(content, "function_call") and content.function_call:

            return {
                "type": "tool_call",
                "tool": content.function_call.name,
                "args": dict(content.function_call.args)
            }

        # FINAL RESPONSE
        return {
            "type": "final",
            "content": content.text
        }