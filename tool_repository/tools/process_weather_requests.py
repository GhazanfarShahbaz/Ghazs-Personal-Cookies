import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather() -> dict:
    api_key: str = os.environ["WEATHER_API_KEY"]
    weather_zip_code: str = os.environ["WEATHER_ZIP_CODE"]
    weather_country: str = os.environ["WEATHER_COUNTRY"]

    return requests.get("https://api.openweathermap.org/data/2.5/weather?zip=11230,us&appid=8d96edab6c640b9d6b6f97ce1bad77f6").json()