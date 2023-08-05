"""
file_name = event_model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module representing the Event model.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

# pylint: disable=invalid-name, global-variable-not-assigned, too-few-public-methods, undefined-variable, too-many-instance-attributes

from sqlalchemy import Column, DateTime, Integer, String

from . import Base


class Event(Base):
    """
    Represents an event.

    Attributes:
    - EventId: The unique ID of the event.
    - RecurranceId: The ID of the recurring event, if applicable.
    - Name: The name of the event.
    - StartDate: The start date and time of the event.
    - EndDate: The end date and time of the event.
    - Type: The type of the event.
    - Location: The location of the event.
    - RecurranceType: The type of recurrence for the event, if applicable.
    - Description: A description of the event.
    """

    __tablename__ = "events"

    EventId = Column("EventId", Integer, primary_key=True, autoincrement=True)
    ReccuranceId = Column("RecurranceId", Integer, nullable=True)

    Name = Column("Name", String(256), nullable=False)
    StartDate = Column("StartDate", DateTime(timezone=True), nullable=False)
    EndDate = Column("EndDate", DateTime(timezone=True), nullable=False)
    Type = Column("Type", String(32), nullable=False)
    Location = Column("Location", String(1024), nullable=False)
    ReccuranceType = Column("ReccurranceType", String(64), nullable=True)
    Description = Column("Description", String(512), nullable=True)

    def __init__(self, event_information: dict) -> None:
        self.ReccuranceId = event_information.get("ReccuranceId")
        self.Name = event_information.get("Name")
        self.StartDate = event_information.get("StartDate")
        self.EndDate = event_information.get("EndDate")
        self.Location = event_information.get("Location")
        self.Type = event_information.get("Type")
        self.ReccuranceType = event_information.get("ReccuranceType")
        self.Description = event_information.get("Description")

    def to_dict(self) -> dict:
        return {
            "Id": self.EventId,
            "ReccuranceId": self.ReccuranceId,
            "Name": self.Name,
            "StartDate": self.StartDate,
            "EndDate": self.EndDate,
            "Type": self.Type,
            "Description": self.Description,
            "ReccuranceType": self.ReccuranceType,
            "Location": self.Location
        }
