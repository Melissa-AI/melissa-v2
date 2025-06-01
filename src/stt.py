import sys
import os
from vosk import Model, KaldiRecognizer, SetLogLevel
import pyaudio
import json
import time

def stt():
	SetLogLevel(-1)  # Disable Vosk logging
	# Load the Vosk model
	model = Model("model")
	recognizer = KaldiRecognizer(model, 16000)

	# Start audio stream
	mic = pyaudio.PyAudio()
	stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
	stream.start_stream()

	MAX_SILENCE_TIME = 2.0  # Maximum time to wait for speech
	INITIAL_TIMEOUT = 5.0   # Longer initial timeout to wait for speech
	last_speech_time = time.time()
	has_speech = False
	resultText = ""
	print("Listening...")

	while True:
		data = stream.read(4096, exception_on_overflow=False)

		if recognizer.AcceptWaveform(data):
			result = json.loads(recognizer.Result())
			if result['text'].strip():
				has_speech = True
				last_speech_time = time.time()
				resultText += f"{result['text']} "
				print(f"Recognized: {resultText}")
		else:
			# Check partial results for ongoing speech
			partial = json.loads(recognizer.PartialResult())
			if partial.get('partial', '').strip():
				has_speech = True
				last_speech_time = time.time()

		current_time = time.time()
		# Check if we've had speech and now there's a pause
		if has_speech and (current_time - last_speech_time) > MAX_SILENCE_TIME:
			print("Speech completed, stopping...")
			break

		# Use longer timeout for initial speech detection
		if not has_speech and (current_time - last_speech_time) > INITIAL_TIMEOUT:
			print("No speech detected, stopping...")
			return None

	# Clean up
	stream.stop_stream()
	stream.close()
	mic.terminate()

	return resultText