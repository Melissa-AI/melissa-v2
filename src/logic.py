import re
from ollama import chat, ChatResponse

def logic(message):
    """
    This function takes a user message as an argument and passes it to the LLM.
    The response from the LLM is then sent to the tts function.
    """
    response = chat(model='qwen3:1.7b', messages=[
        {
            'role': 'system',
            'content': 'You are a helpful virtual assistant named Melissa. Give concise replies.',
        },
        {
            'role': 'user',
            'content': message or 'hi',
        },
    ])

	# Clean the response content
    if 'content' in response.message and response.message['content']:
        response.message['content'] = re.sub(r'<think>.*?</think>', '', response.message['content'], flags=re.DOTALL).strip()

    return response.message.content
