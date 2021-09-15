from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import os

def get_engine() -> Engine:
    load_dotenv()
    sql_type: str = os.environ["SQL_TYPE"]
    sql_host: str = os.environ["SQL_HOST"]
    sql_address: str = os.environ["SQL_ADDRESS"]
    sql_port: str = os.environ["SQL_PORT"]
    sql_database: str = os.environ["SQL_DATABASE"]
    engine: Engine = create_engine(f"{sql_type}://{sql_host}:{sql_address}:{sql_port}/{sql_database}")

    return engine