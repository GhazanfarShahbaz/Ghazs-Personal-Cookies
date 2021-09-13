import os
import sys

# if this filei s called from a parent directory the repository.... path is needed this allows all modules to be called from this directory
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)