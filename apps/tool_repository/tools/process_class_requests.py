"""
file_name = process_class_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used for handling class requests
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

from typing import List
from apps.tool_repository.tools.class_utils import class_type_list_to_event_dict_list

from repository.models.class_model import Class
from repository.classes import ClassRepository


def process_create_class(class_data: dict) -> None:
    """
    Processes a request to create a new class.

    This function takes a dictionary representing class data from a request and inserts
    the data into the ClassRepository to create the new class.

    Args:
        class_data: A dictionary representing the class data from a request.

    Returns:
        None. The function does not return anything.
    """

    ClassRepository().insert(class_data)


def process_update_class(update_form: dict) -> None:
    """
    Processes a request to update an existing class.

    This function takes a dictionary representing update data from a request and uses the
    ata to update an existing class in the ClassRepository.

    Args:
        update_form: A dictionary representing the update data from a request. The required
        fields are "ClassId" and "UpdateParams".

    Returns:
        None. The function does not return anything.
    """

    ClassRepository().update(
        update_form.get("ClassId"), update_form.get("UpdateParams")
    )


def process_get_class_request(filter_form: dict) -> List[dict]:
    """
    Processes a request to retrieve a list of classes.

    This function takes a dictionary representing filter data from a request and uses the
    data to retrieve a list of classes from the ClassRepository.

    Args:
        filter_form: A dictionary representing the filter data from a request. The optional
        fields are "UserId", "ClassId", "Name", "StartDate", "EndDate", "Status".

    Returns:
        A list of dictionaries, where each dictionary represents a single class and contains
        the fields "ClassId", "UserId", "Name", "StartDate", "EndDate", and "Status".
    """

    class_list: List[Class] = ClassRepository().get(filter_form)
    return class_type_list_to_event_dict_list(class_list)


def process_delete_class_request(delete_form: dict) -> None:
    """
    Processes a request to delete a class.

    This function takes a dictionary representing delete data from a request and uses the data
    to delete an existing class from the ClassRepository.

    Args:
        delete_form: A dictionary representing the delete data from a request. The required fields
        are "ClassId", "UserId", and "Name".

    Returns:
        None. The function does not return anything.
    """

    ClassRepository().delete(delete_form)
