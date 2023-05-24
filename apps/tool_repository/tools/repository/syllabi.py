from sqlalchemy.orm import Session, Query
from typing import List

from apps.tool_repository.tools.repository.models.model import Session as Sess
from apps.tool_repository.tools.repository.models.class_model import Class
from apps.tool_repository.tools.repository.models.syllabus_model import Syllabus


class SyllabusRepository(object):
    """
    A class representing a data store for Syllabus objects.

    This class provides methods for inserting, updating, and querying Syllabus objects in the database.

    Attributes:
        session: An SQLAlchemy session object used for managing database transactions.
    """

    def __init__(self):
        """
        Creates a new SyllabusRepository object and initializes an SQLAlchemy session.
        """
        self.session: Session = Sess()

    def __enter__(self):
        """
        Called when the object is used as a context manager.

        This function is called when the `with` statement is used to create a context
        for the SyllabusRepository object. Does nothing, and returns None.
        """
        
        pass

    def __exit__(self, type, value, traceback):
        """
        Called when the context manager is exited.

        This function is called when the `with` block created by the `with` statement
        that created this context manager is exited. This function closes the SQLAlchemy
        session.
        """
        
        self.session.close()

    def insert(self, syllabus: Syllabus) -> int:
        """
        Inserts a new Syllabus object into the database.

        This method takes a Syllabus object and inserts it into the database.

        Args:
            syllabus: A Syllabus object to be inserted into the database.

        Returns:
            An integer representing the ID of the new Syllabus object in the database.
        """
        
        self.session.add(syllabus)
        self.session.commit()
        return syllabus.SectionId

    def update(self, section_id: int, update_dictionary: dict) -> None:
        """
        Updates a Syllabus object in the database.

        This method takes the ID of a Syllabus object and a dictionary of updates, and applies the updates
        to the corresponding Syllabus object in the database.

        Args:
            section_id: An integer representing the ID of the Syllabus object to be updated.
            update_dictionary: A dictionary of updates to apply to the Syllabus object.

        Returns:
            None.
        """
        
        syllabus: Syllabus = self.session.query(Syllabus).filter(
            Syllabus.SectionId == section_id).first()

        if update_dictionary.get("Section"):
            syllabus.Section = update_dictionary["Section"]

        if update_dictionary.get("Percentage"):
            syllabus.Percentage = update_dictionary["Percentage"]

        if update_dictionary.get("Droppable"):
            syllabus.Droppable = update_dictionary["Droppable"]

        self.session.commit()

    def get(self, filters: dict) -> List[Syllabus]:
        """
        Retrieves a list of Syllabus objects from the database that match the specified filter criteria.

        This method queries the database for Syllabus objects that match the specified filter criteria and
        returns a list of Syllabus objects that match the criteria.

        Args:
            filters: A dictionary of filter criteria used to query the database.

        Returns:
            A list of Syllabus objects that match the filter criteria.

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """
        query: Query = self.session.query(Syllabus).join(
            Class, Class.ClassId == Syllabus.ClassId)

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("ClassName"):
            if filters.get("ClassNameExact") is None or filters["ClassNameExact"] is True:
                query = query.filter(Class.Name == filters["ClassName"])
            else:
                query = query.filter(Class.Name.like(filters["ClassName"]))

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Droppable"):
            query = query.filter(Syllabus.Droppable == filters["Droppable"])

        if filters.get("Section"):
            if filters.get("SectionExact") is None or filters["SectionExact"] is True:
                query = query.filter(Syllabus.Section == filters["Section"])
            else:
                query = query.filter(Syllabus.Section.like(filters["Section"]))

        return query.all()

    def delete(self, filters: dict) -> List[Syllabus]:
        """
        Delete Syllabus objects from the database that match the specified filter criteria.

        This method queries the database for Syllabus objects that match the specified filter criteria and
        deletes all of them.

        Args:
            filters: A dictionary of filter criteria used to delete Syllabus objects.

        Returns:
            None

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """
        
        query: Query = self.session.query(Syllabus).join(
            Class, Class.ClassId == Syllabus.ClassId)

        if filters.get("ClassIds"):
            query = query.filter(Class.ClassId.in_(filters["ClassIds"]))

        if filters.get("ClassName"):
            if filters.get("ClassNameExact") is None or filters["ClassNameExact"] is True:
                query = query.filter(Class.Name == filters["ClassName"])
            else:
                query = query.filter(Class.Name.like(filters["ClassName"]))

        if filters.get("SectionIds"):
            query = query.filter(Syllabus.SectionId.in_(filters["SectionIds"]))

        if filters.get("Droppable"):
            query = query.filter(Syllabus.Droppable == filters["Droppable"])

        if filters.get("Section"):
            if filters.get("SectionExact") is None or filters["SectionExact"] is True:
                query = query.filter(Syllabus.Section == filters["Section"])
            else:
                query = query.filter(Syllabus.Section.like(filters["Section"]))

        query.delete()
        self.session.commit()
