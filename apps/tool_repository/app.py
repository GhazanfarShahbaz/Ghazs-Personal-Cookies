"""
file_name = app.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/08/2023
Description: A flask file for the tools application.
Edit Log:
07/08/2023
-   Changed file name from endpoints.py to app.py.
-   Conformed to pylint conventions
07/21/2023
-   Turned all endpoints into blueprints for modularity
"""

import logging.config

from datetime import datetime

from os import environ

from json import loads

from flask import Flask
from flask import request

from typing import Set

from firebase_admin import credentials, firestore, initialize_app

from apps.tool_repository.tools.endpoint_diagnostics import (
    setup_request,
    commit_endpoint_diagnostics,
)

CREDENTIALS = credentials.Certificate(environ["FIRESTORE_TOKEN"])
initialize_app(CREDENTIALS)

from apps.tool_repository.blueprints.assignment_blueprint import assignment_blueprint
from apps.tool_repository.blueprints.authentication_blueprint import token_handler, authentication_blueprint
from apps.tool_repository.blueprints.class_blueprint import class_blueprint
from apps.tool_repository.blueprints.diagnostics_blueprint import diagnostics_blueprint
from apps.tool_repository.blueprints.email_blueprint import email_blueprint
from apps.tool_repository.blueprints.environment_blueprint import environment_blueprint
from apps.tool_repository.blueprints.events_blueprint import events_blueprint
from apps.tool_repository.blueprints.file_blueprint import file_blueprint
from apps.tool_repository.blueprints.help_blueprint import help_blueprint
from apps.tool_repository.blueprints.logs_blueprint import logs_blueprint
from apps.tool_repository.blueprints.message_blueprint import message_blueprint
from apps.tool_repository.blueprints.qrcode_blueprint import qrcode_blueprint
from apps.tool_repository.blueprints.syllabus_blueprint import syllabus_blueprint
from apps.tool_repository.blueprints.translation_blueprint import translation_blueprint
from apps.tool_repository.blueprints.weather_blueprint import weather_blueprint


app = Flask(__name__)

logging.config.fileConfig("/home/ghaz/flask_gateway/logging.conf")
app.logger = logging.getLogger("MainLogger")

handler = logging.handlers.TimedRotatingFileHandler("logs/app.log", when="midnight")

handler.prefix = "%Y%m%d"

formatter = logging.Formatter(
    fmt="%(asctime)s | %(pathname)s | \
        %(levelname)-8s | %(filename)s-%(funcName)s-%(lineno)04d | \
        %(message)s"
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

APP_PATH: str = "/tools"

# TODO: Change and make specific
EXCLUDED_VALIDATION: Set[str] = {
    "grantAuthenticationToken"
}

@app.before_request
def log_request() -> None:  # pylint: disable=inconsistent-return-statements
    """
    Logs the incoming request.

    This function logs the incoming request, including the IP address
    of the request and the path of the request.
    If the request includes JSON data, the function logs this as well.
    The function then validates the request
    user using the `validate_user` function. If the user is invalid,
    the function returns a status dictionary with
    "Status": "Invalid Request". The function then sets up the request
    with `setup_request`.

    Returns:
        None.
    """

    app.logger.info(" %s %s%s", request.remote_addr, APP_PATH, request.path)
    app.logger.info(request.json)

    content_type: str = request.content_type
    request_form = None

    if content_type == "multipart/form-data":
        request_form = loads(request.form["json"])
        request.json = request_form
    else:
        request_form = request.json
    
    excluded: bool = False 
    for exclusion in EXCLUDED_VALIDATION:
        if exclusion.find(request.path):
            excluded = True 
    
    if not request_form.get("token") and not(request.path.find("grantAuthenticationToken") or request.path.find("validateAuthenticationToken")):
        if not validate_user(request_form.get("username"), request_form.get("password")):
            return {"Status": "Invalid Request"}
            
    elif not excluded:
        validation_code = token_handler.validate_token(request_form.get("username"), request_form.get("token"))

        if validation_code[ErrorCode] > 0: 
            return validation_code
            
            
    setup_request(request, f"tools{request.path}")


@app.after_request
def commit_diagnostics(response):
    """
    Commits endpoint diagonstic information after handling a request.

    This function takes a response object and checks if the request
    includes an "endpoint_id" parameter.
    If the parameter is present, the function logs a message and
    commits endpoint diagnostic information
    using the `commit_endpoint_diagnostics` function. The function
    then returns the original response.

    Args:
        response: A Flask response object representing the response to a request.

    Returns:
        The original Flask response object.

    Raises:
        None.
    """

    if request.args.get("endpoint_id"):
        app.logger.info("Commiting endpoint diagonstic")
        commit_endpoint_diagnostics(
            request.args.get("endpoint_id"),
            f"Html associated with  {request.remote_addr}",
            "",
        )

    return response

def get_login(from_server=False) -> dict:
    """
    Retrieves login information from Firebase.

    This function retrieves login information from Firebase Firestore.
    If the `from_server` argument is False (default), the function checks
    if the server is currently allowing login by checking if the "allow"
    field of the "allow" document in the collection named in `FIRESTORE_SERVER`
    is True. If the field is False, the function returns None. If the field is
    True or the `from_server` argument is True, the function sets
    the "allow" field to False and retrieves the login information
    from the document specified in `FIRESTORE_DOC_ID`.

    Args:
        from_server: A boolean indicating whether the request is coming from a server.

    Returns:
        A dictionary containing the login information.

    Raises:
        None
    """

    firestore_client = firestore.client()
    users_ref = firestore_client.collection(environ["FIRESTORE_SERVER"])
    login_allow = users_ref.document("allow")

    if not from_server and login_allow.get().to_dict()["allow"] is False:
        return None

    login_allow.update({"allow": False})

    return users_ref.document(environ["FIRESTORE_DOC_ID"]).get().to_dict()


def validate_user(username: str, password: str) -> bool:
    """
    Validates the user login credentials.

    This function takes a string `username` representing the user's
    login username and a string `password` representing the user's login
    password. The function retrieves the login information using the `get_login`
    function and checks whether the provided `username` and `password` match the
    login information. If the login information matches, the function returns True.
    Otherwise, the function logs a message and returns False.

    Args:
        username: A string representing the user's login username.
        password: A string representing the user's login password.

    Returns:
        A boolean indicating whether or not the user's login credentials are valid.

    Raises:
        None.
    """

    token = get_login()

    if (
        token
        and (username and username == token["username"])
        and (password and password == token["password"])
    ):
        return True

    app.logger.info(
        "Invalid Username and password were supplied %s /tools/%s on %s",
        request.remote_addr,
        request.path,
        datetime.now(),
    )

    return False


app.register_blueprint(authentication_blueprint)
app.register_blueprint(assignment_blueprint)
app.register_blueprint(class_blueprint)
app.register_blueprint(diagnostics_blueprint)
app.register_blueprint(email_blueprint)
app.register_blueprint(environment_blueprint)
app.register_blueprint(events_blueprint)
app.register_blueprint(file_blueprint)
app.register_blueprint(help_blueprint)
app.register_blueprint(logs_blueprint)
app.register_blueprint(message_blueprint)
app.register_blueprint(qrcode_blueprint)
app.register_blueprint(syllabus_blueprint)
app.register_blueprint(translation_blueprint)
app.register_blueprint(weather_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
