"""
file_name = events_blueprint.py
Creator: Ghazanfar Shahbaz
Date Created: 07/20/2023
Last Updated: 07/21/2023
Description: A blueprint for events endpoints.
Edit Log:
07/20/2023
-   Moved events endpoints to this file.
07/21/2023
-   Documented with docstring.
"""

from typing import List

from flask import Blueprint, request, jsonify, current_app

from apps.tool_repository.response_processing.event_processing import (
    print_events,
    jsonify_event_list
)
from repository.models.event_model import Event

from apps.tool_repository.tools.process_event_requests import (
    process_create_event,
    process_get_event,
    process_get_default_event,
    process_update_event,
    process_delete_event,
)

events_blueprint: Blueprint = Blueprint("events", __name__)


@events_blueprint.route("/createEvent", methods=["POST"])
def create_event():
    """
    Creates an event.

    This function creates an event by processing the event form included in the POST request.
    The `process_create_event` function is called to create the event.

    Returns:
        A string "Success" indicating that the event was successfully created.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("eventForm"):
        process_create_event(request_form.get("eventForm"))

    return "Success"


@events_blueprint.route("/addEventsFromCSV", methods=["POST"])
def add_events_from_csv():
    """
    Adds events from a CSV.

    This function adds events to the database by processing a CSV file included in the POST request.
    The function does not currently have an implementation, and the "TODO" comment indicates that
    this is an area that needs to be developed.

    Returns:
        None.

    Raises:
        None.
    """

    # TODO: Finish this function # pylint: disable=fixme
    ...  # pylint: disable=unnecessary-ellipsis


@events_blueprint.route("/getEvent", methods=["POST"])
def get_events():
    """
    Gets events.

    This function gets events by either processing the default event form or a filter event form.
    If the `defaultForm` argument is present in the POST request, the function calls the
    `process_get_default_event` function to get the default events. If the `filterForm` argument
    is present, the function calls the `process_get_event` function to get events based on the
    filter.

    Returns:
        A JSON object containing the event list if the `stringifyResult` argument is not present,
        or a stringified version of the event list if the `stringifyResult` argument is present.

    Raises:
        None.
    """

    request_form = request.json
    event_list: List[Event] = []

    if request_form.get("defaultForm"):
        event_list = process_get_default_event(request_form.get("defaultForm"))
    elif request_form.get("filterForm"):
        event_list = process_get_event(request_form.get("filterForm"))
    else:
        event_list = process_get_event({})

    current_app.logger.info(jsonify_event_list(event_list))
    return (
        jsonify_event_list(event_list)
        if request_form.get("stringifyResult") is None
        else jsonify(print_events(event_list, set()))
    )


@events_blueprint.route("/updateEvent", methods=["POST"])
def update_event():
    """
    Updates events.

    This function updates events based on a filter event form.

    Returns:
        A string "Success" indicating that the events were successfully updated.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("filterForm"):
        process_update_event(request_form.get("filterForm"))

    return "Success"


@events_blueprint.route("/deleteEvent", methods=["POST"])
def delete_event():
    """
    Deletes events.

    This function deletes events based on a delete event form.

    Returns:
        A string "Success" indicating that the events were successfully deleted.

    Raises:
        None.
    """

    request_form = request.json

    if request_form.get("deleteForm"):
        process_delete_event(request_form.get("deleteForm"))

    return "Success"
