import sys
from os import path
from sqlalchemy.ext.declarative import declarative_base


# if this filei s called from a parent directory the repository.... path is needed this allows all modules to be called from this directory
current = path.dirname(path.realpath(__file__))
sys.path.append(current)

Base = declarative_base()