import sys
from os import path

# if this filei s called from a parent directory the tools.... path is needed this allows all modules to be called from this directory
current = path.dirname(path.realpath(__file__))
sys.path.append(current)

import event_processing