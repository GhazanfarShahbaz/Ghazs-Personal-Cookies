"""
file_name = syllabus_utils.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/09/2023
Description: A module used for syllabus assignment objects. 
Edit Log:
07/09/2023
-   Conformed to pylint conventions.
"""

from typing import List

from apps.tool_repository.tools.repository.models.syllabus_model import Syllabus


def syllabus_type_list_to_event_dict_list(syllabus_list: List[dict]) -> List[Syllabus]:
    """
    Converts a list of syllabus dictionaries to a list of Syllabus objects.

    This function takes a list `syllabus_list` of syllabus dictionaries and creates a new list of Syllabus objects.

    Args:
        syllabus_list: A list of dictionaries representing syllabuses.

    Returns:
        A list of Syllabus objects.
    """

    return [syllabus.to_dict() for syllabus in syllabus_list]
