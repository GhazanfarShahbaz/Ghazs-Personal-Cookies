"""
file_name = coding_questions.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to work with the coding_question table.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=too-many-branches

from typing import List

from sqlalchemy.orm import Session, Query

from apps.tool_repository.tools.repository.models.model import Session as Sess
from apps.tool_repository.tools.repository.models.coding_question_model import (
    CodingQuestion,
)


class CodingQuestionRepository():
    """
    A class representing a data store for CodingQuestion objects.

    This class provides methods for inserting CodingQuestion objects into the database.

    Attributes:
        session: An SQLAlchemy session object used for managing database transactions.
    """

    def __init__(self):
        """
        Creates a new CodingQuestionRepository object and initializes an SQLAlchemy session.
        """
        self.session: Session = Sess()

    def __enter__(self):
        """
        Called when the object is used as a context manager.

        This function is called when the `with` statement is used to create a context
        for the CodingQuestionRepository object. Returns the current object as the context
        manager value.
        """

        return self  # pylint: disable=unnecessary-pass

    def __exit__(self, type, value, traceback):  # pylint: disable=redefined-builtin
        """
        Called when the context manager is exited.

        This function is called when the `with` block created by the `with` statement
        that created this context manager is exited. This function closes the SQLAlchemy
        session.
        """

        self.session.close()

    def insert(self, coding_questions: List[CodingQuestion]) -> None:
        """
        Inserts one or more CodingQuestion objects into the database.

        This function takes a list of CodingQuestion objects as input, inserts each of
        them into the database using the current SQLAlchemy session, and commits the
        transaction.

        Args:
            coding_questions: A list of CodingQuestion objects to insert into the database.

        Returns:
            None
        """

        for coding_question in coding_questions:
            self.session.add(coding_question)

        self.session.commit()

    def update(self, question_id: int, update_dict: dict) -> None:
        """
        Updates a coding question object in the database with the specified changes.

        This method takes a question ID and a dictionary of updates, and updates the corresponding
        coding question object in the database with the new values. Any keys in the update 
        dictionarythat are not valid attributes of the coding question object are ignored.

        Args:
            question_id: The ID of the coding question object to be updated.
            update_dict: A dictionary of updates to apply to the coding question object.

        Returns:
            None

        Raises:
            ValueError: If the `question_id` parameter is not a valid ID for a coding question
            object.
        """

        # retrieve the coding question object to be updated from the database
        coding_question: CodingQuestion = (
            self.session.query(CodingQuestion)
            .filter(CodingQuestion.QuestionId == question_id)
            .first()
        )

        # apply any changes that were requested in the update dictionary
        if update_dict.get("QuestionLink"):
            coding_question.QuestionLink = update_dict["QuestionLink"]

        if update_dict.get("Difficulty"):
            coding_question.Difficulty = update_dict["Difficulty"]

        if update_dict.get("AcceptanceRate"):
            coding_question.AcceptanceRate = update_dict["AcceptanceRate"]

        if update_dict.get("Tags"):
            coding_question.Tags = update_dict["Tags"]

        if update_dict.get("RequiresSubscription"):
            coding_question.RequiresSubscription = update_dict["RequiresSubscription"]

        # commit the changes to the database
        self.session.commit()

    def get(self, filters: dict) -> List[CodingQuestion]:
        query: Query = self.session.query(CodingQuestion)

        if filters.get("QuestionIds"):
            query = query.filter(CodingQuestion.QuestionId.in_(filters["QuestionIds"]))

        if filters.get("QuestionName"):
            if (
                filters.get("QuestionNameExact") is None
                or filters["QuestionNameExact"] is True
            ):
                query = query.filter(
                    CodingQuestion.QuestionName == filters["QuestionName"]
                )
            else:
                query = query.filter(
                    CodingQuestion.QuestionName.like(filters["QuestionName"])
                )

        if filters.get("QuestionLink"):
            query = query.filter(CodingQuestion.QuestionLink == filters["QuestionLink"])

        if filters.get("Difficulties"):
            query = query.filter(CodingQuestion.Difficulty.in_(filters["Difficulties"]))

        if filters.get("AcceptanceRateFrom"):
            query = query.filter(
                CodingQuestion.AcceptanceRate >= filters["AcceptanceRateFrom"]
            )

        if filters.get("AcceptanceRateTo"):
            query = query.filter(
                CodingQuestion.AcceptanceRate >= filters["AcceptanceRateTo"]
            )

        if filters.get("RequiresSubscription") is not None:
            query = query.filter(
                CodingQuestion.RequiresSubscription == filters["RequiresSubscription"]
            )

        return query.all()

    def delete(self, filters: dict) -> None:
        """
        Retrieves a list of coding question objects from the database that match the specified 
        filter criteria.

        This method queries the database for coding questions that match the specified filter 
        criteria and returns a list of coding question objects that match the criteria.

        Args:
            filters: A dictionary of filter criteria used to query the database.

        Returns:
            A list of coding question objects that match the filter criteria.

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """

        # create a query object for the CodingQuestion table
        query: Query = self.session.query(CodingQuestion)

        # filter the query based on the input filter dictionary
        if filters.get("QuestionIds"):
            query = query.filter(CodingQuestion.QuestionId.in_(filters["QuestionIds"]))

        if filters.get("QuestionName"):
            if (
                filters.get("QuestionNameExact") is None
                or filters["QuestionNameExact"] is True
            ):
                query = query.filter(
                    CodingQuestion.QuestionName == filters["QuestionName"]
                )
            else:
                query = query.filter(
                    CodingQuestion.QuestionName.like(filters["QuestionName"])
                )

        if filters.get("QuestionLink"):
            query = query.filter(CodingQuestion.QuestionLink == filters["QuestionLink"])

        if filters.get("Difficulties"):
            query = query.filter(CodingQuestion.Difficulty.in_(filters["Difficulties"]))

        if filters.get("AcceptanceRateFrom"):
            query = query.filter(
                CodingQuestion.AcceptanceRate >= filters["AcceptanceRateFrom"]
            )

        if filters.get("AcceptanceRateTo"):
            query = query.filter(
                CodingQuestion.AcceptanceRate >= filters["AcceptanceRateTo"]
            )

        if filters.get("RequiresSubscription") is not None:
            query = query.filter(
                CodingQuestion.RequiresSubscription == filters["RequiresSubscription"]
            )

        # execute the query and return the result as a list of coding question objects
        return query.all()
