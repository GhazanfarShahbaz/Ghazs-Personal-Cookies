"""
file_name = translation_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for translation endpoints.
Edit Log:
07/20/2023
-   Moved translation endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request

from apps.tool_repository.tools.process_translate_request import process_translate

translation_blueprint: Blueprint = Blueprint("translation", __name__)

@translation_blueprint.route("/getTranslation", methods=["POST"])
def get_translation():
    """
    Gets a translation.

    This function gets a translation by processing a translation form included in the POST request.

    Returns:
        A JSON object containing the translated text.

    Raises:
        None
    """

    request_form = request.json

    return process_translate(request_form.get("translationForm"))
