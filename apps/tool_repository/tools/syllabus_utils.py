from typing import List

from apps.tool_repository.tools.repository.models.syllabus_model import Syllabus


def syllabus_type_list_to_event_dict_list(syllabus_list: List[dict]) -> List[Syllabus]:
    return [syllabus.to_dict() for syllabus in syllabus_list]
