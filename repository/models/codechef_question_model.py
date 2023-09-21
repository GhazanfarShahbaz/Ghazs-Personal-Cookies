"""
file_name = codechef_question_model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the CodeChefQuestion model.
Edit Log:
07/14/2023
-   Moved over from leetcode bot repository
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable, too-many-instance-attributes

from sqlalchemy import Column, Integer, String, Float

from . import Base


class CodeChefQuestion(Base):
    """
    Model representing a CodeChef question in a SQL database.

    Attributes:
        id (int): The unique identifier of the question.
        name (str): The name of the CodeChef question.
        link (str): The CodeChef URL for the question.
        submit_link (str): The CodeChef URL to submit solutions to the question.
        submitted_solutions (int): The number of solutions submitted to the question.
        accuracy (float): The percentage of solutions submitted to the question that are correct.
        status_link (str): The CodeChef URL to view the status of submissions to the question.
        difficulty (str): The difficulty level of the question (Easy, Medium, or Hard).
    """

    __tablename__ = "codechef_question"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    link = Column(String(255))
    submit_link = Column(String(255))
    submitted_solutions = Column(Integer)
    accuracy = Column(Float)
    status_link = Column(String(255))
    difficulty = Column(String(32))

    def __init__(self, question_information):
        """
        Initializes a new instance of the CodeChefQuestion class.

        Args:
            question_information (dict): A dictionary containing attribute values
                                         for the CodeChefQuestion object.
        """
        self.id = question_information["id"]
        self.name = question_information["name"]
        self.link = question_information["link"]
        self.submit_link = question_information["submit_link"]
        self.submitted_solutions = question_information["submitted_solutions"]
        self.accuracy = question_information["accuracy"]
        self.status_link = question_information["status_link"]
        self.difficulty = question_information["difficulty"]

    def to_dict(self):
        """
        Convert the CodeChefQuestion object to a dictionary.

        Returns:
            dict: A dictionary representation of the CodeChefQuestion object.
        """
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "submit_link": self.submit_link,
            "submitted_solutions": self.submitted_solutions,
            "accuracy": self.accuracy,
            "status_link": self.status_link,
            "difficulty": self.difficulty,
        }
