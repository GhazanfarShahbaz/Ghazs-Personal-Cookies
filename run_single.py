"""
file_name = run_single.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/07/2023
Description: A file used to run a single flask application alone. This is used for debugging.
"""

import sys

from typing import Dict

from stringcolor import cs

from apps.personal_website.app import app as personal_website_app
from apps.tool_repository.app import app as tool_app
from apps.knowledge_graph.app import app as knowledge_graph_app
from apps.projects.the_mouseion.app import app as mouseion_app
from apps.coding_questions.app import app as coding_question_app
from apps.obsidian_connector.app import app as obsidian_connector_app


# Define a dictionary of Flask apps. Each key is an app number and
# each value is the corresponding app dictionary containing the applications name and module
app_list: Dict[int, dict] = {
    1: {"app_name": "Personal Website", "app_module": personal_website_app},
    2: {"app_name": "Tools Application", "app_module": tool_app},
    3: {"app_name": "Knowledge Graph", "app_module": knowledge_graph_app},
    4: {"app_name": "The Mouseion", "app_module": mouseion_app},
    5: {"app_name": "Coding Questions App", "app_module": coding_question_app},
    6: {"app_name": "Obsidian Connector App", "app_module": obsidian_connector_app},
}


print("Available Applications: ")

for app_index, app_dict in app_list.items():
    print(cs(app_index, "grey4"), cs(app_dict["app_name"], "dodgerblue"))

print()

# Get the app number from the user
app_number_temp: str = input(
    "Please Enter the number of the application you want to run: "
)
app_number: int or None = None

# Try converting app number string to a number
try:
    app_number = int(app_number_temp)
except ValueError:
    print(cs("\nThis is not a number, exiting script.", "red"))
    sys.exit()

# If the app number is in the app_list dictionary, run the corresponding app
if app_number in app_list:
    app_list[app_number]["app_module"].run()
# If the app number is not in the app_list dictionary, print an error message
else:
    print(cs("That application number you entered does not exist", "red"))
