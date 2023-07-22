"""
file_name = help_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for help endpoints.
Edit Log:
07/20/2023
-   Moved help endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request

from apps.tool_repository.tools.process_help_requests import get_command

help_blueprint: Blueprint = Blueprint("help", __name__)

@help_blueprint.route("/getHelp", methods=["POST"])
def get_help():
    """
    Gets help information.

    This function gets help information by processing a command included in the POST request.
    The function calls the `get_command` function to get information about the command.

    Returns:
        A JSON object containing the command information.

    Raises:
        None.
    """

    request_form = request.json

    return get_command(request_form.get("command"))
