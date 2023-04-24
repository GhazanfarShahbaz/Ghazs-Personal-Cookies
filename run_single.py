from apps.personal_website.requests import app as personal_website_app
from apps.tool_repository.endpoints import app as tool_app
from apps.projects.the_mouseion.app import app as mouseion_app
from apps.Asian210CreativeProject.app import app as creative_app


from typing import Dict
from flask import Flask


app_list: Dict[str, Flask] = {
    "personal_website"  : personal_website_app,
    "tools"             : tool_app ,
    "the_mouseion"      : creative_app,
    "creative_project"  : creative_app

}

app_name = input("Input the application name: ")

if app_name in app_list.keys():
    app_list[app_name].run()
else:
    print("That application does not exist")