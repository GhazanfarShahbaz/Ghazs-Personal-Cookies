"""
file_name: app.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/08/2023
Description: Flask app for the obsodiain_connector api.
Edit Log:
07/08/23 - Conformed to pylint conventions
"""

import logging.config

from flask import Flask, request
from flask_apscheduler import APScheduler  # pylint: disable=import-error

from apps.obsidian_connector.utils.utils import (
    reload_vault,
    get_vault_files,
    get_vault_file_contents_by_name,
    get_file_contents_by_name_detailed,
    get_folder_contents
)

from apps.tool_repository.app import validate_user
from apps.tool_repository.tools.endpoint_diagnostics import (
    setup_request,
    commit_endpoint_diagnostics,
)

app: Flask = Flask(
    __name__,
)

# set app variables
app.config["app_path"] = "/obsidian_connector"

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
def log_request():
    app.logger.info(
        " %s %s%s", request.remote_addr, app.config["app_path"], request.path
    )

    if request.method != "GET":
        content_type: str = request.content_type
        request_form = None

        if content_type == "multipart/form-data":
            request_form = loads(request.form["json"])
            request.json = request_form
        else:
            request_form = request.json

        app.logger.info(request_form)

        if not validate_user(
            request_form.get("username"), request_form.get("password")
        ):
            return {"Status": "Invalid Request"}

    setup_request(request, f"{app.config['app_path']}{request.path}")


@app.after_request
def commit_diagnostics(response):
    if request.args.get("endpoint_id"):
        app.logger.info("Commiting endpoint diagonstic")
        commit_endpoint_diagnostics(
            request.args.get("endpoint_id"),
            f"Html associated with  {request.remote_addr}",
            "",
        )

    return response


@scheduler.task("cron", id="update_vault_1", minute="*/15")
def update_vault():
    reload_vaullt()


@app.route("/", methods=["GET"])
def home_route():
    return {"staus": "APi is up"}


@app.route("/getFileList", methods=["POST"])
def get_file_list():
    return {"fileNames": sorted(get_vault_files())}


@app.route("/getFileContents", methods=["POST"])
def get_file_contents():
    return {"contents": get_vault_file_contents_by_name(request.json.get("fileName"))}


@app.route("/geFileContentsDetailed", methods=["POST"])
def get_file_contents_detailed():
    return {"contents": get_file_contents_by_name_detailed(request.json.get("fileName"))}

@app.route("/getFolderContents", methods=["POST"])
def get_folder():
    request_data = request.json
    return get_file_contents(request_data["folderName"])

# TODO: Endoint for editing a markdown file.
# TODO: Endpoint for getting file information like referenced files , lasted edited, first created, last opened, etc.add()
# TODO: Endpoint for returning a tree instead of a list of files. So we can traverse through directories.
# TODO: Endpoint for adding a markdown file .add()
# TODO: Endpoint for getting vault information: connectivity (for each folder?), total number of references, total number of files, total space, etc.


scheduler.init_app(app)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
