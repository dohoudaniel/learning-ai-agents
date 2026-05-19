from app.tools.calculator import CalculatorTool

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def get(self, name):
        return self.tools.get(name)

    def get_schemas(self):
        return [tool.schema() for tool in self.tools.values()]

registry = ToolRegistry()
registry.register(CalculatorTool())