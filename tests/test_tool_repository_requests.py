from firebase_admin import firestore
import logging
from apps.tool_repository.endpoints import get_login, validate_user
from apps.tool_repository.endpoints import app
import apps
import json
import pytest
import os
import sys

ROOT_DIRECTORY: str = "/home/ghaz/flask_gateway/"
sys.path.append(ROOT_DIRECTORY)


db = firestore.client()
users_ref = db.collection(os.environ["FIRESTORE_SERVER"])
credentials = users_ref.document(os.environ["FIRESTORE_DOC_ID"]).get().to_dict()

def test_get_login_one():
    response = get_login(False)
    assert response is None


def test_get_login_two():
    login_allow = users_ref.document('allow')

    login_allow.update({
        u'allow': True
    })

    response = get_login(False)

    assert response is not None
    assert "username" in response
    assert type(response["username"]) is str
    assert "password" in response
    assert type(response["password"]) is str


def test_get_login_three():
    response = get_login(True)

    assert response is not None
    assert "username" in response
    assert type(response["username"]) is str
    assert "password" in response
    assert type(response["password"]) is str


def test_validate_user():
    login_allow = users_ref.document('allow')

    login_allow.update({
        u'allow': True
    })
    response = validate_user(credentials["username"], credentials["password"])

    assert response is True


def test_validate_get_help():
    login_allow = users_ref.document('allow')

    login_allow.update({
        u'allow': True
    })

    response = app.test_client().post(
        "/getHelp",
        json={
            "username": credentials['username'],
            "password": credentials['password'],
            "command": "getTranslation"
        }
    )

    response_dict = json.loads(response.data.decode('UTF-8'))

    assert response.status_code == 200
    assert response_dict == {
        "Description": "Translates a piece of text based on a series of parameters",
        "RequestTemplate": {
            "username": "your username",
            "password": "your password",
            "translationForm": {
                "text": "a required parameter, string type",
                "source": "an optional parameter, string type",
                "target": "an optional parameter, string type"
            }
        }
    }


def test_validate_get_current_weather():
    login_allow = users_ref.document('allow')

    login_allow.update({
        u'allow': True
    })

    response = app.test_client().post(
        "/getCurrentWeather",
        json={
            "username": credentials['username'],
            "password": credentials['password'],
        }
    )

    response_dict = json.loads(response.data.decode('UTF-8'))

    assert response.status_code == 200
    assert "weather" in response_dict
