import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather() -> dict:
    api_key: str = os.environ["WEATHER_API_KEY"]
    weather_zip_code: str = os.environ["WEATHER_ZIP_CODE"]
    weather_country: str = os.environ["WEATHER_COUNTRY"]

    return requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={weather_zip_code},{weather_country}&appid={api_key}").json()