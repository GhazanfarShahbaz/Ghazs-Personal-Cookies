"""
file_name = assignments.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to work with the assignment table.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=too-many-branches, duplicate-code

from typing import List

from sqlalchemy.orm import Session, Query

from apps.tool_repository.tools.repository.models.model import Session as Sess
from apps.tool_repository.tools.repository.models.assignment_model import Assignment
from apps.tool_repository.tools.repository.models.class_model import Class
from apps.tool_repository.tools.repository.models.syllabus_model import Syllabus


class AssignmentRepository:
    """
    A class representing a data store for Assignment objects.

    This class provides methods for inserting, updating, and deleting Assignment objects
    in the database using an SQLAlchemy session.

    Attributes:
        session: An SQLAlchemy session object used for managing database transactions.
    """

    def __init__(self):
        """
        Creates a new AssignmentStore object and initializes an SQLAlchemy session.
        """

        self.session: Session = Sess()

    def __enter__(self):
        """
        Called when the object is used as a context manager.

        This function is called when the `with` statement is used to create a context
        for the AssignmentStore object. Returns the current object as the context
        manager value.
        """

        pass  # pylint: disable=unnecessary-pass

    def __exit__(self, type, value, traceback):  # pylint: disable=redefined-builtin
        """
        Called when the context manager is exited.

        This function is called when the `with` block created by the `with` statement
        that created this context manager is exited. This function closes the SQLAlchemy
        session.
        """

        self.session.close()

    def insert(self, assignment: Assignment) -> int:
        """
        Inserts an Assignment object into the database.

        This function takes an Assignment object as input, inserts it into the database using
        the current SQLAlchemy session, commits the transaction, and returns the ID of the
        inserted Assignment.

        Args:
            assignment: An Assignment object to insert into the database.

        Returns:
            The ID of the inserted Assignment.
        """

        self.session.add(assignment)
        self.session.commit()
        return assignment.AssignmentId

    def update(self, assignment_id: int, update_dictionary: dict) -> int:
        """
        Updates an Assignment object in the database with the specified changes.

        This function takes an Assignment ID and a dictionary of updates, and updates the
        corresponding Assignment object in the database with the new values. Any keys in the
        update dictionary that are not valid attributes of the Assignment object are ignored.

        Args:
            assignment_id: The ID of the Assignment object to be updated.
            update_dictionary: A dictionary of updates to apply to the Assignment object.

        Returns:
            The number of rows affected in the database by the update.

        Raises:
            ValueError: If the `assignment_id` parameter is not a valid ID for an Assignment object.
        """

        assignment = (
            self.session.query(Assignment)
            .filter(Assignment.AssignmentId == assignment_id)
            .first()
        )

        if update_dictionary.get("Name"):
            assignment.Name = update_dictionary["Name"]

        if update_dictionary.get("Grade"):
            assignment.Grade = update_dictionary["Grade"]

        if update_dictionary.get("DateAssigned"):
            assignment.DateAssigned = update_dictionary["DateAssigned"]

        if update_dictionary.get("DateDue"):
            assignment.DateDue = update_dictionary["DateDue"]

        if update_dictionary.get("Submitted"):
            assignment.Submitted = update_dictionary["Submitted"]

        self.session.commit()

    def get(self, filters: dict) -> List[Assignment]:
        """
        Retrieves a list of assignments from the database that match the specified filter criteria.

        This method queries the database for assignments that match the specified filter criteria
        and returns a list of Assignment objects that match the criteria.

        Args:
            filters: A dictionary of filter criteria used to query the database.

        Returns:
            A list of Assignment objects that match the filter criteria.

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """

        # Create a query object with joins between Assignment, Syllabus, and Class tables
        query: Query = (
            self.session.query(Assignment)
            .join(Syllabus, Syllabus.SectionId == Assignment.SectionId)
            .join(Class, Class.ClassId == Syllabus.ClassId)
        )

        # Filter the query based on the input filter dictionary
        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("ClassName"):
            if (
                filters.get("ClassNameExact") is None
                or filters["ClassNameExact"] is True
            ):
                query = query.filter(Class.Name == filters["ClassName"])
            else:
                query = query.filter(Class.Name.like(filters["ClassName"]))

        if filters.get("DateAssigned"):
            query = query.filter(Assignment.DateAssigned == filters["DateAssigned"])

        if filters.get("DateDue"):
            query = query.filter(Assignment.DateDue == filters["DateDue"])

        if filters.get("Submitted"):
            query = query.filter(Assignment.Submitted == filters["Submitted"])

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Section"):
            if filters.get("SectionExact") is None or filters["SectionExact"] is True:
                query = query.filter(Syllabus.Section == filters["Section"])
            else:
                query = query.filter(Syllabus.Section.like(filters["Section"]))

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Assignment.Name == filters["Name"])
            else:
                query = query.filter(Assignment.Name.like(filters["Name"]))

        # Execute the query and return the result as a list of Assignment objects
        return query.all()

    def delete(self, filters: dict) -> None:
        """
        Deletes one or more assignment objects from the database.

        This method takes a dictionary of filters and uses them to search for Assignment objects
        that match the criteria specified in the filters. It then deletes all matching Assignment
        objects from the database.

        Args:
            filters: A dictionary of filter criteria used to query the database.

        Returns:
            None

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """

        # Create a query object with joins between Assignment, Syllabus, and Class tables
        query: Query = (
            self.session.query(Assignment)
            .join(Syllabus, Syllabus.SectionId == Assignment.SectionId)
            .join(Class, Class.ClassId == Syllabus.ClassId)
        )

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("ClassName"):
            if (
                filters.get("ClassNameExact") is None
                or filters["ClassNameExact"] is True
            ):
                query = query.filter(Class.Name == filters["ClassName"])
            else:
                query = query.filter(Class.Name.like(filters["ClassName"]))

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Section"):
            if filters.get("SectionExact") is None or filters["SectionExact"] is True:
                query = query.filter(Syllabus.Section == filters["Section"])
            else:
                query = query.filter(Syllabus.Section.like(filters["Section"]))

        if filters.get("DateDue"):
            query = query.filter(Assignment.DateDue == filters["DateDue"])

        if filters.get("Submitted"):
            query = query.filter(Assignment.Submitted == filters["Submitted"])

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Assignment.Name == filters["Name"])
            else:
                query = query.filter(Assignment.Name.like(filters["Name"]))

        # Perform the deletion and then commit
        query.delete()
        self.session.commit()
