from apps.tool_repository.tools.assignment_utils import assignment_type_list_to_event_dict_list  # pylint: disable=import-error, useless-option-value, nknown-option-value, unrecognized-option
from apps.tool_repository.tools.repository.model import Assignment

import pytest 

from datetime import datetime
from typing import List

@pytest.fixture
def my_assignments():
    return [
        Assignment({
            "ClassId": 1,
            "Grade": 100,
            "DateAssigned": datetime(2022, 10, 18, 2, 30),
            "DateDue": datetime(2022, 10, 19, 11, 59),
            "Submitted": True   
        }),
        Assignment({
            "ClassId": 2,
            "Grade": 100,
            "DateAssigned": datetime(2022, 9, 18, 2, 30),
            "DateDue": datetime(2022, 9, 19, 11, 59),
            "Submitted": False   
        })
    ]
    
def test_type_list_to_event_dict_list(my_assignments: List[Assignment]):
    assignment_list = assignment_type_list_to_event_dict_list(my_assignments)
    
    assert len(assignment_list) == len(my_assignments)
    assert assignment_list[0] == {
            "ClassId": 1,
            "AssignmentId": None,
            "Grade": 100,
            "DateAssigned": datetime(2022, 10, 18, 2, 30),
            "DateDue": datetime(2022, 10, 19, 11, 59),
            "Submitted": True   
        }
    
    assert assignment_list[1] == {
            "ClassId": 2,
            "AssignmentId": None,
            "Grade": 100,
            "DateAssigned": datetime(2022, 9, 18, 2, 30),
            "DateDue": datetime(2022, 9, 19, 11, 59),
            "Submitted": False   
        }