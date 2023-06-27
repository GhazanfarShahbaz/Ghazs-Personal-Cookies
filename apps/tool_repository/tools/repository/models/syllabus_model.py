from sqlalchemy import ARRAY, Column, DateTime, JSON, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Syllabus(Base):
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
