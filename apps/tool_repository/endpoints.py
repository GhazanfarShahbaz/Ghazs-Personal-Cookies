
from datetime import datetime

from flask import Flask
from flask import request, jsonify

from firebase_admin import credentials, firestore, initialize_app
from response_processing.event_processing import print_events

from tools.repository.model import Event
from tools.process_event_requests import process_create_event, process_get_event, process_get_default_event, process_update_event, process_delete_event
from tools.process_class_requests import process_create_class, process_get_class_request, process_update_class, process_delete_class_request
from tools.process_syllabus_requests import process_get_syllabus_request, process_create_syllabus, process_update_syllabus, process_delete_syllabus_request
from tools.process_assignment_requests import process_get_assignment_request, process_create_assignment, process_update_assignment, process_delete_assignment_request
from tools.process_weather_requests import get_weather
from tools.process_gmail_requests import get_emails
from tools.process_help_requests import get_command
from tools.process_translate_request import process_translate

from typing import List

import logging
import os


app = Flask(__name__)
logging.basicConfig(filename='logs/tool_requests.log', level=logging.DEBUG)

cred = credentials.Certificate(os.getenv("FIRESTORE_TOKEN"))
initialize_app(cred)


def get_login(from_server = False) -> dict:
    db = firestore.client()
    users_ref = db.collection(os.environ["FIRESTORE_SERVER"])

    login_allow = users_ref.document('allow')

    if not from_server and login_allow.get().to_dict()["allow"] is False:
        return None
    
    login_allow.update({
        u'allow': False
    })

    return users_ref.document(os.environ["FIRESTORE_DOC_ID"]).get().to_dict()


def validate_user(username: str, password: str) -> bool:
    token = get_login()

    if token and (username and username == token["username"]) and (password and password == token["password"]):
        return True

    app.logger.info(
        f'Invalid Username and Password were supplied {request.remote_addr} on {datetime.now()}'
    )
    return False


@app.route("/createEvent", methods=["POST"])
def create_event():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint createEvent")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("eventForm"):
        process_create_event(request_form.get("eventForm"))

    return "Success"


@app.route("/getEvent", methods=["POST"])
def get_events():
    request_form = request.json
    event_list: List[Event] = []

    app.logger.info(f"{request.remote_addr} visited endpoint getEvent")
    app.logger.info(request.json)

    if validate_user(request_form.get("username"), request_form.get("password")):
        if request_form.get("defaultForm"):
            event_list = process_get_default_event(
                request_form.get("defaultForm"))
        elif request_form.get("filterForm"):
            event_list = process_get_event(request_form.get("filterForm"))
        else:
            event_list = process_get_event({})

    return jsonify(event_list) if request_form.get("stringifyResult") is None else jsonify(print_events(event_list, set()))


@app.route("/updateEvent", methods=["POST"])
def update_event():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint updateEvent")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("filterForm"):
        process_update_event(request_form.get("filterForm"))

    return "Success"


@app.route("/deleteEvent", methods=["POST"])
def delete_event():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint deleteEvent")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("deleteForm"):
        process_delete_event(request_form.get("deleteForm"))

    return "Success"


@app.route("/addClass", methods=["POST"])
def add_class():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint addClass")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("classForm"):
        process_create_class(request_form.get("classForm"))

    return {}


@app.route("/getClass", methods=["POST"])
def get_class():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint getClass")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("filterForm"):
        process_get_class_request(request_form.get("filterForm"))

    return {}


@app.route("/updateClass", methods=["POST"])
def update_class():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint updateClass")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("updateForm"):
        process_update_class(request_form.get("updateForm"))

    return {}


@app.route("/deleteClass", methods=["POST"])
def delete_class():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint deleteClass")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("deleteForm"):
        process_delete_class_request(request_form.get("deleteForm"))

    return {}


@app.route("/addSyllabus", methods=["POST"])
def add_syllabus():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint addSyllabus")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("syllabusForm"):
        process_create_syllabus(request_form.get("syllabusForm"))

    return {}


@app.route("/getSyllabus", methods=["POST"])
def get_syllabus():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint getSyllabus")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("filterForm"):
        process_get_syllabus_request(request_form.get("filterForm"))

    return {}


@app.route("/updateSyllabus", methods=["POST"])
def update_syllabus():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint updateSyllabus")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("updateForm"):
        process_update_syllabus(request_form.get("updateForm"))

    return {}


@app.route("/deleteSyllabus", methods=["POST"])
def delete_syllabus():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint deleteSyllabus")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("deleteForm"):
        process_delete_syllabus_request(request_form.get("deleteForm"))

    return {}


@app.route("/addAssignment", methods=["POST"])
def add_assignment():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("assignmentForm"):
        process_create_assignment(request_form.get("assignmentForm"))

    return {}


@app.route("/getAssignment", methods=["POST"])
def get_assignment():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint getAssignment")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("filterForm"):
        process_get_assignment_request(request_form.get("filterForm"))

    return {}


@app.route("/updateAssignment", methods=["POST"])
def update_assignment():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint updateAssignment")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("updateForm"):
        process_update_assignment(request_form.get("updateForm"))

    return {}


@app.route("/deleteAssignment", methods=["POST"])
def delete_assignment():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint deleteAssignment")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("deleteForm"):
        process_delete_assignment_request(request_form.get("deleteForm"))

    return {}

@app.route("/getCurrentWeather", methods=["POST"])
def get_current_weather():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint getWeather")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return get_weather()


@app.route("/getGmailEmails", methods=["POST"])
def get_gmail_emails():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint getEmails")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return get_emails(request_form.get("authorizationFile"), request_form.get("labelFilters"), request_form.get("maxResults"))


@app.route("/getTranslation", methods=["POST"])
def get_translation():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint getEmails")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return process_translate(request_form.get("translationForm"))


@app.route("/getHelp", methods=["POST"])
def get_help():
    request_form = request.json

    app.logger.info(f"{request.remote_addr} visited endpoint getEmails")
    app.logger.info(request.json)

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return get_command(request_form.get("command"))

if __name__ == "__main__":
    app.run(debug=True)
