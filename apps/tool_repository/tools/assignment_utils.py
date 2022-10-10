from typing import List

from repository.model import Assignment


def assignment_type_list_to_event_dict_list(assignment_list: List[dict]) -> List[Assignment]:
    return [assignment.to_dict() for assignment in assignment_list]
