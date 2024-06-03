"""
file_name = __init__.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to setup the Base for sqlalchemy.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""


from sqlalchemy.orm import declarative_base

Base = declarative_base()
