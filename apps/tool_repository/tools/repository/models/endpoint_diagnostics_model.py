"""
file_name = endpoint_diagnostics.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the EndpointDiagnostics model.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable

from sqlalchemy import (
    Column,
    DateTime,
    JSON,
    Integer,
    String,
    Float
)

from . import Base


class EndpointDiagnostics(Base):
    """
        Represents diagnostics information for an endpoint.

        Attributes:
        - DiagnosticId: The unique ID of the diagnostic entry.
        - Endpoint: The endpoint URL.
        - Request: The request data in JSON format.
        - Response: The response data in JSON format.
        - Date: The date and time of the diagnostic entry.
        - Error: The error message, if any.
        - Latency: The latency of the endpoint.
    """

    __tablename__ = "endpoint_"

    DiagnosticId = Column("DiagnosticId", Integer, autoincrement=True, primary_key=True)
    Endpoint = Column("Endpoint", String(1024), nullable=False)
    Request = Column("Request", JSON, nullable=False)
    Response = Column("Response", JSON, nullable=False)
    Date = Column("Date", DateTime(timezone=True), nullable=False)
    Error = Column("Error", String(1024), nullable=False)
    Latency = Column("Float", Float, nullable=False)

    def __init__(self, diagnostics_information: dict) -> None:
        self.Endpoint = diagnostics_information.get("Endpoint")
        self.Request = diagnostics_information.get("Request")
        self.Response = diagnostics_information.get("Response")
        self.Date = diagnostics_information.get("Date")
        self.Error = diagnostics_information.get("Error")
        self.Latency = diagnostics_information.get("Latency")

    def to_dict(self) -> dict:
        return {
            "DiagnosticId": self.DiagnosticId,
            "Endpoint": self.Endpoint,
            "Request": self.Request,
            "Response": self.Response,
            "Date": self.Date,
            "Error": self.Error,
            "Latency": self.Latency,
        }
