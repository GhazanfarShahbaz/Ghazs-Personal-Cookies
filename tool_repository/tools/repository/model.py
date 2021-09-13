from sqlalchemy import (Boolean, Column, DateTime, Integer, String,
                        create_engine, Text, ForeignKey)
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null


def get_engine() -> Engine:
    engine: Engine = create_engine('mysql://doadmin:xwP23NrI_qxocdyg@db-mysql-ghaz-do-user-8116866-0.b.db.ondigitalocean.com:25060/defaultdb')

    return engine


Engine: Engine = get_engine()
Session = sessionmaker(Engine)
Base = declarative_base()


class Event(Base):  # was originally Events
    __tablename__ = "events"

    EventId = Column("EventId", Integer, primary_key=True, autoincrement=True)
    ReccuranceId = Column("RecurranceId", Integer, nullable=True)

    Name = Column("Name", String(256), nullable=False)
    StartDate = Column("StartDate", DateTime, nullable=False)
    EndDate = Column("EndDate", DateTime, nullable=False)
    Type = Column("Type", String(32), nullable=False)
    Location = Column("Location", String(1024), nullable=False)
    ReccuranceType = Column("ReccurranceType", String(64), nullable=True)
    Description = Column("Description", String(512), nullable=True)

    def __init__(self, event_information: dict) -> None:
        self.ReccuranceId = event_information.get("ReccuranceId")
        self.Name = event_information.get("Name")
        self.StartDate = event_information.get("StartDate")
        self.EndDate = event_information.get("EndDate")
        self.Location = event_information.get("Location")
        self.Type = event_information.get("Type")
        self.ReccuranceType = event_information.get("ReccuranceType")
        self.Description = event_information.get("Description")
    
    def to_dict(self) -> dict:
        return {
            "Id": self.EventId,
            "ReccuranceId": self.ReccuranceId,
            "Name": self.Name,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "Type": self.Type,
            "Description": self.Description,
            "ReccuranceType": self.ReccuranceType
        }

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


class Syllabus(Base):
    __tablename__ = "syllabi"

    ClassId = Column("ClassId", ForeignKey(
        "classes.ClassId", ondelete="CASCADE"))
    SectionId = Column("SectionId", String(64), primary_key=True)

    Section = Column("Section", String(64), nullable=False)
    Percentage = Column("Percentage", Integer, nullable=False)
    Droppable = Column("Droppable", Integer, nullable=False, default=0)

    Assignments = relationship(
        "Assignment", backref="syllabi", cascade="all, delete-orphan", passive_deletes=True)


class Assignment(Base):
    __tablename__ = "assignments"

    SectionId = Column("SectionId", ForeignKey(
        "syllabi.SectionId", ondelete="CASCADE"))
    AssignmentId = Column("AssignmentId", Integer,
                          autoincrement=True, primary_key=True)


    Name = Column("Name", String(64), nullable=False)
    Grade = Column("Grade", Integer, nullable=False)
    DateAssigned = Column("DateAssigned", DateTime, nullable=True)
    DateDue = Column("DateDue", DateTime, nullable=True)
    Submitted = Column("Submitted", Boolean, nullable=False, default=False)


class Definition(Base):
    __tablename__ = "definitions"
    
    DefinitionId = Column("DefinitionId", Integer, autoincrement=True, primary_key=True)
    
    ClassName = Column("ClassName", String(128), nullable=False)
    FileName = Column("FileName", String(128), nullable=False)
    Definition = Column("Definition", Text, nullable=True)


def init_db():
    global Base, Engine
    Base.metadata.create_all(bind=Engine)
    print("Created Model")
