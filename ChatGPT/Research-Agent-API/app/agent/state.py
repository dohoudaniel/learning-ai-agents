from typing import List
from google.genai import types


class AgentState:

    def __init__(self):
        self.messages: List[types.Content] = []
        self.steps = 0

    def add_user_message(self, content: str):

        self.messages.append(
            types.Content(
                role="user",
                parts=[types.Part(text=content)]
            )
        )

    def add_model_message(self, content: str):

        self.messages.append(
            types.Content(
                role="model",
                parts=[types.Part(text=content)]
            )
        )

    def add_tool_message(self, tool_name: str, result):

        self.messages.append(
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=f"Tool '{tool_name}' returned: {result}"
                    )
                ]
            )
        )