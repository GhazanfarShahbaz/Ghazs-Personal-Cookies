from typing import List
from grade_utils import grade_type_list_to_event_dict_list
from repository.syllabi import GradeRepository
from repository.model import Grade

def process_create_grade(grade_data: dict) -> None: 
    GradeRepository().insert(grade_data)


def process_update_grade(update_form: dict) -> None:
    GradeRepository().insert(update_form.get("GradeId"), update_form.get("UpdateParams"))


def process_get_grade_request(filter_form: dict) -> List[dict]:
    grade_list: List[Grade] = GradeRepository().get(filter_form)

    return grade_type_list_to_event_dict_list(grade_list)


def process_delete_event_request(delete_form: dict) -> None: 
    GradeRepository().delete(delete_form)