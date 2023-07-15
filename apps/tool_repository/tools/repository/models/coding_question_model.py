"""
file_name = coding_question_model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the CodingQuestion model.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable

from sqlalchemy import (
    ARRAY,
    Column,
    Float,
    Boolean,
    Integer,
    String
)

from . import Base


class CodingQuestion(Base):
    """
        Represents a coding question for practice or assessment.

        Attributes:
        - QuestionId: The unique ID of the question.
        - QuestionLink: The link to the question.
        - QuestionName: The name of the question.
        - Difficulty: The difficulty level of the question.
        - AcceptanceRate: The acceptance rate of the question.
        - Tags: The tags associated with the question.
        - RequiresSubscription: A boolean indicating whether the question requires a subscription.
    """

    __tablename__ = "coding_questions"

    QuestionId = Column("QuestionId", String(64), primary_key=True)
    QuestionLink = Column("QuestionLink", String(256), nullable=True)
    QuestionName = Column("QuestionName", String(128), nullable=True)
    Difficulty = Column("Difficulty", String(32), nullable=True)
    AcceptanceRate = Column("AcceptanceRate", Float, nullable=True)
    Tags = Column("Tags", ARRAY(Integer), nullable=True)
    RequiresSubscription = Column("RequiresSubscription", Boolean, nullable=True)

    def __init__(self, question_information: dict) -> None:
        self.QuestionId = question_information.get("QuestionId")
        self.QuestionName = question_information.get("QuestionName")
        self.QuestionLink = question_information.get("QuestionLink")
        self.Difficulty = question_information.get("Difficulty")
        self.AcceptanceRate = question_information.get("AcceptanceRate")
        self.Tags = question_information.get("Tags")
        self.RequiresSubscription = question_information.get("RequiresSubscription")

    def to_dict(self) -> dict:
        return {
            "QuestionId": self.QuestionId,
            "QuestionLink": self.QuestionLink,
            "QuestionName": self.QuestionName,
            "Difficulty": self.Difficulty,
            "AcceptanceRate": self.AcceptanceRate,
            "Tags": self.Tags,
            "RequiresSubscription": self.RequiresSubscription,
        }
