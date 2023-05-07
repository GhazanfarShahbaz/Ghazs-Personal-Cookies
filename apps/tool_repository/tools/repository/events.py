from sqlalchemy.orm import Session, Query
from sqlalchemy import func, distinct
from typing import List

from apps.tool_repository.tools.repository.models.model import Session as Sess
from apps.tool_repository.tools.repository.models.event_model import Event

class EventRepository(object):
    def __init__(self) -> None:
        self.session: Session = Sess()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.session.close()

    def insert(self, events: List[Event]) -> None:
        for event in events:
            self.session.add(event)

        self.session.commit()

    def update_by_id(self, event_id: int, update_dictionary: dict) -> None:
        event: Event = self.session.query(Event).filter(
            Event.EventId == event_id).first()

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

    def update_by_recurrance_id(self, recurrance_id: int, update_dictionary: dict) -> None:
        self.session.query(Event).filter(
            Event.ReccuranceId == recurrance_id).update(update_dictionary)
        self.session.commit()

    def get(self, filters: dict) -> List[Event]:
        query: Query = self.session.query(Event)

        if filters.get("EventIds"):
            query = query.filter(Event.EventId.in_(filters["EventIds"]))

        if filters.get("ReccuranceIds"):
            query = query.filter(
                Event.ReccuranceId.in_(filters["ReccuranceIds"]))

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

        return query.all()

    def delete(self, filters: dict) -> None:
        query: Query = self.session.query(Event)

        if filters.get("EventIds"):
            query = query.filter(Event.EventId.in_(filters["EventIds"]))

        if filters.get("ReccuranceIds"):
            query = query.filter(
                Event.ReccuranceId.in_(filters["ReccuranceIds"]))

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
        query: Query = self.session.query(
            func.max(distinct(Event.ReccuranceId)))
        return query.first()[0] + 1 if query.first()[0] else 0
