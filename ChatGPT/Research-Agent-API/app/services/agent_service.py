# app/services/agent_service.py
from app.core.logger import logger
from app.llm.client import LLMClient
from app.tools.registry import registry

class AgentService:
    def __init__(self):
        self.llm = LLMClient()

    def run_once(self, user_input: str):
        decision = self.llm.decide(user_input)

        if decision["type"] == "final":
            return {"result": decision["content"]}

        tool = registry.get(decision["tool"])
        if not tool:
            raise ValueError(f"Unknown tool: {decision['tool']}")

        logger.info("Tool selected: %s", decision["tool"])
        logger.info("Tool args: %s", decision["args"])

        result = tool.execute(**decision["args"])

        return {
            "tool_used": decision["tool"],
            "tool_result": result,
        }