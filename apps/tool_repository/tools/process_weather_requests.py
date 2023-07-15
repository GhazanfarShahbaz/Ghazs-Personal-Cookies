"""
file_name = process_weather_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to process weather requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
-   Added timeout to get weather request.
"""

from os import environ

from requests import get


def get_weather() -> dict:
    """
    Retrieves weather information from an API.

    This function retrieves weather information from an API using the OpenWeatherMap API.
    The function uses environment variables to retrieve the API key, ZIP code, and country 
    code. 
    The function then sends a request to the OpenWeatherMap API to retrieve the weather 
    information for the specified location and returns it as a dictionary.

    Returns:
        A dictionary containing the weather information for the specified location.
    """

    api_key: str = environ["WEATHER_API_KEY"]
    weather_zip_code: str = environ["WEATHER_ZIP_CODE"]
    weather_country: str = environ["WEATHER_COUNTRY"]

    return get(
        f"https://api.openweathermap.org/data/2.5/weather?zip={weather_zip_code},{weather_country}&appid={api_key}", # pylint: disable=line-too-long
        timeout=10
    ).json()
