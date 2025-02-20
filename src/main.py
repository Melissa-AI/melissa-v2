from stt import stt
from tts import tts
import json

# Load the profile.json file
with open("profile.json") as f:
	profile = json.load(f)

name = profile["name"]

tts("Hello " + name + ", I am Melissa. How can I help you?")

userInput = stt()
print(userInput)

tts("You said: " + userInput)