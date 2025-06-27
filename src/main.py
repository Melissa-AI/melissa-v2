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
        You are an AI assistant designed to be helpful and efficient. You have tools to assist with specific tasks.

        **TOOL USAGE GUIDELINES:**
        *   If a user asks a question that your tool is designed to answer, you MUST use the tool.
        *   You MUST use your available tools whenever a user's request directly and clearly maps to a tool's capability.

        AVAILABLE TOOLS:
        1.  **get_current_date:** Get the current date.
            *   **Instruction:** You MUST use this tool for ANY request about the current date (e.g., "What's today's date?"). Do not attempt to answer date questions from your own knowledge.

        2.  **get_current_time:** Get the current time.
            *   **Instruction:** You MUST use this tool for ANY request about the current time (e.g., "What time is it?"). Do not attempt to answer time questions from your own knowledge.

        3. **get_hackernews_info:** Get top stories from HackerNews.
			*   **Instruction:** You MUST use this tool for ANY request about the top stories on HackerNews (e.g., "What are the top stories on HackerNews?"). Do not attempt to answer HackerNews questions from your own knowledge.

        For all other questions not covered by your tools, respond naturally.

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

        User: "Hello, my name is John"
        Assistant: Hello John, how can I help you today?
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