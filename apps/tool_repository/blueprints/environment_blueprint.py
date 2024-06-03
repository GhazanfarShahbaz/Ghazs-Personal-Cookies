"""
file_name = environment_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for environment endpoints.
Edit Log:
07/20/2023
-   Moved environment endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from os import environ, getenv

from firebase_admin import firestore

from flask import Blueprint, request

environment_blueprint: Blueprint = Blueprint("environment", __name__)


@environment_blueprint.route("/setEnvironmentVariable", methods=["POST"])
def set_environment_variable():
    """
    Sets an environment variable.

    This function sets an environment variable in the database
    by processing an environment form included in the POST request.
    The function updates the environment variable in the database
    and in the server's environment variables.

    Returns:
        A JSON object containing the status of the operation.

    Raises:
        None.
    """

    request_form = request.json

    environment_form = request_form.get("environmentForm")
    key: str = environment_form["key"]
    value: str = environment_form["value"]

    if getenv(key) and not environ[environment_form["overwrite"]]:
        return {"Status": "Needs overwrite permission"}

    firestore_client = firestore.client()
    users_ref = firestore_client.collection(environ["FIRESTORE_SERVER"])
    environment_document = users_ref.document(environ["FIRESTORE_ENVIRONMENT_ID"])

    environment_document.update({key: value})

    environ[key] = value
    return {"Status": "Success"}
