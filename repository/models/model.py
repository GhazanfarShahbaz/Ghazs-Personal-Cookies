"""
file_name = model.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module that indirectly combines all models and setups the engine.
07/14/2023
-   Conformed to pylint conventions.
"""

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from repository.get_db_engine import get_engine

from . import Base

Engine: Engine = get_engine()
Session = sessionmaker(Engine)


def init_db():
    """
    Initializes the database by creating any necessary tables.

    This function initializes the database tables by calling the `create_all()` method on the
    `Base` object with the `Engine` object as a bind parameter. Prints a message indicating
    that the model has been created.

    Returns:
        None
    """

    # pylint: disable=global-variable-not-assigned
    global Base, Engine

    Base.metadata.create_all(bind=Engine)
    print("Created Model")


# init_db()
