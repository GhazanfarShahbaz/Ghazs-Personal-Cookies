from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
import os

def get_engine() -> Engine:
    load_dotenv()
    sql_type: str = os.environ["SQL_TYPE"]
    sql_host: str = os.environ["SQL_HOST"]
    sql_password: str = os.environ["SQL_PASSWORD"]
    sql_port: str = os.environ["SQL_PORT"]
    sql_database: str = os.environ["SQL_DATABASE"]
    sql_username: str = os.environ["SQL_USERNAME"]

    engine: Engine = create_engine(f"{sql_type}://{sql_username}:{sql_password}@{sql_host}:{sql_port}/{sql_database}")
    return engine