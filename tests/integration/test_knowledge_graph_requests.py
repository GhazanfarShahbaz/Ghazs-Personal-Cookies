import pytest

from json import loads

from apps.knowledge_graph.app import app  # pylint: disable=import-error


def test_get_base_endpoint():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert loads(response.data.decode("UTF-8")) is not None
