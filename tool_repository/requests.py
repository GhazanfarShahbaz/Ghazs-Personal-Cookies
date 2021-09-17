from apscheduler.schedulers.background import BackgroundScheduler
from typing import List
from flask import Flask 
from flask import request, jsonify

from tools.repository.model import Event
from tools.process_event_requests import process_create_event, process_get_event, process_get_default_event, process_update_event, process_delete_event
from tools.process_class_requests import process_create_class, process_get_class_request, process_update_class, process_delete_class_request
from tools.process_syllabus_requests import process_get_syllabus_request, process_create_syllabus, process_update_syllabus, process_delete_syllabus_request
from tools.process_assignment_requests import process_get_assignment_request, process_create_assignment, process_update_assignment, process_delete_assignment_request
from tools.process_weather_requests import get_weather
from response_processing.event_processing import print_events
from validate import validate_user

app = Flask(__name__)

@app.route("/createEvent", methods=["POST"])
def create_event():
    request_form = request.json
    
    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("eventForm"):
        process_create_event(request_form.get("eventForm"))

    return "Success"
    

@app.route("/getEvent", methods=["POST"])
def get_events():
    request_form = request.json
    event_list: List[Event] = []

    if validate_user(request_form.get("username"), request_form.get("password")):
        if request_form.get("defaultForm"):
            event_list = process_get_default_event(request_form.get("defaultForm"))
        elif request_form.get("filterForm"):
            event_list = process_get_event(request_form.get("filterForm"))
        else:
            event_list = process_get_event({})
    return jsonify(event_list) if request_form.get("stringifyResult") is None else jsonify(print_events(event_list, set()))


@app.route("/updateEvent", methods=["POST"])
def update_event():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("filterForm"):
        process_update_event(request_form.get("filterForm"))

    return "Success"


@app.route("/deleteEvent", methods=["POST"])
def delete_event():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("deleteForm"):
        process_delete_event(request_form.get("deleteForm"))
    

    return "Success"


@app.route("/addClass", methods=["POST"])
def add_class():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("classForm"):
        process_create_class(request_form.get("classForm"))

    return {}


@app.route("/getClass", methods=["POST"])
def get_class():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("filterForm"):
        process_get_class_request(request_form.get("filterForm"))

    return {}


@app.route("/updateClass", methods=["POST"])
def update_class():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("updateForm"):
        process_update_class(request_form.get("updateForm"))

    return {}


@app.route("/deleteClass", methods=["POST"])
def delete_class():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("deleteForm"):
        process_delete_class_request(request_form.get("deleteForm"))

    return {}


@app.route("/addSyllabus", methods=["POST"])
def add_syllabus():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("syllabusForm"):
        process_create_syllabus(request_form.get("syllabusForm"))

    return {}


@app.route("/getSyllabus", methods=["POST"])
def get_syllabus():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("filterForm"):
        process_get_syllabus_request(request_form.get("filterForm"))

    return {}


@app.route("/updateSyllabus", methods=["POST"])
def update_syllabus():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("updateForm"):
        process_update_syllabus(request_form.get("updateForm"))

    return {}


@app.route("/deleteSyllabus", methods=["POST"])
def delete_syllabus():
    request_form = request.json

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

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("filterForm"):
        process_get_assignment_request(request_form.get("filterForm"))

    return {}


@app.route("/updateAssignment", methods=["POST"])
def update_assignment():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("updateForm"):
        process_update_assignment(request_form.get("updateForm"))

    return {}


@app.route("/deleteAssignment", methods=["POST"])
def delete_assignment():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    if request_form.get("deleteForm"):
        process_delete_assignment_request(request_form.get("deleteForm"))

    return {}


@app.route("/getQuestion", methods=["POST"])
def get_question():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}

@app.route("/syncQuestion", methods=["POST"])
def sync_question():
    # request_form = request.json
    # print("SUCCES")
    # if not validate_user(request_form.get("username"), request_form.get("password")):
    #     return "Invalid"

    print("Test")


@app.route("/getWeather", methods=["POST"])
def get_weather():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return get_weather()

scheduler = BackgroundScheduler()
scheduler.add_job(func=sync_question, trigger="interval", hours=1)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
