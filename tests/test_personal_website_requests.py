import os
import sys

ROOT_DIRECTORY: str =  "/home/ghaz/flask_gateway/"
sys.path.append(ROOT_DIRECTORY)

import pytest
import json

import apps
from apps.personal_website.requests import app

def test_get_home():
    response = app.test_client().get("/")
    
    assert response.status_code == 200
    
    
def test_get_projects():
    response = app.test_client().get("/projects")
    
    assert response.status_code == 200
    
    
def test_get_skills():
    response = app.test_client().get("/skills")
    
    assert response.status_code == 200
    
def test_get_skills():
    response = app.test_client().get("/skills")
    
    assert response.status_code == 200
    
def test_get_education():
    response = app.test_client().get("/education")
    
    assert response.status_code == 200
    
    
def test_get_resume():
    response = app.test_client().get("/resume")
    
    assert response.status_code == 200
