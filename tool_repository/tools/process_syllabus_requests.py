from typing import List
from syllabus_utils import syllabus_type_list_to_event_dict_list
from repository.syllabi import SyllabusRepository
from repository.model import Syllabus

def process_create_syllabus(syllabus_data: dict) -> None: 
    SyllabusRepository().insert(syllabus_data)


def process_update_syllabus(update_form: dict) -> None:
    SyllabusRepository().insert(update_form.get("SyllabusId"), update_form.get("UpdateParams"))


def process_get_syllabus_request(filter_form: dict) -> List[dict]:
    syllabus_list: List[Syllabus] = SyllabusRepository().get(filter_form)

    return syllabus_type_list_to_event_dict_list(syllabus_list)


def process_delete_event_request(delete_form: dict) -> None: 
    SyllabusRepository().delete(delete_form)