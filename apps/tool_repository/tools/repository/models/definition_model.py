from sqlalchemy import ARRAY, Column, DateTime, JSON, Integer, String, Text

from . import Base


class Definition(Base):
    __tablename__ = "definitions"

    DefinitionId = Column("DefinitionId", Integer, autoincrement=True, primary_key=True)

    ClassName = Column("ClassName", String(128), nullable=False)
    FileName = Column("FileName", String(128), nullable=False)
    Definition = Column("Definition", Text, nullable=True)

    def __init__(self, assignment_information: dict) -> None:
        self.DefinitionId = assignment_information.get("DefinitionId")
        self.ClassName = assignment_information.get("ClassName")
        self.FileName = assignment_information.get("FileName")
        self.Definition = assignment_information.get("Definition")

    def to_dict(self) -> dict:
        return {
            "DefinitionId": self.DefinitionId,
            "ClassName": self.ClassName,
            "FileName": self.FileName,
            "Definition": self.Definition,
        }
