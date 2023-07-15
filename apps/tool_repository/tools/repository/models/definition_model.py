"""
file_name = definition_model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the Definition model.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text
)

from . import Base


class Definition(Base):
    """
    Represents a definition for a programming concept.

    Attributes:
    - DefinitionId: The unique ID of the definition.
    - ClassName: The name of the class associated with the definition.
    - FileName: The name of the file related to the definition.
    - Definition: The actual definition text.
    """

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
