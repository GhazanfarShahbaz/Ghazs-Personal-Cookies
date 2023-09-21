"""
file_name = diagnostics_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for diagnostic endpoints.
Edit Log:
07/20/2023
-   Moved diagnostic endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request

from apps.tool_repository.tools.process_endpoint_diagnostics import (
    process_get_diagnostics,
)

diagnostics_blueprint: Blueprint = Blueprint("diagnostics", __name__)


@diagnostics_blueprint.route("/getEndpointDiagnostics", methods=["POST"])
def get_endpoints_data():
    """
    Gets endpoint diagnostics.

    This function gets endpoint diagnostics by processing a
    filter form included in the POST request. The function calls the
    `process_get_diagnostics` function to get the diagnostics data.

    Returns:
        A JSON object containing the diagnostics data.

    Raises:
        None.
    """

    request_form = request.json

    return process_get_diagnostics(request_form.get("filterForm"))
