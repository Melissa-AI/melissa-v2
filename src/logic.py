from ollama import chat, ChatResponse

def logic(message):
    """
    This function takes a user message as an argument and passes it to the LLM.
    The response from the LLM is then sent to the tts function.
    """
    response = chat(model='llama3.2', messages=[
        {
            'role': 'system',
            'content': 'You are a helpful virtual assistant named Melissa. Give concise replies.',
        },
        {
            'role': 'user',
            'content': message or 'hi',
        },
    ])
    return response.message.content
