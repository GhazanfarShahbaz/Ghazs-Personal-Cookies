"""
file_name = file_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for file endpoints.
Edit Log:
07/20/2023
-   Moved file endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request

from apps.tool_repository.tools.process_file_storage_requests import (
    process_upload_file,
    process_delete_file,
)

file_blueprint: Blueprint = Blueprint("file", __name__)


@file_blueprint.route("/uploadFile", methods=["POST"])
def upload_file():
    """
    Uploads a file.

    This function uploads a file based on the file data included in the POST request.

    Returns:
        A JSON object containing information about the uploaded file.

    Raises:
        None.
    """

    file = request.files["file"]

    return process_upload_file(file, request.mimetype)


@file_blueprint.route("/deleteFile", methods=["POST"])
def delete_file():
    """
    Deletes a file.

    This function deletes a file based on a delete file form.

    Returns:
        A JSON object indicating whether the file was successfully deleted.

    Raises:
        None.
    """

    request_form = request.json

    return process_delete_file(request_form.get("deleteForm"))
