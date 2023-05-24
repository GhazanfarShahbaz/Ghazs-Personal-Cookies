from apps.personal_website.requests import app as personal_website_app
from apps.tool_repository.endpoints import app as tool_app
from apps.projects.the_mouseion.app import app as mouseion_app


from typing import Dict
from flask import Flask

# Define a dictionary of Flask apps, where each key is an app name and each value is the corresponding app
app_list: Dict[str, Flask] = {
    "personal_website"  : personal_website_app,
    "tools"             : tool_app,
    "the_mouseion"      : mouseion_app
}

# Get the app name from the user
app_name = input("Input the application name: ")

# If the app name is in the app_list dictionary, run the corresponding app
if app_name in app_list.keys():
    app_list[app_name].run()
# If the app name is not in the app_list dictionary, print an error message
else:
    print("That application does not exist")