"""
file_name = class_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for class endpoints.
Edit Log:
07/20/2023
-   Moved class endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from flask import Blueprint, request

from apps.tool_repository.tools.process_class_requests import (
    process_create_class,
    process_get_class_request,
    process_update_class,
    process_delete_class_request,
)

class_blueprint: Blueprint = Blueprint("class", __name__)

@class_blueprint.route("/addClass", methods=["POST"])
def add_class():
    """
    Adds a class.

    This function adds a class to the database by processing
    a class form included in the POST request.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("classForm"):
        process_create_class(request_form.get("classForm"))

    return {}


@class_blueprint.route("/getClass", methods=["POST"])
def get_class():
    """
    Gets classes.

    This function gets classes based on a filter class form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("filterForm"):
        process_get_class_request(request_form.get("filterForm"))

    return {}


@class_blueprint.route("/updateClass", methods=["POST"])
def update_class():
    """
    Updates classes.

    This function updates classes based on a update class form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("updateForm"):
        process_update_class(request_form.get("updateForm"))

    return {}


@class_blueprint.route("/deleteClass", methods=["POST"])
def delete_class():
    """
    Deletes a class.

    This function deletes a class based on a delete class form.

    Returns:
        An empty dictionary.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_class_request(request_form.get("deleteForm"))

    return {}
