"""
file_name = classes.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to work with the class table.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=too-many-branches

from typing import List

from sqlalchemy.orm import Session, Query

from apps.tool_repository.tools.repository.models.model import Session as Sess
from apps.tool_repository.tools.repository.models.class_model import Class


class ClassRepository:
    """
    A class representing a data store for Class objects.

    This class provides methods for inserting Class objects into the database, retrieving
    Class objects from the database, and deleting Class objects from the database.

    Attributes:
        session: An SQLAlchemy session object used for managing database transactions.
    """

    def __init__(self):
        """
        Creates a new ClassRepository object and initializes an SQLAlchemy session.
        """

        self.session: Session = Sess()

    def __enter__(self):
        """
        Called when the object is used as a context manager.

        This function is called when the `with` statement is used to create a context
        for the ClassRepository object. Returns the current object as the context
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

    def insert(self, _class_: Class) -> int:
        """
        Inserts a Class object into the database.

        This function takes a Class object as input, inserts it into the database using
        the current SQLAlchemy session, commits the transaction, and returns the ID of the
        inserted Class.

        Args:
            _class_: A Class object to insert into the database.

        Returns:
            The ID of the inserted Class.
        """

        self.session.add(_class_)
        self.session.commit()
        return _class_.ClassId

    def update(self, class_id: int, update_dictionary: dict) -> None:
        """
        Updates a Class object in the database with the specified changes.

        This function takes a Class ID and a dictionary of updates, and updates the corresponding
        Class object in the database with the new values. Any keys in the update dictionary
        that are not valid attributes of the Class object are ignored.

        Args:
            class_id: The ID of the Class object to be updated.
            update_dictionary: A dictionary of updates to apply to the Class object.

        Returns:
            None

        Raises:
            ValueError: If the `class_id` parameter is not a valid ID for a Class object.
        """

        _class_: Class = (
            self.session.query(Class).filter(Class.ClassId == class_id).first()
        )

        if update_dictionary.get("Department"):
            _class_.Department = update_dictionary["Department"]

        if update_dictionary.get("CourseNumber"):
            _class_.CourseNumber = update_dictionary["Course Number"]

        if update_dictionary.get("Professor"):
            _class_.Professor = update_dictionary["Professor"]

        if update_dictionary.get("Name"):
            _class_.Name = update_dictionary["Name"]

        if update_dictionary.get("Semester"):
            _class_.Semester = update_dictionary["Semester"]

        self.session.commit()

    def get(self, filters: dict) -> List[Class]:
        """
        Retrieves a list of classes from the database that match the specified filter criteria.

        This method queries the database for classes that match the specified filter criteria and
        returns a list of Class objects that match the criteria.

        Args:
            filters: A dictionary of filter criteria used to query the database.

        Returns:
            A list of Class objects that match the filter criteria.

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """

        query: Query = self.session.query(Class)

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("Department"):
            query = query.filter(Class.Department == filters["Department"])

        if filters.get("CourseNumber"):
            query = query.filter(Class.CourseNumber == filters["CourseNumber"])

        if filters.get("Professor"):
            query = query.filter(Class.Professor == filters["Professor"])

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Class.Name == filters["Name"])
            else:
                query = query.filter(Class.Name.like(filters["Name"]))

        if filters.get("Semester"):
            query = query.filter(Class.Semester == filters["Semester"])

        return query.all()

    def delete(self, filters: dict) -> None:
        """
        Deletes one or more Class objects from the database that match the specified filter
        criteria.

        This method takes a dictionary of filters and uses them to search for Class objects
        that match the criteria specified in the filters. It then deletes all matching Class
        objects from the database.

        Args:
            filters: A dictionary of filter criteria used to query the database.

        Returns:
            None

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """

        query: Query = self.session.qeury(Class)
        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("Department"):
            query = query.filter(Class.Department == filters["Department"])

        if filters.get("CourseNumber"):
            query = query.filter(Class.CourseNumber == filters["CourseNumber"])

        if filters.get("Professor"):
            query = query.filter(Class.Professor == filters["Professor"])

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Class.Name == filters["Name"])
            else:
                query = query.filter(Class.Name.like(filters["Name"]))

        if filters.get("Semester"):
            query = query.filter(Class.Semester == filters["Semester"])

        query.delete()
        self.session.commit()
