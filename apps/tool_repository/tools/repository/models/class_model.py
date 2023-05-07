from sqlalchemy import ARRAY, Boolean, Column, DateTime, JSON, Float, Integer, String, Text, ForeignKey
from sqlalchemy.orm import  relationship

from . import Base 

class Class(Base):
    __tablename__ = "classes"

    ClassId = Column("ClassId", Integer, primary_key=True, autoincrement=True)

    Department = Column("Department", String(128), nullable=False)
    CourseNumber = Column("CourseNumber", Integer, nullable=False)
    Professor = Column("Professor", String(128), nullable=False)
    Name = Column("Name", String(128), nullable=False)
    Semester = Column("Semester", String(128), nullable=False)

    Syllabus = relationship("Syllabus", backref="classes",
                            cascade="all, delete-orphan", passive_deletes=True)

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