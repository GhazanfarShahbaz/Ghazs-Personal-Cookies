from typing import List

from repository.events import EventRepository
from repository.model import Event

from event_utils import create_event_information, event_type_list_to_event_type_list

def process_create_event(event_data: dict) -> None:
    event_list: List[Event] = create_event_information(event_data)
    
    EventRepository().insert(event_list)

def process_get_event(filter_form: dict) -> List[dict]:
    event_list: List[Event] = EventRepository().get(filter_form)
    return event_type_list_to_event_type_list(event_list)

def process_update_event(update_form: dict) -> None:
    if update_form.get("EventId"):
        EventRepository().update_by_id(update_form.get("EventId"), update_form.get("updateDictionary"))
    elif update_form.get("RecurranceId"):
        EventRepository().update_by_recurrance_id(update_form.get("RecurranceId"), update_form.get("updateDictionary"))

def process_delete_event(delete_form: dict) -> None:
    EventRepository().delete(delete_form)
