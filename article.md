In the previous chapter, you learned about APIs and created a plugin that fetches information from an API. In this chapter, you will create a plugin that will use a weather API to fetch the current weather in the city you specify. You can use this plugin to decide if you need a jacket for the cold winds, or an umbrella for the showers.
To get the current weather information, you will use the OpenWeather (https://openweathermap.org/) API. Unlike the Hacker News API, this API needs authentication. Without the authentication, you can’t make successful API calls to the OpenWeather APIs. OpenWeather uses an API key to allow you to make authenticated requests.
Get OpenWeather API Key
There are different ways an API can implement authentication, API key is one of the most popular approaches. An API key is a uniquely generated string that you use to call the API. Each user has their own unique API key, and this helps the API provider (OpenWeather in this case) identify the user making the API call. So whenever you use an API key, make sure you don’t share it with anyone. In the later sections, you will learn the best practices to securely use API keys.
OpenWeather provides a bunch of APIs like the Air Pollution API (https://openweathermap.org/api/air-pollution), Geocoding API (https://openweathermap.org/api/geocoding-api), Current Weather API (https://openweathermap.org/current) and more. Since you want Melissa to tell you the current weather, you will use the Current Weather API. At the time of writing this book, this API is available in the free tier, and you don’t need to pay or share your credit card information.
To get started with the API, you need an OpenWeather account. If you don’t have an account, you can sign-up for a new account on their website (https://home.openweathermap.org/users/sign_up). On the sign-up page, you might be asked to enter a username, email address, and a password. Once the account is created successfully, you will get a verification email. Make sure you follow the instructions in the email to verify your account.
After verification, you will receive another email. This email will contain the API key that you will need in the next steps. So make sure to save it somewhere safe. Do not share this API key with anyone. Someone with access to your API key, can make a request to the API on your behalf.
Let’s test it out! Using cURL from your terminal, you will make a request to the API. Make sure to edit the command to add the name of your city and your API key, to get the current weather for your city.
curl "http://api.openweathermap.org/data/2.5/weather?q=CITY&appid=API_KEY&units=metric"
You should get a similar output.
{"coord":{"lon":13.4105,"lat":52.5244},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"base":"stations","main":{"temp":14.55,"feels_like":13.24,"temp_min":12.83,"temp_max":15.6,"pressure":1022,"humidity":45,"sea_level":1022,"grnd_level":1016},"visibility":10000,"wind":{"speed":0.89,"deg":134,"gust":3.13},"clouds":{"all":7},"dt":1742548685,"sys":{"type":2,"id":2011538,"country":"DE","sunrise":1742533591,"sunset":1742577629},"timezone":3600,"id":2950159,"name":"Berlin","cod":200}%
Create the Weather plugin
You now have access to the API that returns the current weather of your city. You need to create a plugin and provide Melissa the access to this plugin. Once Melissa has access to the weather plugin, you will be able to ask Melissa the current weather!
Create a getWeather.py file inside the plugins directory. Add the below code to get the current weather for a city.
import json
from urllib import request, parse, error
from typing import Dict, Optional

# You'll need to sign up at OpenWeatherMap and get an API key

API_KEY = "YOUR_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city: str) -> Optional[Dict]:
"""Fetch weather data for given city from OpenWeatherMap API"""
try:
params = {
'q': city,
'appid': API_KEY,
'units': 'metric' # For Celsius
}
url = f"{BASE_URL}?{parse.urlencode(params)}"
with request.urlopen(url) as response:
return json.loads(response.read())
except (error.URLError, json.JSONDecodeError):
return None

def get_weather_info(query: str) -> str:
"""Process user query and return weather information""" # Extract city name from query
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

    return f"Current weather in {city.title()}:\n" \
           f"Temperature: {temp}°C\n" \
           f"Conditions: {description.capitalize()}\n" \
           f"Humidity: {humidity}%"

print(get_weather_info("weather in Berlin")) # Test the function with a sample query
The code above imports all the required packages, and defines the API Key and the API endpoint. For now, replace YOUR_API_KEY, with your OpenWeatherMap API key. In the next step, you will learn how to securely store the API key. For testing, you can paste the API key in the code.
You define a fetch_weather_data function that takes the city as the input parameter and makes a call to the OpenWeatherMap API. It uses your API key to make an authenticated request to the API, and returns the weather data.
The get_weather_info takes the users’ input as a query, and extracts the city name. It calls the fetch_weather_data function using the extracted city name, and returns the result in a more readable format.
To test this plugin, execute the getWeather.py file.
python3 src/plugins/getWeather.py
You should get a similar output.
Current weather in Berlin:
Temperature: 10.31°C
Conditions: Clear sky
Humidity: 47%
Melissa, what is the temperature?
You have a Weather Plugin that returns the weather information. However, if you ask Melissa the current weather, the virtual assistant will not be able to give you a correct response. This is because you have not provided this plugin to Melissa, yet.
In the previous chapter, you set up the foundation of the function calling for LLM. To add new tools, you need to make minor changes.
First, update the logic.py file. Import the get_weather_info plugin, and add it to the available_functions and tools list.
from ollama import chat, ChatResponse
from plugins.getDateAndTime import get_date_time
from plugins.getWeather import get_weather_info

def logic(messages):
"""
Process messages and handle tool calls
Returns appropriate response from the LLM.
"""
available_functions = {
'get_date_time': get_date_time,
'get_weather_info': get_weather_info,
}

    # Define tool schema more explicitly
    tools = [{
        "type": "function",
        "function": {
            "name": "get_date_time",
            "description": "Get the current date or time based on user query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's query about date or time"
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
            "description": "Get weather information for a specific city",
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
    response = chat(model='llama3.2', messages=messages, tools=tools)

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
        messages.extend(tool_outputs)

        final_response = chat('llama3.2', messages=messages)
        return final_response.message

    return response.message

Next, update the system prompt in the main.py file. You should add the plugin under the AVAILABLE TOOLS section, and also add an example.
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

For non-tool questions, respond normally. For date/time questions, you MUST use the tool.

EXAMPLES:
User: "What time is it?"
Assistant: The current time is 12:34

User: "Tell me today's date"
Assistant: Today's date is 17 Dec, 2025

User: "What's the weather in London?"
Assistant: Here's the current weather in London:
Conditions: Partly cloudy
Temperature: 12 C
Humidity: 65%

User: "Hello, my name is John"
Assistant: Hello, how can I help you today?
'''
},
]
Lastly, you can remove the print statement in the src/plugins/getWeather.py file that was added to test the plugin. You do not need to call the get_weather_info function inside the getWeather.py anymore.
Start the Ollama server, and execute the main.py file. Ask Melissa the temperature in your city, and you will hear the response from Melissa with the accurate information.
ollama serve
python3 src/main.py
Securely storing API key
Your virtual assistant can make API calls to the Current Weather API and fetch the information. The API uses an API key for a secure call. You have hardcoded the API key in the getWeather.py file, which is not secure. In this section, you will learn about securely storing and using API keys and other credentials.
The best practice to store the API keys and other secret credentials, is to use an environment variable file. You will create a .env file. You will add this file to .gitignore to make sure you don’t accidentally commit this file and leak your credentials. To do this, enter the following commands in your terminal.
touch .env
echo “.env” >> .gitignore
The updated .gitignore file should contain the following content.
venv/
**pycache**/
\*.pyc
.env
The .env file should have the following content. Make sure to replace YOUR_API_KEY with your OpenWeatherMap API key.
WEATHER_API_KEY = YOUR_API_KEY
You will load the API key from the .env file. You will need the dotenv package to load the data from this file. Execute the following command to install the package.
pip install python-dotenv
Using this package you can now securely load the API key in the getWeather.py file. Import the package in the getWeather.py file and update the code to load the API key from the .env file. You should also remove the hardcoded API key from this file since it will now get loaded from the .env file.
import json
from urllib import request, parse, error
from typing import Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()

# You'll need to sign up at OpenWeatherMap and get an API key

API_KEY = os.environ.get('WEATHER_API_KEY') # Get API key from environment variable

if not API_KEY:
raise ValueError("API key for OpenWeatherMap not found")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city: str) -> Optional[Dict]:
"""Fetch weather data for given city from OpenWeatherMap API"""
try:
params = {
'q': city,
'appid': API_KEY,
'units': 'metric' # For Celsius
}
url = f"{BASE_URL}?{parse.urlencode(params)}"
with request.urlopen(url) as response:
return json.loads(response.read())
except (error.URLError, json.JSONDecodeError):
return None

def get_weather_info(query: str) -> str:
"""Process user query and return weather information""" # Extract city name from query
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

    return f"Current weather in {city.title()}:\n" \
           f"Temperature: {temp}°C\n" \
           f"Conditions: {description.capitalize()}\n" \
           f"Humidity: {humidity}%"

Execute the program, and try asking Melissa the temperature in your city. You will notice that Melissa is still able to tell you the correct temperature. The only that is changed is how the API key is accessed. It is now more secure than before.
Exercise
You can now ask Melissa the current weather, and Melissa will use the plugins you created to provide the information. While the information returned by the get_weather_info plugin is good, it can be better. The API provides more information like the minimum temperature, maximum temperature, and feels like temperature (defined as human perception of weather). Update the plugin to return this information as well. You can refer to the Current Weather API documentation (https://openweathermap.org/current) to learn more.

Solution
To return the minimum, maximum, and feels like temperature, you need to update the getWeather.py file. Update the get_weather_info to get these values from the API response.
def get_weather_info(query: str) -> str:
"""Process user query and return weather information""" # Extract city name from query
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

You should also update the system prompt in the main.py file.
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

For non-tool questions, respond normally. For date/time questions, you MUST use the tool.

EXAMPLES:
User: "What time is it?"
Assistant: The current time is 12:34

User: "Tell me today's date"
Assistant: Today's date is 17 Dec, 2025

User: "What's the weather in London?"
Assistant: Here's the current weather in London:
Conditions: Partly cloudy
Temperature: 12 C
Humidity: 65%
Min Temp: 4 C
Max Temp: 14 C
Feels Like: 11 C

User: "Hello, my name is John"
Assistant: Hello, how can I help you today?
'''
},
]
Now when you ask Melissa about the weather, you will get a better result which might help you decide if you need that jacket!
Get the Code
If you are running into issues or want to just get the code, you can find it on the GitHub repository: https://github.com/Melissa-AI/melissa-v2. Clone the repository, and checkout to the chapter-6 branch. You can use the code as is. Just make sure to create and activate a virtual environment and install the packages. You will also need the API key from OpenWeatherMap.
// clone the repo
git remote add origin https://github.com/Melissa-AI/melissa-v2.git
// navigate into the repo
cd melissa-v2
// switch to chapter 6 branch
git checkout chapter-6
// rename .env.copy
mv .env.copy .env
// update the .env file. Replace YOUR_API_KEY with your API key
// create the virtual environment
python3 -m venv venv
// start the virtual environment
source venv/bin/activate
// install packages
pip install -r requirements.txt
Summary
In this chapter, you learned about authenticated APIs and how to interact with them. You created a plugin that fetches the weather information from the internet by calling the Current Weather API from OpenWeatherMap. You then updated the code to provide Melissa access to the plugin you created. Melissa can tell you the correct date, time, and weather!
Now before you head out, you can ask Melissa for weather information that can help you decide if you need an umbrella or not.
You have three plugins now - to get current date and time, get top stories from Hacker News, and get weather information. Let’s create another plugin that will help you create and save notes. You would be able to use this plugin to store the URL of the Hacker News article you are interested in reading later, or add a note for the amazing idea you just had!
