"""
file_name = weather_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for weather endpoints.
Edit Log:
07/20/2023
-   Moved weather endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint

from apps.tool_repository.tools.process_weather_requests import get_weather

weather_blueprint: Blueprint = Blueprint("weather", __name__)

@weather_blueprint.route("/getCurrentWeather", methods=["POST"])
def get_current_weather():
    """
    Gets the current weather.

    This function gets the current weather using the `get_weather` function.

    Returns:
        A JSON object containing the current weather.

    Raises:
        None.
    """

    return get_weather()
