from apps.tool_repository.tools.class_utils import (
    class_type_list_to_event_dict_list,
)  # pylint: disable=import-error, useless-option-value, nknown-option-value, unrecognized-option
from repository.models.class_model import Class

import pytest

from typing import List


@pytest.fixture
def class_one_dict() -> dict:
    return {
        "ClassId": None,
        "Department": "Circus",
        "CourseNumber": "101",
        "Professor": "Someone Real",
        "Name": "Introduction to the Circus",
        "Semester": "Test One",
    }


@pytest.fixture
def class_two_dict() -> dict:
    return {
        "ClassId": None,
        "Department": "Circus",
        "CourseNumber": "201",
        "Professor": "Someone Really Real",
        "Name": "Advanced Circus",
        "Semester": "Test Two",
    }


@pytest.fixture
def my_classes(class_one_dict, class_two_dict) -> List[Class]:
    return [Class(class_one_dict), Class(class_two_dict)]


def test_type_list_to_event_dict_list(
    my_classes: List[Class], class_one_dict, class_two_dict
):
    classes_list = class_type_list_to_event_dict_list(my_classes)

    assert len(classes_list) == len(my_classes)
    assert classes_list[0] == class_one_dict
    assert classes_list[1] == class_two_dict
