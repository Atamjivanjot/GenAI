import requests
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()


def get_weather(city: str):

    encoded_city = quote(city, safe='')

    url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={encoded_city}&count=1"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return "Unable to fetch location."

    if "results" not in data:
        return "City not found."

    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    name = data["results"][0]["name"]

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&current=temperature_2m,apparent_temperature,"
        f"relative_humidity_2m,wind_speed_10m,"
        f"wind_gusts_10m,weather_code"
        f"&daily=uv_index_max"
    )

    response_weather = requests.get(weather_url)
    data_weather = response_weather.json()

    return {
        "temperature": data_weather["current"]["temperature_2m"],
        "feelsLike": data_weather["current"]["apparent_temperature"],
        "humidity": data_weather["current"]["relative_humidity_2m"],
        "windSpeed": data_weather["current"]["wind_speed_10m"],
        "windGust": data_weather["current"]["wind_gusts_10m"],
        "conditions": get_weather_condition(
            data_weather["current"]["weather_code"]
        ),
        "location": name,
        "uvIndex": data_weather["daily"]["uv_index_max"][0]
    }


def get_weather_condition(code: int) -> str:

    conditions = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        56: 'Light freezing drizzle',
        57: 'Dense freezing drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        66: 'Light freezing rain',
        67: 'Heavy freezing rain',
        71: 'Slight snow fall',
        73: 'Moderate snow fall',
        75: 'Heavy snow fall',
        77: 'Snow grains',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with slight hail',
        99: 'Thunderstorm with heavy hail',
    }

    return conditions.get(code, 'Unknown')