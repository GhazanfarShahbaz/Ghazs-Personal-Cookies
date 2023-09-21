"""
file_name = class_utils.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/09/2023
Description: A module used for database class objects. 
Edit Log:
07/09/2023
-   Conformed to pylint conventions.
"""

from typing import List

from repository.models.class_model import Class


def class_type_list_to_event_dict_list(class_list: List[Class]) -> List[dict]:
    """
    Converts a list of Class objects to a list of dictionaries.

    This function takes a list of Class objects and converts them to a list of dictionaries.
    Each dictionary represents an event and contains the information about the class
    for that event.

    Args:
        class_list: A list of Class objects to be converted.

    Returns:
        A list of dictionaries, with each dictionary representing an event.

    Raises:
        TypeError: If the input list contains objects that are not of type Class.
    """

    if not all(isinstance(_class, Class) for _class in class_list):
        raise TypeError("All items in the list must be of type `Class`")

    return [_class.to_dict() for _class in class_list]
