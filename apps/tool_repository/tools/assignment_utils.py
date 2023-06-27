from typing import List

from apps.tool_repository.tools.repository.models.assignment_model import Assignment


def assignment_type_list_to_event_dict_list(
    assignment_list: List[Assignment],
) -> List[dict]:
    """
    Converts a list of Assignment objects to a list of dictionaries.

    This function takes a list of Assignment objects and converts them to a list of dictionaries.
    Each dictionary represents an event and contains the information about the assignment for
    that event.

    Args:
        assignment_list: A list of Assignment objects to be converted.

    Returns:
        A list of dictionaries, with each dictionary representing an event.

    Raises:
        TypeError: If the input list contains objects that are not of type Assignment.
    """

    if not all(isinstance(assignment, Assignment) for assignment in assignment_list):
        raise TypeError("All items in the list must be of type `Assignment`")

    return [assignment.to_dict() for assignment in assignment_list]
