from apscheduler.schedulers.background import BackgroundScheduler
from typing import List
from flask import Flask 
from flask import request, jsonify

from tools.repository.model import Event
from tools.process_event_requests import process_create_event, process_get_event, process_get_default_event, process_update_event, process_delete_event
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

    return {}


@app.route("/getClass", methods=["POST"])
def get_class():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/updateClass", methods=["POST"])
def update_class():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/deleteClass", methods=["POST"])
def delete_class():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/addSyllabus", methods=["POST"])
def add_syllabus():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/getSyllabus", methods=["POST"])
def get_syllabus():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/updateSyllabus", methods=["POST"])
def update_syllabus():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/deleteSyllabus", methods=["POST"])
def delete_syllabus():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/addGrade", methods=["POST"])
def add_grade():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/getGrade", methods=["POST"])
def get_grade():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/updateGrade", methods=["POST"])
def update_grade():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

    return {}


@app.route("/deleteGrade", methods=["POST"])
def delete_grade():
    request_form = request.json

    if not validate_user(request_form.get("username"), request_form.get("password")):
        return "Invalid"

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