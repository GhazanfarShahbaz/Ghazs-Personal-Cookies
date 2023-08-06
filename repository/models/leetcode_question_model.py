"""
file_name = leetcode_question_model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the LeetCodeQuestion model.
Edit Log:
07/14/2023
-   Moved over from leetcode bot repository
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable, too-many-instance-attributes

from sqlalchemy import Column, Boolean, Float, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from . import Base


class LeetCodeQuestion(Base):
    """
    Model representing a LeetCode question in a SQL database.

    Attributes:
        number (int): The unique identifier of the question on LeetCode.
        name (str): The name of the LeetCode question.
        subscription (bool): Whether or not the question requires a subscription to access.
        link (str): The LeetCode URL for the question.
        acceptance (float): The percentage of submissions that receive an accepted answer.
        difficulty (str): The difficulty level of the question (Easy, Medium, or Hard).
        tags (List[str]): The categories of the question (e.g. Array, Hash Table, etc.).
    """

    __tablename__ = "leetcode_questions"

    number = Column(Integer, primary_key=True)
    name = Column(String(156))
    subscription = Column(Boolean)
    link = Column(String(156))
    acceptance = Column(Float)
    difficulty = Column(String(32))
    tags = Column(ARRAY(String), server_default="{}")

    def __init__(self, question_information):
        """
        Initializes a new instance of the LeetCodeQuestion class.

        Args:
            question_information (dict): A dictionary containing attribute values
                                         for the LeetCodeQuestion object.
        """
        self.number = question_information["number"]
        self.name = question_information["name"]
        self.subscription = question_information["subscription"]
        self.link = question_information["link"]
        self.acceptance = question_information["acceptance"]
        self.difficulty = question_information["difficulty"]
        self.tags = question_information["tags"]

    def to_dict(self):
        """
        Convert the LeetCodeQuestion object to a dictionary.

        Returns:
            dict: A dictionary representation of the LeetCodeQuestion object.
        """
        return {
            "number": self.number,
            "name": self.name,
            "subscription": self.subscription,
            "link": self.link,
            "acceptance": self.acceptance,
            "difficulty": self.difficulty,
            "tags": self.tags,
        }
