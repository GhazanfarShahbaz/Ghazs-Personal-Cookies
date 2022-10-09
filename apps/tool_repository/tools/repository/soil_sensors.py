from model import Session as Sess, SoilSensor
from sqlalchemy.orm import Session, Query
from typing import List


class SoilSensorRepository(object):
    def __init__(self) -> None:
        self.session: Session = Sess()

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self.session.close()

    def insert(self, soil_sensor_info: SoilSensor) -> None:
        self.session.add(soil_sensor_info)
        self.session.commit()

    def get(self, filters: dict) -> List[SoilSensor]:
        query: Query = self.session.query(SoilSensor)
        
        if filters.get("XCoordinate"):
            query = query.filter(SoilSensor.XCoordinate == filters["XCoordinate"])
            
        if filters.get("YCoordinate"):
            query = query.filter(SoilSensor.YCoordinate == filters["YCoordinate"])
            
        if filters.get("DateFrom"):
            query = query.filter(SoilSensor.Timestamp >= filters["DateFrom"])

        if filters.get("DateTo"):
            query = query.filter(SoilSensor.Timestamp <= filters["DateTo"])
            
        return query.all()


