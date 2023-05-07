from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from apps.tool_repository.tools.repository.get_db_engine import get_engine
from . import Base

Engine: Engine = get_engine()
Session = sessionmaker(Engine)

def init_db():
    global Base, Engine
    
    # Base.metadata.drop_all(bind=Engine, tables=[EndpointDiagnostics.__table__])
    Base.metadata.create_all(bind=Engine)
    print("Created Model")
    

# init_db()
