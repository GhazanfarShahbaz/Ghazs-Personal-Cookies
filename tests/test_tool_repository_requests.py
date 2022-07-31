import sys

ROOT_DIRECTORY: str = "/home/ghaz/flask_gateway/"
sys.path.append(ROOT_DIRECTORY)

from os import environ
from firebase_admin import credentials, firestore

import json
import pytest

from generate_env import load_environment
load_environment()

from apps.tool_repository.endpoints import app
from apps.tool_repository.endpoints import get_login, validate_user


# print(environ)


db = firestore.client()
users_ref = db.collection(environ["FIRESTORE_SERVER"])
credentials = users_ref.document(environ["FIRESTORE_DOC_ID"]).get().to_dict()

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


def test_validate_get_help_one():
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
    
def test_validate_get_help_two():
    login_allow = users_ref.document('allow')

    login_allow.update({
        u'allow': True
    })

    response = app.test_client().post(
        "/getHelp",
        json={
            "username": credentials['username'],
            "password": credentials['password'],
            "command": "somethingFake"
        }
    )

    response_dict = json.loads(response.data.decode('UTF-8'))

    assert response.status_code == 200
    assert response_dict == {}


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


def test_create_event():
    login_allow = users_ref.document('allow')

    login_allow.update({
        u'allow': True
    })

    response = app.test_client().post(
        "/createEvent",
        json={
            "username": credentials['username'],
            "password": credentials['password'],
            "eventForm": {
                "StartDate": "08/27/2001 12:00 AM",
                "EndDate": "08/27/2001 12:01 AM",
                "Name": "TEST",
                "Location": "TEST",
                "Type": "TEST",
                "Description": "TEST",
                "ReccuranceType": ""
            }
        }
    )    
    
    assert response.status_code == 200
    assert response.data == b"Success"


def test_get_event():
    login_allow = users_ref.document('allow')

    login_allow.update({
        u'allow': True
    })

    response = app.test_client().post(
        "/getEvent",
        json={
            "username": credentials['username'],
            "password": credentials['password'],
            "filterForm": {
                "Name": "TEST",
            }
        }
    )   
    
    response_dict = json.loads(response.data.decode('UTF-8'))
 
    print(response_dict)
    assert response.status_code == 200
    assert response_dict != {}


def test_delete_event():
    login_allow = users_ref.document('allow')

    login_allow.update({
        u'allow': True
    })

    response = app.test_client().post(
        "/deleteEvent",
        json={
            "username": credentials['username'],
            "password": credentials['password'],
            "deleteForm": {
                "Name": "TEST",
            }
        }
    )    
    
    assert response.status_code == 200
    assert response.data == b"Success"


# def test_upload_file():
#     login_allow = users_ref.document('allow')

#     login_allow.update({
#         u'allow': True
#     })
    
#     base_request = {
#         "username": credentials["username"],
#         "password": credentials["password"]
#     }
    
    
#     response = app.test_client().post(
#         "uploadFile",
#         data={
#             "file": open("/home/ghaz/flask_gateway/tests/test_file.txt", "rb"),
#             "json": (None, json.dumps(base_request), 'application/json')
#         }
#     )  
    
    # response_dict = json.loads(response.data.decode('UTF-8'))
    
    # assert response.status_code == 200
    # assert response.data != "Invalid"
    # assert response_dict == {"status": "success"}
    
    