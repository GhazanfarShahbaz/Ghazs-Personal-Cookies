"""
file_name: app.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/08/2023
Description: Flask app for the knowledge_graph application.
Edit Log:
07/08/23 - Conformed to pylint conventions
"""

import logging.config

from json import load
from pathlib import Path
from os.path import join

from flask import Flask, request
from flask_apscheduler import APScheduler
from flask_cors import CORS

from apps.knowledge_graph.utils.build_knowledge_graph import (
    create_and_save_graph,
)

from apps.tool_repository.tools.endpoint_diagnostics import (
    setup_request,
    commit_endpoint_diagnostics,
)


app: Flask = Flask(
    __name__,
)
CORS(app)  # allows for cross-origin requests

# set app variables
app.config["data_directory"] = join(Path(__file__).resolve().parent, "data")
app.config["app_path"] = "/knowledge_graph"

# set uop logger
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


# Setup scheduler
scheduler = APScheduler()


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
            f"Html associated with  {request.remote_addr}",
            "",
        )

    return response


def load_and_return_graph():
    """
    Loads and returns the force-directed graph data from a JSON file.

    Returns:
        The loaded graph data.
    """

    with open(
        join(app.config["data_directory"], "forceGraph.json"),
        encoding="utf-8",
    ) as data_file:
        return load(data_file)


@scheduler.task("cron", id="update_force_graph_1", minute="*/15")
def update_force_graph():
    """
    Updates the force-directed graph by creating and saving the graph data to a JSON file.

    This function is run every 15 minutes by the apscheduler.

    Returns:
        None
    """

    app.logger.info("Running update_force_graph function")
    create_and_save_graph(join(app.config["data_directory"], "forceGraph.json"))


@app.route("/", methods=["GET"])
def home_route():
    """
    Returns the loaded force-directed graph data.

    Returns:
        The loaded graph data.
    """

    return load_and_return_graph()


scheduler.init_app(app)
scheduler.start()

# Replacement for before_first_request
with app.app_context():
    update_force_graph()

if __name__ == "__main__":
    app.run(debug=True)
