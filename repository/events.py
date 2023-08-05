"""
file_name = events.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to work with the events table.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=too-many-branches

from typing import List

from sqlalchemy.orm import Session, Query
from sqlalchemy import func, distinct, asc

from repository.models.model import Session as Sess
from repository.models.event_model import Event


class EventRepository:
    """
    A class representing a data store for Event objects.

    This class provides methods for inserting Event objects into the database.

    Attributes:
        session: An SQLAlchemy session object used for managing database transactions.
    """

    def __init__(self):
        """
        Creates a new EventRepository object and initializes an SQLAlchemy session.
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

    def insert(self, events: List[Event]) -> None:
        """
        Inserts one or more Event objects into the database.

        This method takes a list of Event objects as input, inserts each of them into the
        database using the current SQLAlchemy session, and commits the transaction.

        Args:
            events: A list of Event objects to insert into the database.

        Returns:
            None
        """
        for event in events:
            self.session.add(event)
        self.session.commit()

    def update_by_id(self, event_id: int, update_dictionary: dict) -> None:
        """
        Updates an Event object in the database with the specified changes.

        This method takes an event ID and a dictionary of updates, and updates the
        corresponding event object in the database with the new values.
        Any keys in the update dictionary that are not valid attributes of the event
        object are ignored.

        Args:
            event_id: The ID of the event object to be updated.
            update_dict: A dictionary of updates to apply to the event object.

        Returns:
            None

        Raises:
            ValueError: If the `event_id` parameter is not a valid ID for an event object.
        """

        event: Event = (
            self.session.query(Event).filter(Event.EventId == event_id).first()
        )

        if update_dictionary.get("Name"):
            event.Name = update_dictionary["Name"]

        if update_dictionary.get("StartDate"):
            event.StartDate = update_dictionary["StartDate"]

        if update_dictionary.get("EndDate"):
            event.EndDate = update_dictionary["EndDate"]

        if update_dictionary.get("Type"):
            event.Type = update_dictionary["Type"]

        if update_dictionary.get("Description"):
            event.Description = update_dictionary["Description"]

        self.session.commit()

    def update_by_recurrance_id(
        self, recurrance_id: int, update_dictionary: dict
    ) -> None:
        """
        Updates one or more Event objects in the database with the specified changes.

        This method takes a recurrence ID and a dictionary of updates, and updates all
        corresponding event objects in the database with the new values. Any keys in the
        update dictionary that are not valid attributes of the event objects are ignored.

        Args:
            recurrance_id: The ID of the recurrence pattern for the event objects to be updated.
            update_dict: A dictionary of updates to apply to the event objects.

        Returns:
            None

        Raises:
            ValueError: If the `recurrance_id` parameter is not a valid ID for an event
            recurrence pattern.
        """

        self.session.query(Event).filter(Event.ReccuranceId == recurrance_id).update(
            update_dictionary
        )
        self.session.commit()

    def get(self, filters: dict) -> List[Event]:
        """
        Retrieves a list of Event objects from the database that match the specified filter
        criteria.

        This method queries the database for Event objects that match the specified filter
        criteria and returns a list of Event objects that match the criteria.

        Args:
            filters: A dictionary of filter criteria used to query the database.

        Returns:
            A list of Event objects that match the filter criteria.

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """

        query: Query = self.session.query(Event)

        if filters.get("EventIds"):
            query = query.filter(Event.EventId.in_(filters["EventIds"]))

        if filters.get("ReccuranceIds"):
            query = query.filter(Event.ReccuranceId.in_(filters["ReccuranceIds"]))

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Event.Name == filters["Name"])
            else:
                query = query.filter(Event.Name.like(filters["Name"]))

        if filters.get("StartDate"):
            query = query.filter(Event.StartDate == filters["StartDate"])

        if filters.get("EndDate"):
            query = query.filter(Event.EnDate == filters["EndDate"])

        if filters.get("DateFrom"):
            query = query.filter(Event.StartDate >= filters["DateFrom"])

        if filters.get("DateTo"):
            query = query.filter(Event.EndDate <= filters["DateTo"])

        if filters.get("Type"):
            query = query.filter(Event.Type == filters["Type"])

        if filters.get("Description"):
            query = query.filter(Event.Description == filters["Description"])
            
            
        query = query.order_by(asc(Event.StartDate))

        return query.all()

    def delete(self, filters: dict) -> None:
        """
        Deletes Event objects from the database that match the specified filter criteria.

        This method queries the database for Event objects that match the specified filter
        criteria and deletes all of them.

        Args:
            filters: A dictionary of filter criteria used to select the Event objects to delete.

        Returns:
            None

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """

        query: Query = self.session.query(Event)

        if filters.get("EventIds"):
            query = query.filter(Event.EventId.in_(filters["EventIds"]))

        if filters.get("ReccuranceIds"):
            query = query.filter(Event.ReccuranceId.in_(filters["ReccuranceIds"]))

        if filters.get("Name"):
            if filters.get("NameExact") is None or filters["NameExact"] is True:
                query = query.filter(Event.Name == filters["Name"])
            else:
                query = query.filter(Event.Name.like(filters["Name"]))

        if filters.get("StartDate"):
            query = query.filter(Event.StartDate == filters["StartDate"])

        if filters.get("EndDate"):
            query = query.filter(Event.EnDate == filters["EndDate"])

        if filters.get("DateFrom"):
            query = query.filter(Event.StartDate >= filters["DateFrom"])

        if filters.get("DateTo"):
            query = query.filter(Event.EndDate <= filters["DateTo"])

        if filters.get("Type"):
            query = query.filter(Event.Type == filters["Type"])

        if filters.get("Description"):
            query = query.filter(Event.Description == filters["Description"])

        query.delete()
        self.session.commit()

    def get_reccurance_count(self) -> int:
        """
        Returns the number of unique recurrence IDs in the database.

        This method queries the database for the highest value of the recurrence ID attribute
        of all Event objects, and returns that value plus 1.

        Returns:
            An integer representing the number of unique recurrence IDs in the database.
        """

        query: Query = self.session.query(func.max(distinct(Event.ReccuranceId)))
        return query.first()[0] + 1 if query.first()[0] is not None else 0
