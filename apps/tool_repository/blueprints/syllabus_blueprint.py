"""
file_name = syllabus_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for syllabus endpoints.
Edit Log:
07/20/2023
-   Moved syllabus endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request

from apps.tool_repository.tools.process_syllabus_requests import (
    process_get_syllabus_request,
    process_create_syllabus,
    process_update_syllabus,
    process_delete_syllabus_request,
)

syllabus_blueprint: Blueprint = Blueprint("syllabus", __name__)


@syllabus_blueprint.route("/addSyllabus", methods=["POST"])
def add_syllabus():
    """
    Adds a syllabus.

    This function adds a syllabus to the database by processing
    a syllabus form included in the POST request.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("syllabusForm"):
        process_create_syllabus(request_form.get("syllabusForm"))

    return {}


@syllabus_blueprint.route("/getSyllabus", methods=["POST"])
def get_syllabus():
    """
    Gets a syllabus.

    This function gets syllabi based on a filter syllabus form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("filterForm"):
        process_get_syllabus_request(request_form.get("filterForm"))

    return {}


@syllabus_blueprint.route("/updateSyllabus", methods=["POST"])
def update_syllabus():
    """
    Updates a syllabus.

    This function updates a syllabus based on an update syllabus form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("updateForm"):
        process_update_syllabus(request_form.get("updateForm"))

    return {}


@syllabus_blueprint.route("/deleteSyllabus", methods=["POST"])
def delete_syllabus():
    """
    Deletes a syllabus.

    This function deletes a syllabus based on a delete syllabus form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_syllabus_request(request_form.get("deleteForm"))

    return {}
