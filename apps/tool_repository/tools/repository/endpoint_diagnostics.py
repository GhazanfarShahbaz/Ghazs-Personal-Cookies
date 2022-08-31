from model import Session as Sess, EndpointDiagnostics
from sqlalchemy.orm import Session, Query 
from typing import List

class EndpointDiagnosticsRepository(object):
    def __init__(self):
        self.session: Session = Sess()
        
    def __enter__(self):
        pass
    
    def __exit__(self, type, value, traceback):
        self.session.close()
        
    def insert(self, endpoint_diagnostic: EndpointDiagnostics) -> int:
        self.session.add(endpoint_diagnostic)
        self.session.commit()
        return endpoint_diagnostic.DiagnosticId
    
    def get(self, filters: dict) -> List[EndpointDiagnostics]:
        query_diagnostics: Query = self.session.query(EndpointDiagnostics)
        
        if filter.get("Endpoint"):
            query_diagnostics = query_diagnostics.filter(EndpointDiagnostics.Endpoint.like(filters["Endpoint"]))
            
        if filters.get("DateFrom"):
            query_diagnostics = query_diagnostics.filter(EndpointDiagnostics.Date >= filters["DateFrom"])

        if filters.get("DateTo"):
            query_diagnostics = query_diagnostics.filter(EndpointDiagnostics.Date <= filters["DateTo"])
            
        endpoint_diagnostics_list: List[EndpointDiagnostics] = query_diagnostics.all()
        
        # get sum, average of errors and latency
        
        return endpoint_diagnostics_list

        
        
        
"""
class EndpointDiagnostics(Base):
    __tablename__   = "endpoint_"

    DiagnosticId    = Column("DiagnosticId", Integer, autoincrement=True, primary_key=True)
    Endpoint        = Column("Endpoint", String(1024), nullable=False)
    Request         = Column("Request", JSON, nullable=False)
    Response        = Column("Response", JSON, nullable=False)
    Date            = Column("Date", DateTime(timezone=True), nullable=False)
    Error           = Column("Error", String(1024), nullable=False)
    Latency         = Column("Float", Float, nullable=False)
    
    def to_dict(self) -> dict:
        return {
            "DiagnosticId"  : self.DiagnosticId,
            "Endpoint"      : self.Endpoint,
            "Request"       : self.Request,
            "Response"      : self.Response,
            "Date"          : self.Date,
            "Error"         : self.Error,
            "Latency"       : self.Latency
        }
"""