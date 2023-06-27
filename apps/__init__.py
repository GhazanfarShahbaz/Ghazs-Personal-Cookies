import sys
from os import path

sys.path.append("../")
from generate_env import load_environment

load_environment()

# if this filei s called from a parent directory the tools.... path is needed this allows all modules to be called from this directory
current = path.dirname(path.realpath(__file__))
sys.path.append(current)
