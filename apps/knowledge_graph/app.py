"""
file_name: app.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/01/2023
Description: Flask app for the knowledge_graph application.
"""

from json import load
from pathlib import Path
from os.path import join

from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS

from apps.knowledge_graph.utils.build_knowledge_graph import (  # pylint: disable=import-error
    create_and_save_graph,
)

app: Flask = Flask(
    __name__,
)
CORS(app)  # allows for cross-origin requests

# set app variables
app.config["data_directory"] = join(Path(__file__).resolve().parent, "data")

# Setup scheduler
scheduler = APScheduler()


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


# NOTE: Update this as flask will be deprecating before_request_function
@app.before_first_request
@scheduler.task("cron", id="update_force_graph_1", minute="*/15")
def update_force_graph():
    """
    Updates the force-directed graph by creating and saving the graph data to a JSON file.

    This function is run every 15 minutes by the apscheduler.

    Returns:
        None
    """

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

if __name__ == "__main__":
    app.run(debug=True)
