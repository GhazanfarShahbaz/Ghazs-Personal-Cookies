from sqlalchemy.orm import Session, Query
from typing import List

from apps.tool_repository.tools.repository.models.model import Session as Sess
from apps.tool_repository.tools.repository.models.class_model import Class
from apps.tool_repository.tools.repository.models.syllabus_model import Syllabus


class SyllabusRepository(object):
    def __init__(self):
        self.session: Session = Sess()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.session.close()

    def insert(self, syllabus: Syllabus) -> int:
        self.session.add(syllabus)
        self.session.commit()
        return syllabus.SectionId

    def update(self, section_id: int, update_dictionary: dict) -> None:
        syllabus: Syllabus = self.session.query(Syllabus).filter(
            Syllabus.SectionId == section_id).first()

        if update_dictionary.get("Section"):
            syllabus.Section = update_dictionary["Section"]

        if update_dictionary.get("Percentage"):
            syllabus.Percentage = update_dictionary["Percentage"]

        if update_dictionary.get("Droppable"):
            syllabus.Droppable = update_dictionary["Droppable"]

        self.session.commit()

    def get(self, filters: dict) -> List[Syllabus]:
        query: Query = self.session.query(Syllabus).join(
            Class, Class.ClassId == Syllabus.ClassId)

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("ClassName"):
            if filters.get("ClassNameExact") is None or filters["ClassNameExact"] is True:
                query = query.filter(Class.Name == filters["ClassName"])
            else:
                query = query.filter(Class.Name.like(filters["ClassName"]))

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Droppable"):
            query = query.filter(Syllabus.Droppable == filters["Droppable"])

        if filters.get("Section"):
            if filters.get("SectionExact") is None or filters["SectionExact"] is True:
                query = query.filter(Syllabus.Section == filters["Section"])
            else:
                query = query.filter(Syllabus.Section.like(filters["Section"]))

        return query.all()

    def delete(self, filters: dict) -> List[Syllabus]:
        query: Query = self.session.query(Syllabus).join(
            Class, Class.ClassId == Syllabus.ClassId)

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("ClassName"):
            if filters.get("ClassNameExact") is None or filters["ClassNameExact"] is True:
                query = query.filter(Class.Name == filters["ClassName"])
            else:
                query = query.filter(Class.Name.like(filters["ClassName"]))

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Droppable"):
            query = query.filter(Syllabus.Droppable == filters["Droppable"])

        if filters.get("Section"):
            if filters.get("SectionExact") is None or filters["SectionExact"] is True:
                query = query.filter(Syllabus.Section == filters["Section"])
            else:
                query = query.filter(Syllabus.Section.like(filters["Section"]))

        query.delete()
        self.session.commit()
