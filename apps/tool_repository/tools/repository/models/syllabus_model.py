"""
file_name = syllabus_model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the Syllabus model.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable, too-many-instance-attributes

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Syllabus(Base):
    """
    Represents the syllabus for a specific class section.

    Attributes:
    - ClassId: The ID of the associated class.
    - SectionId: The unique ID of the syllabus section.
    - Section: The section name.
    - Percentage: The percentage weightage of the section.
    - Droppable: A flag indicating if the section is droppable.
    """

    __tablename__ = "syllabi"

    ClassId = Column("ClassId", ForeignKey("classes.ClassId", ondelete="CASCADE"))
    SectionId = Column("SectionId", String(64), primary_key=True)

    Section = Column("Section", String(64), nullable=False)
    Percentage = Column("Percentage", Integer, nullable=False)
    Droppable = Column("Droppable", Integer, nullable=False, default=0)

    Assignments = relationship(
        "Assignment",
        backref="syllabi",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __init__(self, syllabus_information: dict) -> None:
        self.ClassId = syllabus_information.get("ClassId")
        self.SectionId = syllabus_information.get("SectionId")
        self.Section = syllabus_information.get("Section")
        self.Percentage = syllabus_information.get("Percentage")
        self.Droppable = syllabus_information.get("Droppable")

    def to_dict(self) -> dict:
        return {
            "ClassId": self.ClassId,
            "SectionId": self.SectionId,
            "Section": self.Section,
            "Percentage": self.Percentage,
            "Droppable": self.Droppable,
        }
