from typing import List

from repository.model import Class


def class_type_list_to_event_dict_list(class_list: List[dict]) -> List[Class]:
    return [_class.to_dict() for _class in class_list]
