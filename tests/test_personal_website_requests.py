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
    
    
def test_getprojects():
    response = app.test_client().get("/projects")
    
    assert response.status_code == 200
    
    
def test_getskills():
    response = app.test_client().get("/skills")
    
    assert response.status_code == 200
    
def test_getskills():
    response = app.test_client().get("/skills")
    
    assert response.status_code == 200
    
def test_geteducation():
    response = app.test_client().get("/education")
    
    assert response.status_code == 200
    
    
def test_getresume():
    response = app.test_client().get("/resume")
    
    assert response.status_code == 200
