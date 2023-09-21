"""
file_name = assignment_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for assignment endpoints.
Edit Log:
07/20/2023
-   Moved assignment endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request

from apps.tool_repository.tools.process_assignment_requests import (
    process_get_assignment_request,
    process_create_assignment,
    process_update_assignment,
    process_delete_assignment_request,
)

assignment_blueprint: Blueprint = Blueprint("assignment", __name__)


@assignment_blueprint.route("/addAssignment", methods=["POST"])
def add_assignment():
    """
    Adds an assignment.

    This function adds an assignment to the database by processing
    an assignment form included in the POST request.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("assignmentForm"):
        process_create_assignment(request_form.get("assignmentForm"))

    return {}


@assignment_blueprint.route("/getAssignment", methods=["POST"])
def get_assignment():
    """
    Gets an assignment.

    This function gets assignments based on a filter assignment form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("filterForm"):
        process_get_assignment_request(request_form.get("filterForm"))

    return {}


@assignment_blueprint.route("/updateAssignment", methods=["POST"])
def update_assignment():
    """
    Updates an assignment.

    This function updates an assignment based on an update assignment form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("updateForm"):
        process_update_assignment(request_form.get("updateForm"))

    return {}


@assignment_blueprint.route("/deleteAssignment", methods=["POST"])
def delete_assignment():
    """
    Deletes an assignment.

    This function deletes an assignment based on a delete assignment form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_assignment_request(request_form.get("deleteForm"))

    return {}
