"""
file_name = leetcode_question_repository.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to work with the leetcode questions table.
Edit Log:
07/14/2023
-   Moved over from leetcode bot repository
"""

from typing import List

from sqlalchemy import or_
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from repository.models.model import Session as Sess
from repository.models.leetcode_question_model import LeetCodeQuestion


class LeetCodeQuestionRepository():
    """
    A class representing a data store for LeetCodeQuestion objects.

    This class provides methods for inserting LeetCodeQuestion objects into the database.

    Attributes:
        session: An SQLAlchemy session object used for managing database transactions.
    """

    def __init__(self):
        """
        Creates a new LeetCodeQuestionRepository object and initializes an SQLAlchemy session.
        """
        self.session: Session = Sess()

    def __enter__(self):
        """
        Called when the object is used as a context manager.

        This function is called when the `with` statement is used to create a context
        for the CodingQuestionRepository object. Returns the current object as the context
        manager value.
        """
        return self

    def __exit__(self, type, value, traceback):  # pylint: disable=redefined-builtin
        """
        Called when the context manager is exited.

        This function is called when the `with` block created by the `with` statement
        that created this context manager is exited. This function closes the SQLAlchemy
        session.
        """
        self.session.close()

    def insert(self, question: LeetCodeQuestion):
        """
        Inserts a new LeetCodeQuestion object to the database.

        Args:
            question (LeetCodeQuestion): The LeetCodeQuestion object to insert to the database.
        """
        self.session.add(question)
        self.session.commit()

    def filter(self, filter_form: dict) -> List[LeetCodeQuestion]:
        """
        Filters LeetCodeQuestion objects in the database based on the given filter parameters.

        Args:
            filter_form (dict): A dictionary containing the filter parameters. Valid keys are:
                - 'name': A string to search the 'name' column for. 
                          Performs a case-insensitive search.
                - 'tag': A list of strings to search the 'tags' column for.
                         Matches if any of the tags are present.
                - 'difficulty': A list of strings to search the 'difficulty' column for
                                Matches if any of the difficulties are present.
                - 'subscription': A boolean value to search the 'subscription' column for. 
                                  Matches if the value is True.
                - 'acceptance_rate': A float value to search the 'acceptance' column for.
                                     Matches if the value is greater than the given value.

        Returns:
            list[LeetCodeQuestion]: A list of LeetCodeQuestion objects that match the
                                    filter criteria.
        """
        query = self.session.query(LeetCodeQuestion)

        if "name" in filter_form:
            query = query.filter(
                LeetCodeQuestion.name.ilike(f'%{filter_form["name"]}%')
            )

        if "tag" in filter_form:
            tags_filters = [
                LeetCodeQuestion.tags.contains(tag) for tag in filter_form["tag"]
            ]
            query = query.filter(or_(*tags_filters))

        if "difficulty" in filter_form:
            query = query.filter(
                LeetCodeQuestion.difficulty.in_(filter_form["difficulty"])
            )

        if "subscription" in filter_form:
            query = query.filter(
                LeetCodeQuestion.subscription == filter_form["subscription"]
            )

        if "acceptance_rate" in filter_form:
            query = query.filter(
                LeetCodeQuestion.acceptance > filter_form["acceptance_rate"]
            )

        return query.all()

    def filter_and_get_random(self, filter_form: dict) -> LeetCodeQuestion:
        """
        Filters LeetCodeQuestion objects in the database based on the given filter parameters.

        Args:
            filter_form (dict): A dictionary containing the filter parameters. Valid keys are:
                - 'name': A string to search the 'name' column for.
                          Performs a case-insensitive search.
                - 'tag': A list of strings to search the 'tags' column for.
                         Matches if any of the tags are present.
                - 'difficulty': A list of strings to search the 'difficulty' column for.
                                Matches if any of the difficulties are present.
                - 'subscription': A boolean value to search the 'subscription' column for.
                                  Matches if the value is True.
                - 'acceptance_rate': A float value to search the 'acceptance' column for.
                                     Matches if the value is greater than the given value.

        Returns:
            LeetCodeQuestion: A LeetCodeQuestion object that matchs the filter criteria.
        """
        query = self.session.query(LeetCodeQuestion)

        if "name" in filter_form and filter_form["name"]:
            query = query.filter(
                LeetCodeQuestion.name.ilike(f'%{filter_form["name"]}%')
            )

        if "tag" in filter_form and filter_form["tag"]:
            tags_filters = [
                LeetCodeQuestion.tags.contains(tag) for tag in filter_form["tag"]
            ]
            query = query.filter(or_(*tags_filters))

        if "difficulty" in filter_form and filter_form["difficulty"]:
            query = query.filter(
                LeetCodeQuestion.difficulty.in_(filter_form["difficulty"])
            )

        if "subscription" in filter_form and filter_form["subscription"]:
            query = query.filter(
                LeetCodeQuestion.subscription == filter_form["subscription"]
            )

        if "acceptance_rate" in filter_form and filter_form["acceptance_rate"]:
            query = query.filter(
                LeetCodeQuestion.acceptance > filter_form["acceptance_rate"]
            )

        return query.order_by(func.random()).first()    # pylint: disable=not-callable

    def update(self, question: LeetCodeQuestion):
        """
        Updates the attributes of an existing LeetCodeQuestion object in the database.

        Args:
            question (LeetCodeQuestion): The updated LeetCodeQuestion object.
        """
        self.session.merge(question)
        self.session.commit()

    def delete(self, question: LeetCodeQuestion):
        """
        Deletes an existing LeetCodeQuestion object from the database.

        Args:
            question (LeetCodeQuestion): The LeetCodeQuestion object to delete.
        """
        self.session.delete(question)
        self.session.commit()
