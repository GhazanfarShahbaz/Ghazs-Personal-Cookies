from sqlalchemy.orm import Session, Query
from typing import List

from apps.tool_repository.tools.repository.models.model import Session as Sess
from apps.tool_repository.tools.repository.models.class_model import Class

class ClassRepository(object):
    def __init__(self):
        self.session: Session = Sess()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.session.close()

    def insert(self, _class_: Class) -> int:
        self.session.add(_class_)
        self.session.commit()
        return _class_.ClassId

    def update(self, class_id: int, update_dictionary: dict) -> None:
        _class_: Class = self.session.query(Class).filter(
            Class.ClassId == class_id).first()

        if update_dictionary.get("Department"):
            _class_.Department = update_dictionary["Department"]

        if update_dictionary.get("CourseNumber"):
            _class_.CourseNumber = update_dictionary["Course Number"]

        if update_dictionary.get("Professor"):
            _class_.Professor = update_dictionary["Professor"]

        if update_dictionary.get("Name"):
            _class_.Name = update_dictionary["Name"]

        if update_dictionary.get("Semester"):
            _class_.Semester = update_dictionary["Semester"]

        self.session.commit()

    def get(self, filters: dict) -> List[Class]:
        query: Query = self.session.query(Class)

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("Department"):
            query = query.filter(Class.Department == filters["Department"])

        if filters.get("CourseNumber"):
            query = query.filter(Class.CourseNumber == filters["CourseNumber"])

        if filters.get("Professor"):
            query = query.filter(Class.Professor == filters["Professor"])

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Class.Name == filters["Name"])
            else:
                query = query.filter(Class.Name.like(filters["Name"]))

        if filters.get("Semester"):
            query = query.filter(Class.Semester == filters["Semester"])

        return query.all()

    def delete(self, filters: dict) -> None:
        query: Query = self.session.qeury(Class)
        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("Department"):
            query = query.filter(Class.Department == filters["Department"])

        if filters.get("CourseNumber"):
            query = query.filter(Class.CourseNumber == filters["CourseNumber"])

        if filters.get("Professor"):
            query = query.filter(Class.Professor == filters["Professor"])

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Class.Name == filters["Name"])
            else:
                query = query.filter(Class.Name.like(filters["Name"]))

        if filters.get("Semester"):
            query = query.filter(Class.Semester == filters["Semester"])

        query.delete()
        self.session.commit()
