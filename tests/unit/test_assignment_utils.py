from apps.tool_repository.tools.assignment_utils import (
    assignment_type_list_to_event_dict_list,
)  # pylint: disable=import-error, useless-option-value, nknown-option-value, unrecognized-option
from repository.models.assignment_model import Assignment

import pytest

from datetime import datetime
from typing import List


@pytest.fixture
def assignment_one_dict():
    return {
        "ClassId": 1,
        "AssignmentId": None,
        "Grade": 100,
        "DateAssigned": datetime(2022, 10, 18, 2, 30),
        "DateDue": datetime(2022, 10, 19, 11, 59),
        "Submitted": True,
    }


@pytest.fixture
def assignment_two_dict():
    return {
        "ClassId": 2,
        "AssignmentId": None,
        "Grade": 100,
        "DateAssigned": datetime(2022, 9, 18, 2, 30),
        "DateDue": datetime(2022, 9, 19, 11, 59),
        "Submitted": False,
    }


@pytest.fixture
def my_assignments(assignment_one_dict, assignment_two_dict):
    return [Assignment(assignment_one_dict), Assignment(assignment_two_dict)]


def test_type_list_to_event_dict_list(
    my_assignments: List[Assignment], assignment_one_dict, assignment_two_dict
):
    assignment_list = assignment_type_list_to_event_dict_list(my_assignments)

    assert len(assignment_list) == len(my_assignments)
    assert assignment_list[0] == assignment_one_dict
    assert assignment_list[1] == assignment_two_dict
