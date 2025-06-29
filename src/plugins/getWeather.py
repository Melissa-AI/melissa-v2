import json
from urllib import request, parse, error
from typing import Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# You'll need to sign up at OpenWeatherMap and get an API key
# Get API key from environment variable
API_KEY = os.environ.get('WEATHER_API_KEY')

if not API_KEY:
    raise ValueError("API key for OpenWeatherMap not found")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> str:
    """Fetch weather data for given city from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # For Celsius
        }
        url = f"{BASE_URL}?{parse.urlencode(params)}"
        with request.urlopen(url) as response:
            weather_data = json.loads(response.read())
            if not weather_data:
                return f"Sorry, I couldn't fetch weather information for {city}"

            temp = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            humidity = weather_data['main']['humidity']
            min_temp = weather_data['main']['temp_min']
            max_temp = weather_data['main']['temp_max']
            feels_like = weather_data['main']['feels_like']

            return f"Current weather in {city.title()}:\n" \
                f"Temperature: {temp}°C\n" \
                f"Conditions: {description.capitalize()}\n" \
                f"Humidity: {humidity}%"\
                f"Min Temp: {min_temp}°C\n" \
                f"Max Temp: {max_temp}°C\n" \
                f"Feels Like: {feels_like}°C"

    except (error.URLError, json.JSONDecodeError):
        return None
