import requests
from dotenv import load_dotenv
from os import environ

def get_weather() -> dict:
    api_key: str = environ["WEATHER_API_KEY"]
    weather_zip_code: str = environ["WEATHER_ZIP_CODE"]
    weather_country: str = environ["WEATHER_COUNTRY"]

    return requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={weather_zip_code},{weather_country}&appid={api_key}").json()