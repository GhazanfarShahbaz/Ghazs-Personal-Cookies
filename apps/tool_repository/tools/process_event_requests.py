"""
file_name = process_event_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to process event requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
07/20/2023
-   Added caching to get default event.
-   Remove previous cache when creating, deleting, or updating events.
"""

from typing import List

from apps.tool_repository.tools.repository.events import EventRepository
from apps.tool_repository.tools.repository.models.event_model import Event

from apps.tool_repository.tools.event_utils import (
    create_event_information,
    default_form_get_date_to_and_date_from,
    event_type_list_to_event_type_list,
    time_until_eod,
)

from apps.tool_repository.tools.redis_decorator import Cache
from apps.tool_repository.tools.redis_utils import RedisClient

DEFAULT_KEYS: List[str] = ["today", "week", "month", "year"]


def key_remover(func):
    def wrapper(*args, **kwargs):
        with RedisClient() as client:
            global DEFAULT_KEYS  # pylint: disable=global-variable-not-assigned
            client.remove_keys(DEFAULT_KEYS)

        return func(*args, **kwargs)

    return wrapper


@key_remover
def process_create_event(event_data: dict) -> None:
    """
    Processes a request to create a new event.

    This function takes a dictionary `event_data` representing the event data from a
    request and creates new events in the event repository.
    The `event_data` can represent a single event or a series of recurring events.

    Args:
        event_data: A dictionary containing the event data.

    Returns:
        None. The function does not return anything.
    """

    event_list: List[Event] = create_event_information(event_data)
    EventRepository().insert(event_list)


def process_get_default_event(default_form: dict) -> List[dict]:
    """
    Processes a request to retrieve a list of events using default parameters.

    This function takes a dictionary `default_form` representing the default
    parameters for an events request.
    It sets any missing parameters to their default values, then calls the `process_get_event`
    function with these parameters to retrieve a list of events.

    Args:
        default_form: A dictionary containing the default parameters for the request.

    Returns:
        A list of dictionaries representing the retrieved events. Each dictionary contains the
        fields "EventId", "UserId", "Name", "StartDate", "EndDate", and "Recurring".
    """

    # @Cache(cache_key=default_form.get("DefaultOption"), expiration_time=time_until_eod)
    def get_default_events():
        (
            default_form["DateFrom"],
            default_form["DateTo"],
        ) = default_form_get_date_to_and_date_from(default_form.get("DefaultOption"))

        return process_get_event(default_form)

    return get_default_events()


def process_get_event(filter_form: dict) -> List[dict]:
    """
    Processes a request to retrieve a list of events that match the given filter.

    This function takes a dictionary `filter_form` representing the filter parameters for
    an events request, and calls the `EventRepository().get()` method with these parameters
    to retrieve a list of events that match the filter.
    The returned events are then converted to a list of dictionaries using the
    `event_type_list_to_event_type_list()` function.

    Args:
        filter_form: A dictionary containing the filter parameters for the request.

    Returns:
        A list of dictionaries representing the retrieved events. Each dictionary contains the
        fields "EventId", "UserId", "Name", "StartDate", "EndDate", and "Recurring".
    """

    event_list: List[Event] = EventRepository().get(filter_form)

    return event_type_list_to_event_type_list(event_list)


@key_remover
def process_update_event(update_form: dict) -> None:
    """
    Processes a request to update an existing event.

    This function takes a dictionary `update_form` representing the update parameters for an event.
    If the event is a single event, the function calls `EventRepository().update_by_id()`
    method using the event ID and update dictionary.
    If the event is a recurring event, the `EventRepository().update_by_recurrance_id()`
    method is called instead.

    Args:
        update_form: A dictionary containing the event ID or recurrence ID and update dictionary.

    Returns:
        None. The function does not return anything.
    """

    if update_form.get("EventId"):
        EventRepository().update_by_id(
            update_form.get("EventId"), update_form.get("updateDictionary")
        )

    elif update_form.get("RecurranceId"):
        EventRepository().update_by_recurrance_id(
            update_form.get("RecurranceId"), update_form.get("updateDictionary")
        )


@key_remover
def process_delete_event(delete_form: dict) -> None:
    """
    Processes a request to delete an existing event.

    This function takes a dictionary `delete_form` representing the delete parameters
    for an event.
    The function then calls the `EventRepository().delete()` method with these parameters
    to delete the given event.

    Args:
        delete_form: A dictionary containing the event ID or recurrence ID that needs to
        be deleted.

    Returns:
         None. The function does not return anything.
    """

    EventRepository().delete(delete_form)
