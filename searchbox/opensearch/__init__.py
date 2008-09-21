import sys
import os

# woot, this is horrible
currentpath = os.path.abspath(os.path.dirname(__file__))
parentpath = os.path.join(currentpath, "..")
sys.path.append(currentpath)
sys.path.append(parentpath)

from util import *

from description import Description
from query import Query
