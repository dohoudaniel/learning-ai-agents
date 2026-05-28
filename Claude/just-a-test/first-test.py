import anthropic
import json

client = anthropic.Anthropic()

# Define tools
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
]

def get_weather(city: str) -> str:
    # Mock — replace with real API
    return f"Weather in {city}: 28°C, sunny"

def execute_tool(name: str, inputs: dict) -> str:
    if name == "get_weather":
        return get_weather(**inputs)
    raise ValueError(f"Unknown tool: {name}")

def run_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]
    
    while True:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Check stop reason
        if response.stop_reason == "end_turn":
            # Extract final text
            for block in response.content:
                if block.type == "text":
                    return block.text
        
        if response.stop_reason == "tool_use":
            # Append assistant message
            messages.append({"role": "assistant", "content": response.content})
            
            # Execute each tool call
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            # Append tool results and continue loop
            messages.append({"role": "user", "content": tool_results})

# Run it
print(run_agent("What's the weather in Lagos and should I go outside?"))