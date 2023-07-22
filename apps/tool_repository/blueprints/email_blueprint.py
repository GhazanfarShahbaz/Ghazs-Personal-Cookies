"""
file_name = email_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for email endpoints.
Edit Log:
07/20/2023
-   Moved email endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request

from apps.tool_repository.tools.process_gmail_requests import get_emails

email_blueprint: Blueprint = Blueprint("email", __name__)

@email_blueprint.route("/getGmailEmails", methods=["POST"])
def get_gmail_emails():
    """
    Gets Gmail emails.

    This function gets emails from Gmail by calling the `get_emails`
    function with the `authorizationFile`,`labelFilters`, `maxResults`,
    and `snippet` arguments included in the POST request.

    Returns:
        A JSON object containing the requested emails.

    Raises:
        None.
    """

    request_form = request.json

    return get_emails(
        request_form.get("authorizationFile"),
        request_form.get("labelFilters"),
        request_form.get("maxResults"),
        request_form.get("snippet"),
    )
