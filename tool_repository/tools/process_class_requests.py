from typing import List 
from class_utils import class_type_list_to_event_dict_list
from repository.model import Class
from repository.classes import ClassRepository


def process_create_class(class_data: dict) -> None: 
    ClassRepository().insert(class_data)


def process_update_class(update_form: dict) -> None:
    ClassRepository().insert(update_form.get("ClassId"), update_form.get("UpdateParams"))


def process_get_class_request(filter_form: dict) -> List[dict]:
    class_list: List[Class] = ClassRepository().get(filter_form)

    return class_type_list_to_event_dict_list(class_list)


def process_delete_event_request(delete_form: dict) -> None: 
    ClassRepository().delete(delete_form)