"""
file_name = process_weather_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/19/2023
Description: A module used to process weather requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
-   Added timeout to get weather request.
07/19/2023
-   Added caching to get weather.
"""

from os import environ

from requests import get


from apps.tool_repository.tools.redis_utils import RedisClient

def cache_weather_data(response: dict) -> None:
    """
    Caches the weather data for 5 minutes.

    Args:
        response (dict): The weather data to be cached.
    """

    with RedisClient() as client:
        client.save("weather_data", response, 5)


def get_cached_weather() -> dict:
    """
    Checks and returns cached weather data from redis.

    Returns:
        dict: Can be empty signifying no cached data or can be full of data
    """

    response: dict = {}

    with RedisClient() as client:
        try:
            response = client.get("weather_data")
        except KeyError as exception:
            print("Weather data may have been expired", exception)

    return response


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

    response: dict | None = get_cached_weather()

    if not response:
        response = get(
            f"https://api.openweathermap.org/data/2.5/weather?zip={weather_zip_code},{weather_country}&appid={api_key}", # pylint: disable=line-too-long
            timeout=10
        ).json()

        cache_weather_data(response)

    return response
