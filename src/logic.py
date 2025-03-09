from ollama import chat, ChatResponse
from plugins.getDateAndTime import get_date_time

def logic(messages):
    """
    Process messages and handle tool calls
    Returns appropriate response from the LLM.
    """
    available_functions = {
        'get_date_time': get_date_time,
    }

    # Define tool schema more explicitly
    tools = [{
        "type": "function",
        "function": {
            "name": "get_date_time",
            "description": "Get the current date or time based on user query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's query about date or time"
                    }
                },
                "required": ["query"]
            }
        }
    }]

    # Get initial response
    response = chat(model='llama3.2', messages=messages, tools=tools)

    # If no tool calls, return the response directly
    if not response.message.tool_calls:
        print('No tool calls detected')
        return response.message

    # Handle tool calls if present
    tool_outputs = []
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            output = function_to_call(**tool.function.arguments)
            if output:
                tool_outputs.append({
                    'role': 'tool',
                    'content': output,
                    'name': tool.function.name
                })

    if tool_outputs:
        messages.extend(tool_outputs)

        final_response = chat('llama3.2', messages=messages)
        return final_response.message

    return response.message
