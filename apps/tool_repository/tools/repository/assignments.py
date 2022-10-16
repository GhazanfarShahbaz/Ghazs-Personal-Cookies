from model import Session as Sess, Assignment, Syllabus, Class
from sqlalchemy.orm import Session, Query
from typing import List


class AssignmentRepository(object):
    def __init__(self):
        self.session: Session = Sess()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.session.close()

    def insert(self, assignment: Assignment) -> int:
        self.session.add(assignment)
        self.session.commit()
        return assignment.AssignmentId

    def update(self, assignment_id: int, update_dictionary: dict) -> int:
        assignment = self.session.query(Assignment).filter(
            Assignment.AssignmentId == assignment_id).first()

        if update_dictionary.get("Name"):
            assignment.Name = update_dictionary["Name"]

        if update_dictionary.get("Grade"):
            assignment.Grade = update_dictionary["Grade"]

        if update_dictionary.get("DateAssigned"):
            assignment.DateAssigned = update_dictionary["DateAssigned"]

        if update_dictionary.get("DateDue"):
            assignment.DateDue = update_dictionary["DateDue"]

        if update_dictionary.get("Submitted"):
            assignment.Submitted = update_dictionary["Submitted"]

        self.session.commit()

    def get(self, filters: dict) -> List[Assignment]:
        query: Query = self.session.query(Assignment).join(
            Syllabus, Syllabus.SectionId == Assignment.SectionId).join(Class, Class.ClassId == Syllabus.ClassId)

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("ClassName"):
            if filters.get("ClassNameExact") is None or filters["ClassNameExact"] is True:
                query = query.filter(Class.Name == filters["ClassName"])
            else:
                query = query.filter(Class.Name.like(filters["ClassName"]))

        if filters.get("DateAssigned"):
            query = query.filter(Assignment.DateAssigned ==
                                 filters["DateAssigned"])

        if filters.get("DateDue"):
            query = query.filter(Assignment.DateDue == filters["DateDue"])

        if filters.get("Submitted"):
            query = query.filter(Assignment.Submitted == filters["Submitted"])

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Section"):
            if filters.get("SectionExact") is None or filters["SectionExact"] is True:
                query = query.filter(Syllabus.Section == filters["Section"])
            else:
                query = query.filter(Syllabus.Section.like(filters["Section"]))

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Assignment.Name == filters["Name"])
            else:
                query = query.filter(Assignment.Name.like(filters["Name"]))

        return query.all()

    def delete(self, filters: dict) -> None:
        query: Query = self.session.query(Assignment).join(
            Syllabus, Syllabus.SectionId == Assignment.SectionId).join(Class, Class.ClassId == Syllabus.ClassId)

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("ClassName"):
            if filters.get("ClassNameExact") is None or filters["ClassNameExact"] is True:
                query = query.filter(Class.Name == filters["ClassName"])
            else:
                query = query.filter(Class.Name.like(filters["ClassName"]))

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Section"):
            if filters.get("SectionExact") is None or filters["SectionExact"] is True:
                query = query.filter(Syllabus.Section == filters["Section"])
            else:
                query = query.filter(Syllabus.Section.like(filters["Section"]))

        if filters.get("DateDue"):
            query = query.filter(Assignment.DateDue == filters["DateDue"])

        if filters.get("Submitted"):
            query = query.filter(Assignment.Submitted == filters["Submitted"])

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Assignment.Name == filters["Name"])
            else:
                query = query.filter(Assignment.Name.like(filters["Name"]))

        query.delete()
        self.session.commit()
