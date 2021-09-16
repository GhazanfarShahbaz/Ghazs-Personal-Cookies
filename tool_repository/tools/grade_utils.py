from typing import List 

from repository.model import Grade 

def grade_type_list_to_event_dict_list(grade_list: List[dict]) -> List[Grade]:
    return [grade.to_dict() for grade in grade_list]