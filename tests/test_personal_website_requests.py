import os
import sys

ROOT_DIRECTORY: str =  "/home/ghaz/flask_gateway/"
sys.path.append(ROOT_DIRECTORY)

import pytest
import json

import apps
from apps.personal_website.requests import app

def test_gethome():
    response = app.test_client().get("/")
    
    assert response.status_code == 200
    assert response.data.decode('UTF-8') == "This site is under maintenance"
    
