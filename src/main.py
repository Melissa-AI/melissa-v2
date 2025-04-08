from stt import stt
from tts import tts
from logic import logic
import json

# Load the profile.json file
with open("profile.json") as f:
	profile = json.load(f)

name = profile["name"]

messages = [
    {
        'role': 'system',
        'content':
        '''
        You are an AI assistant that MUST use the provided tools when NECESSARY.

AVAILABLE TOOLS:
1. get_date_time: Get the current date or time based on user query
   - Use this tool whenever a user asks about the current time or date
2. get_weather_info: Get weather information for a specific city
   - Use this tool whenever a user asks about weather in a specific city
3. get_hackernews_info: Get top stories from HackerNews
   - Use this tool whenever a user asks about HackerNews stories

For non-tool questions, respond normally. For date/time questions, you MUST use the tool.

EXAMPLES:
User: "What time is it?"
Assistant: The current time is 12:34

User: "Tell me today's date"
Assistant: Today's date is 17 Dec, 2025

User: "What are the top stories on HackerNews?"
Assistant: Here are the top stories from HackerNews:
1. [Story Title]
   Author: [Author Name]
2. [Story Title]
   Author: [Author Name]
...

User: "Hello, my name is John"
Assistant: Hello, how can I help you today?
        '''
    },
]

# Initial greeting
messages.append({
    'role': 'user',
    'content': f"Hello, my name is {name}",
})

# Get and speak initial response
llm_response = logic(messages)

tts(llm_response.content)

while True:
    try:
        userInput = stt()
        if not userInput:
            print("No input detected. Ending conversation...")
            break

        # Add previous assistant response and new user input
        messages.append({
            'role': 'assistant',
            'content': llm_response.content
        })
        messages.append({
            'role': 'user',
            'content': userInput,
        })

        # Get and speak new response
        llm_response = logic(messages)
        tts(llm_response.content)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        break