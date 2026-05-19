from app.agent.state import AgentState
from app.core.logger import logger
from app.llm.client import LLMClient
from app.tools.registry import registry


class AgentLoop:

    def __init__(self):
        self.llm = LLMClient()

    def run(self, user_input: str):

        state = AgentState()

        state.add_user_message(user_input)

        MAX_STEPS = 10

        while state.steps < MAX_STEPS:

            logger.info(f"STEP: {state.steps}")

            decision = self.llm.decide(state.messages)

            # FINAL ANSWER
            if decision["type"] == "final":

                logger.info("Agent completed task")

                return {
                    "steps": state.steps,
                    "messages": state.messages,
                    "final_answer": decision["content"]
                }

            # TOOL EXECUTION
            if decision["type"] == "tool_call":

                tool_name = decision["tool"]

                logger.info(f"Tool selected: {tool_name}")

                tool = registry.get(tool_name)

                if not tool:
                    raise ValueError(f"Unknown tool: {tool_name}")

                result = tool.execute(**decision["args"])

                logger.info(f"Tool result: {result}")

                state.add_tool_message(tool_name, result)

            state.steps += 1

        raise Exception("Max steps exceeded")