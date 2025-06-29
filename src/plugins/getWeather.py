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


def fetch_weather_data(city: str) -> Optional[Dict]:
    """Fetch weather data for given city from OpenWeatherMap API"""
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # For Celsius
        }
        url = f"{BASE_URL}?{parse.urlencode(params)}"
        with request.urlopen(url) as response:
            return json.loads(response.read())
    except (error.URLError, json.JSONDecodeError):
        return None


def get_weather_info(query: str) -> str:
    """Process user query and return weather information"""
    # Extract city name from query
    words = query.lower().split()
    try:
        city_index = words.index('in') + 1
        city = ' '.join(words[city_index:])
    except ValueError:
        return "Please specify a city using 'in'. For example: 'weather in London'"

    if not city:
        return "Please specify a city name"

    weather_data = fetch_weather_data(city)
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
