from apps.tool_repository.tools.process_weather_requests import (
    get_weather,
)  # pylint: disable=import-error, useless-option-value, nknown-option-value, unrecognized-option

import pytest


def test_get_weather():
    weather_data = get_weather()

    assert type(weather_data) is dict
    assert weather_data != {}
