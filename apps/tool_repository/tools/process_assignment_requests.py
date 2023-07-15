"""
file_name = process_assignment_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used for dealing with assignment requests.
Edit Log:
07/09/2023
-   Conformed to pylint conventions.
"""

from typing import List
from apps.tool_repository.tools.assignment_utils import (
    assignment_type_list_to_event_dict_list,
)

from apps.tool_repository.tools.repository.assignments import AssignmentRepository
from apps.tool_repository.tools.repository.models.assignment_model import Assignment


def process_create_assignment(assignment_data: dict) -> None:
    """
    Process a request to create a new assignment.

    This function takes a dictionary representing assignment data from a request and 
    inserts the data into the AssignmentRepository to create the new assignment.

    Args:
        assignment_data: A dictionary representing the assignment data from a request.

    Returns:
        None. The function does not return anything.
    """

    AssignmentRepository().insert(assignment_data)


def process_update_assignment(update_form: dict) -> None:
    """
    Process a request to update an existing assignment.

    This function takes a dictionary representing update data from a request and uses the
    data to update an existing assignment in the AssignmentRepository.

    Args:
        update_form: A dictionary representing the update data from a request. The required 
        fields are "AssignmentId" and "UpdateParams".

    Returns:
        None. The function does not return anything.
    """

    AssignmentRepository().update(
        update_form.get("AssignmentId"), update_form.get("UpdateParams")
    )


def process_get_assignment_request(filter_form: dict) -> List[dict]:
    """
    Process a request to get a list of assignments.

    This function takes a dictionary representing filter data from a request and uses the data 
    to retrieve a list of assignments from the AssignmentRepository.

    Args:
        filter_form: A dictionary representing the filter data from a request. The optional fields 
        are "UserId", "ClassId", "AssignmentId", "StartDate", "EndDate", and "Status".

    Returns:
        A list of dictionaries representing the retrieved assignments. 
        Each dictionary contains the fields "AssignmentId", "UserId", "ClassId", "StartDate", 
        "EndDate", and "Status".
    """

    assignment_list: List[Assignment] = AssignmentRepository().get(filter_form)

    return assignment_type_list_to_event_dict_list(assignment_list)


def process_delete_assignment_request(delete_form: dict) -> None:
    """
    Process a request to delete an assignment.

    This function takes a dictionary representing delete data from a request and uses the data to 
    delete an existing assignment from the AssignmentRepository.

    Args:
        delete_form: A dictionary representing the delete data from a request. The required fields 
        are "AssignmentId", "UserId", and "ClassId".

    Returns:
        None. The function does not return anything.
    """

    AssignmentRepository().delete(delete_form)
