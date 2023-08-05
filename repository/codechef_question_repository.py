"""
file_name = codechef_question_repository.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to work with the codechef questions table.
Edit Log:
07/14/2023
-   Moved over from leetcode bot repository
"""

from typing import List

from sqlalchemy import or_
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from repository.models.model import Session as Sess
from repository.models.codechef_question_model import CodeChefQuestion



class CodeChefQuestionRepository():
    """
    A class representing a data store for CodeChefQuestion objects.

    This class provides methods for inserting CodeChefQuestion objects into the database.

    Attributes:
        session: An SQLAlchemy session object used for managing database transactions.
    """

    def __init__(self):
        """
        Creates a new CodeChefQuestionRepository object and initializes an SQLAlchemy session.
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

    def __exit__(self, type, value, traceback): # pylint: disable=redefined-builtin
        """
        Called when the context manager is exited.

        This function is called when the `with` block created by the `with` statement
        that created this context manager is exited. This function closes the SQLAlchemy
        session.
        """
        self.session.close()

    def add(self, question: CodeChefQuestion):
        """
        Adds a new CodeChefQuestion object to the database.

        Args:
            question (CodeChefQuestion): The CodeChefQuestion object to add to the database.
        """
        self.session.add(question)
        self.session.commit()

    def update(self, question: CodeChefQuestion):
        """
        Updates the attributes of an existing CodeChefQuestion object in the database.

        Args:
            question (CodeChefQuestion): The updated CodeChefQuestion object.
        """
        self.session.merge(question)
        self.session.commit()

    def filter(self, filters: dict) -> List[CodeChefQuestion]:
        """
        Filters CodeChefQuestion objects in the database based on the given filter parameters.

        Args:
            filters (dict): A dictionary containing the filter parameters. Valid keys are:
                - 'name': A string to search the 'name' column for. 
                          Performs a case-insensitive search.
                - 'tags': A list of strings to search the 'tags' column for. 
                          Matches if any of the tags are present.
                - 'difficulty': A list of strings to search the 'difficulty' column for.
                                Matches if any of the difficulties are present.

        Returns:
            list[CodeChefQuestion]: A list of CodeChefQuestion objects that match the 
                                    filter criteria.
        """
        query = self.session.query(CodeChefQuestion)

        if "name" in filters:
            query = query.filter(CodeChefQuestion.name.ilike(f'%{filters["name"]}%'))

        if "tags" in filters:
            tag_filters = [
                CodeChefQuestion.tags.contains(tag) for tag in filters["tags"]
            ]
            query = query.filter(or_(*tag_filters))

        if "difficulty" in filters:
            query = query.filter(CodeChefQuestion.difficulty.in_(filters["difficulty"]))

        return query.all()

    def filter_and_get_random(self, filters: dict) -> List[CodeChefQuestion]:
        """
        Filters CodeChefQuestion objects in the database based on the given filter parameters.

        Args:
            filters (diccodt): A dictionary containing the filter parameters. Valid keys are:
                - 'name': A string to search the 'name' column for.
                          Performs a case-insensitive search.
                - 'tags': A list of strings to search the 'tags' column for.
                          Matches if any of the tags are present.
                - 'difficulty': A list of strings to search the 'difficulty' column for.
                                Matches if any of the difficulties are present.

        Returns:
            CodeChefQuestion: A CodeChefQuestion object that matchs the filter criteria.
        """
        query = self.session.query(CodeChefQuestion)

        if "name" in filters and filters["name"]:
            query = query.filter(CodeChefQuestion.name.ilike(f'%{filters["name"]}%'))

        if "tags" in filters and filters["tags"]:
            tag_filters = [
                CodeChefQuestion.tags.contains(tag) for tag in filters["tags"]
            ]
            query = query.filter(or_(*tag_filters))

        if "difficulty" in filters and filters["difficulty"]:
            query = query.filter(CodeChefQuestion.difficulty.in_(filters["difficulty"]))

        return query.order_by(func.random()).first()    # pylint: disable=not-callable

    def delete(self, question: CodeChefQuestion):
        """
        Deletes an existing CodeChefQuestion object from the database.

        Args:
            question (CodeChefQuestion): The CodeChefQuestion object to delete.
        """
        self.session.delete(question)
        self.session.commit()
