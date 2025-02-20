from stt import stt
from tts import tts
# import the logic function from logic.py
from logic import logic
import json

# Load the profile.json file
with open("profile.json") as f:
	profile = json.load(f)

name = profile["name"]

# Pass the name to the logic function
llm_response = logic(f"Hello, my name is {name}")

# Pass the response from the logic function to the tts function
tts(llm_response)

while True:
	try:
		# Get user input via voice
		userInput = stt()

		# Check if user input is empty or None
		if not userInput:
			print("No input detected. Ending conversation...")
			break

		# Process user input and respond
		tts(logic(userInput))

	except Exception as e:
		print(f"An error occurred: {str(e)}")
		break