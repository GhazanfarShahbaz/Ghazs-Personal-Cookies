from typing import List

from repository.model import Assignment


def assignment_type_list_to_event_dict_list(assignment_list: List[dict]) -> List[Assignment]:
    """
    Turns assignment type lists into an event dictionary list
    Returns:
        List[Assignment]: A list of Assignments
    """
    
    return [assignment.to_dict() for assignment in assignment_list]
