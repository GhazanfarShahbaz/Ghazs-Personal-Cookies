"""
file_name = logs_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for log endpoints.
Edit Log:
07/20/2023
-   Moved log endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint

from apps.tool_repository.tools.process_log_requests import process_get_logs

logs_blueprint: Blueprint = Blueprint("logs", __name__)

@logs_blueprint.route("/getLogs", methods=["POST"])
def get_logs():
    """
    Gets logs.

    This function gets logs by processing a filter form included in the POST request.
    The function calls the `process_get_logs` function to get the logs data.

    Returns:
        A JSON object containing the logs data.

    Raises:
        None.
    """

    return process_get_logs()
