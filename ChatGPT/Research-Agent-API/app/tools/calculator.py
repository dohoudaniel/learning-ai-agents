# app/tools/calculator.py
import ast
import operator
from pydantic import BaseModel, Field
from app.tools.base import Tool

class CalculatorArgs(BaseModel):
    expression: str = Field(..., min_length=1, max_length=200)

class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluate basic arithmetic expressions such as 25 * 4 or (10 + 2) / 3."

    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A basic arithmetic expression."
                    }
                },
                "required": ["expression"],
            },
        }

    def execute(self, **kwargs):
        args = CalculatorArgs(**kwargs)
        return self.safe_eval(args.expression)

    def safe_eval(self, expr: str):
        allowed_ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
        }

        def eval_node(node):
            if isinstance(node, ast.BinOp):
                op = type(node.op)
                if op not in allowed_ops:
                    raise ValueError("Unsupported operator")
                return allowed_ops[op](eval_node(node.left), eval_node(node.right))

            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Unsupported expression")

        tree = ast.parse(expr, mode="eval")
        return eval_node(tree.body)