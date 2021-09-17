from typing import List
from assignment_utils import assignment_type_list_to_event_dict_list
from repository.assignments import AssignmentRepository
from repository.model import Assignment

def process_create_assignment(assignment_data: dict) -> None: 
    AssignmentRepository().insert(assignment_data)


def process_update_assignment(update_form: dict) -> None:
    AssignmentRepository().insert(update_form.get("AssignmentId"), update_form.get("UpdateParams"))


def process_get_assignment_request(filter_form: dict) -> List[dict]:
    assignment_list: List[Assignment] = AssignmentRepository().get(filter_form)

    return assignment_type_list_to_event_dict_list(assignment_list)


def process_delete_assignment_request(delete_form: dict) -> None: 
    AssignmentRepository().delete(delete_form)