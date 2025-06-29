import re
import re
from ollama import chat, ChatResponse
from plugins.getDateAndTime import get_current_date, get_current_time
from plugins.getHackerNews import get_hackernews_info
from plugins.getWeather import get_weather_info


def logic(messages):
    """
    Process messages and handle tool calls
    Returns appropriate response from the LLM.
    """
    available_functions = {
        'get_current_date': get_current_date,
        'get_current_time': get_current_time,
        'get_hackernews_info': get_hackernews_info,
        'get_weather_info': get_weather_info,
    }

    # Define tool schema more explicitly
    tools = [{
        "type": "function",
        "function": {
                "name": "get_current_date",
            "description": "Get today's date",
            "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
            }
        }
    }, {
        "type": "function",
        "function": {
                "name": "get_current_time",
            "description": "Always get the current time of the day",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "get_hackernews_info",
            "description": "Get top stories from HackerNews",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's query about HackerNews stories"
                    }
                },
                "required": ["query"]
            }
        }
    },
        {
        "type": "function",
        "function": {
            "name": "get_weather_info",
            "description": "Always get weather information for a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's query about weather including city name"
                    }
                },
                "required": ["query"]
            }
        }
    }]

    # Get initial response
    response = chat(model='qwen3:1.7b', messages=messages, tools=tools)

    # Clean the response content
    if 'content' in response.message and response.message['content']:
        response.message['content'] = re.sub(
            r'<think>.*?</think>', '', response.message['content'], flags=re.DOTALL).strip()

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
        # Add the assistant's tool call message
        messages.append({
            'role': 'assistant',
            'content': response.message.content or '',
            'tool_calls': response.message.tool_calls
        })
        # Add the tool outputs
        messages.extend(tool_outputs)

        final_response = chat('qwen3:1.7b', messages=messages, tools=tools)

        # Clean the final response content
        if 'content' in final_response.message and final_response.message['content']:
            final_response.message['content'] = re.sub(
                r'<think>.*?</think>', '', final_response.message['content'], flags=re.DOTALL).strip()
        return final_response.message

    return response.message
