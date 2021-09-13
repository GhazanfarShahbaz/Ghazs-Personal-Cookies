from typing import List
from flask import Flask 
from flask import request, jsonify

from tools.repository.model import Event
from tools.process_event_requests import process_create_event, process_get_event, process_update_event, process_delete_event

app = Flask(__name__)

@app.route("/")
def est():
    return "Success"
    

@app.route("/createEvent", methods=["POST"])
def create_event():
    request_form = request.json
    
    if request_form.get("eventForm"):
        process_create_event(request_form.get("eventForm"))

    print("Success")
    return "Success"
    
@app.route("/getEvent", methods=["POST"])
def get_events():
    request_form = request.json
    event_list: List[Event] = []

    if request_form.get("filterForm"):
        event_list = process_get_event(request_form.get("filterForm"))
    else:
        event_list = process_get_event({})
    
    return jsonify(event_list)


@app.route("/updateEvent", methods=["POST"])
def update_event():
    request_form = request.json

    if request_form.get("filterForm"):
        process_update_event(request_form.get("filterForm"))

    return "Success"


@app.route("/deleteEvent", methods=["POST"])
def delete_event():
    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_event(request_form.get("deleteForm"))
    

    return "Success"

if __name__ == "__main__":
    app.run()