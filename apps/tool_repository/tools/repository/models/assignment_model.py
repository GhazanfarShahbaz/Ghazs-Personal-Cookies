from . import Base 

from sqlalchemy import ARRAY, Column, DateTime, JSON, Integer, String, ForeignKey, Boolean

class Assignment(Base):
    __tablename__ = "assignments"

    SectionId = Column("SectionId", ForeignKey(
        "syllabi.SectionId", ondelete="CASCADE"))
    AssignmentId = Column("AssignmentId", Integer,
                          autoincrement=True, primary_key=True)

    Name = Column("Name", String(64), nullable=False)
    Grade = Column("Grade", Integer, nullable=False)
    DateAssigned = Column("DateAssigned", DateTime(
        timezone=True), nullable=True)
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