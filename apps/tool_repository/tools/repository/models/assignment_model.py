"""
file_name = assignment_model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the Assigment model.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Boolean,
)

from . import Base


class Assignment(Base):
    """
    Represents an assignment in a syllabus section.

    Attributes:
    - SectionId: The ID of the section the assignment belongs to.
    - AssignmentId: The unique ID of the assignment.
    - Name: The name of the assignment.
    - Grade: The grade of the assignment.
    - DateAssigned: The date when the assignment was assigned.
    - DateDue: The due date of the assignment.
    - Submitted: A boolean indicating whether the assignment has been submitted.
    """

    __tablename__ = "assignments"

    SectionId = Column("SectionId", ForeignKey("syllabi.SectionId", ondelete="CASCADE"))
    AssignmentId = Column("AssignmentId", Integer, autoincrement=True, primary_key=True)

    Name = Column("Name", String(64), nullable=False)
    Grade = Column("Grade", Integer, nullable=False)
    DateAssigned = Column("DateAssigned", DateTime(timezone=True), nullable=True)
    DateDue = Column("DateDue", DateTime(timezone=True), nullable=True)
    Submitted = Column("Submitted", Boolean, nullable=False, default=False)

    def __init__(self, assignment_information: dict) -> None:
        self.SectionId = assignment_information.get("ClassId")
        self.Grade = assignment_information.get("Grade")
        self.DateAssigned = assignment_information.get("DateAssigned")
        self.DateDue = assignment_information.get("DateDue")
        self.Submitted = assignment_information.get("Submitted")

    def to_dict(self) -> dict:
        return {
            "ClassId": self.SectionId,
            "AssignmentId": self.AssignmentId,
            "Grade": self.Grade,
            "DateAssigned": self.DateAssigned,
            "DateDue": self.DateDue,
            "Submitted": self.Submitted,
        }
