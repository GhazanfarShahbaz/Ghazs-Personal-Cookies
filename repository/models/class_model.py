"""
file_name = class_model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the class model.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable

from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from . import Base


class Class(Base):
    """
    Represents a class in a university.

    Attributes:
    - ClassId: The unique ID of the class.
    - Department: The department of the class.
    - CourseNumber: The course number of the class.
    - Professor: The professor teaching the class.
    - Name: The name of the class.
    - Semester: The semester in which the class is being taught.
    """

    __tablename__ = "classes"

    ClassId = Column("ClassId", Integer, primary_key=True, autoincrement=True)

    Department = Column("Department", String(128), nullable=False)
    CourseNumber = Column("CourseNumber", Integer, nullable=False)
    Professor = Column("Professor", String(128), nullable=False)
    Name = Column("Name", String(128), nullable=False)
    Semester = Column("Semester", String(128), nullable=False)

    Syllabus = relationship(
        "Syllabus",
        backref="classes",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __init__(self, class_inforamtion: dict) -> None:
        self.Department = class_inforamtion.get("Department")
        self.CourseNumber = class_inforamtion.get("CourseNumber")
        self.Professor = class_inforamtion.get("Professor")
        self.Name = class_inforamtion.get("Name")
        self.Semester = class_inforamtion.get("Semester")

    def to_dict(self) -> dict:
        return {
            "ClassId": self.ClassId,
            "Department": self.Department,
            "CourseNumber": self.CourseNumber,
            "Professor": self.Professor,
            "Name": self.Name,
            "Semester": self.Semester,
        }
