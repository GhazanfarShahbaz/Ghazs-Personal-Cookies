"""
file_name: app.py
Creator: Ghazanfar Shahbaz
Created: 08/05/2023
Last Updated: 08/05/2023
Description: Flask app for getting coding questions.
Edit Log:
08/05/2023
- Created file and added logic
"""

import logging.config

from random import randint

from flask import Flask, request

from apps.coding_questions.utils.process_random_codechef_question import (
    process_random_codechef_request,
)
from apps.coding_questions.utils.process_random_leetcode import (
    process_random_leetcode_request,
)

from apps.tool_repository.tools.endpoint_diagnostics import (
    setup_request,
    commit_endpoint_diagnostics,
)

app: Flask = Flask(
    __name__,
)

# APP VARIABLES
app.config["app_path"] = "/coding_questions"
app.config["euler_count"] = 851

# APP LOGGER
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


@app.before_request
def log_request() -> None:
    app.logger.info(
        " %s %s%s", request.remote_addr, app.config["app_path"], request.path
    )
    setup_request(request, f"{app.config['app_path']}{request.path}")


@app.after_request
def commit_diagnostics(response):
    """
    Commits endpoint diagonstic information after handling a
    request.

    This function takes a response object and checks if the
    request includes an "endpoint_id" parameter.
    If the parameter is present, the function logs a message
    and commits endpoint diagnostic information
    using the `commit_endpoint_diagnostics` function.
    The function then returns the original response.

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
            "",
            "",
        )

    return response


@app.route("/", methods=["GET"])
def home():
    return {"status": "App is up and running"}


@app.route("/getRandomLeetcodeProblem", methods=["POST"])
def get_random_problem():
    return {"link": process_random_leetcode_request(request.get("filterForm"))}


@app.route("/getRandomCodeChefProblem", methods=["POST"])
def get_random_codechef_problem():
    return {"link": process_random_codechef_request(request.get("filterForm"))}


@app.route("/getRandomEulerProblem", methods=["GET"])
def get_random_euler_problem():
    return {"link": f"https://projecteuler.net/problem={randint(1,app.config['euler_count'])}"}
