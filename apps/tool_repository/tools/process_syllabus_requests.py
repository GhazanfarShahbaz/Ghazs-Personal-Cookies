"""
file_name = process_syllabus_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to process syllabus requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""


from typing import List

from apps.tool_repository.tools.syllabus_utils import (
    syllabus_type_list_to_event_dict_list,
)

from repository.syllabi import SyllabusRepository
from repository.models.syllabus_model import Syllabus


def process_create_syllabus(syllabus_data: dict) -> None:
    """
    Processes a request to create a new syllabus.

    This function takes a dictionary `syllabus_data` representing the syllabus data
    from a request and creates a new syllabus in the syllabus repository.

    Args:
        syllabus_data: A dictionary containing the syllabus data.

    Returns:
        None. The function does not return anything.
    """

    SyllabusRepository().insert(syllabus_data)


def process_update_syllabus(update_form: dict) -> None:
    """
    Processes a request to update an existing syllabus.

    This function takes a dictionary `update_form` representing the update parameters
    for a syllabus.
    The function then calls the `SyllabusRepository().update()` method with these parameters
    to update the syllabus in the syllabus repository.

    Args:
        update_form: A dictionary containing the syllabus ID and update parameters.

    Returns:
        None. The function does not return anything.
    """

    SyllabusRepository().insert(  # pylint: disable=too-many-function-args
        update_form.get("SyllabusId"), update_form.get("UpdateParams")
    )


def process_get_syllabus_request(filter_form: dict) -> List[dict]:
    """
    Processes a request to retrieve a list of syllabuses that match the given filter.

    This function takes a dictionary `filter_form` representing the filter parameters for a
    syllabus request, and calls the `SyllabusRepository().get()` method with these parameters
    to retrieve a list of syllabuses that match the filter.
    The returned syllabuses are then converted to a list of dictionaries using the
    `syllabus_type_list_to_event_dict_list()` function.

    Args:
        filter_form: A dictionary containing the filter parameters for the request.

    Returns:
        A list of dictionaries representing the retrieved syllabuses. Each dictionary contains
        the fields "SyllabusId", "Name", "CourseCode", "CourseTitle", "Instructor", and "Syllabus".
    """

    syllabus_list: List[Syllabus] = SyllabusRepository().get(filter_form)

    return syllabus_type_list_to_event_dict_list(syllabus_list)


def process_delete_syllabus_request(delete_form: dict) -> None:
    """
    Processes a request to delete an existing syllabus.

    This function takes a dictionary `delete_form` representing the delete parameters for a
    syllabus request.
    The function then calls the `SyllabusRepository().delete()` method with these parameters to
    delete the given syllabus from the syllabus repository.

    Args:
        delete_form: A dictionary containing the syllabus ID or course code that needs to be
        deleted.

    Returns:
         None. The function does not return anything.
    """

    SyllabusRepository().delete(delete_form)
