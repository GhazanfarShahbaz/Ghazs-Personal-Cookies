from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import func
from typing import List

from apps.tool_repository.tools.repository.models.model import Session as Sess
from apps.tool_repository.tools.repository.models.endpoint_diagnostics_model import EndpointDiagnostics

class EndpointDiagnosticsRepository(object):
    """
    A class representing a data store for EndpointDiagnostics objects.

    This class provides methods for inserting EndpointDiagnostics objects into the database.

    Attributes:
        session: An SQLAlchemy session object used for managing database transactions.
    """

    def __init__(self):
        """
        Creates a new EndpointDiagnosticsRepository object and initializes an SQLAlchemy session.
        """
        self.session: Session = Sess()

    def __enter__(self):
        """
        Called when the object is used as a context manager.

        This function is called when the `with` statement is used to create a context
        for the EndpointDiagnosticsRepository object. Returns the current object as the context
        manager value.
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Called when the context manager is exited.

        This function is called when the `with` block created by the `with` statement
        that created this context manager is exited. This function closes the SQLAlchemy
        session.
        """
        self.session.close()

    def insert(self, endpoint_diagnostic: EndpointDiagnostics) -> int:
        """
        Inserts an EndpointDiagnostics object into the database.

        This function takes an EndpointDiagnostics object as input, inserts it into the
        database using the current SQLAlchemy session, commits the transaction, and
        returns the ID of the inserted EndpointDiagnostics.

        Args:
            endpoint_diagnostic: An EndpointDiagnostics object to insert into the database.

        Returns:
            The ID of the inserted EndpointDiagnostics.
        """

    def get(self, filters: dict) -> List[EndpointDiagnostics]:
        """
        Retrieves a list of EndpointDiagnostics objects from the database that match the specified filter criteria.

        This method queries the database for EndpointDiagnostics that match the specified filter criteria and
        returns a list of EndpointDiagnostics objects that match the criteria.

        Args:
            filters: A dictionary of filter criteria used to query the database.

        Returns:
            A list of EndpointDiagnostics objects that match the filter criteria.

        Raises:
            ValueError: If an invalid filter key is included in the input dictionary.
        """
        
        # Create a query for EndpointDiagnostics
        query = None
        if not filters.get("EndpointCounter"):
            query = self.session.query(EndpointDiagnostics)
        else:
            query = self.session.query(EndpointDiagnostics.Endpoint, func.count(EndpointDiagnostics.Endpoint)).group_by(EndpointDiagnostics.Endpoint)

        # Filter the query according to the input filter dictionary
        if filters.get("Endpoint"):
            query = query.filter(EndpointDiagnostics.Endpoint.like(filters["Endpoint"]))

        if filters.get("DateFrom"):
            query = query.filter(EndpointDiagnostics.Date >= filters["DateFrom"])

        if filters.get("DateTo"):
            query = query.filter(EndpointDiagnostics.Date <= filters["DateTo"])

        # Execute the query and get the list of EndpointDiagnostics objects
        endpoint_diagnostics_list = query.all()

        # Get the sum and average of errors and latency

        # Return the list of EndpointDiagnostics objects
        return endpoint_diagnostics_list