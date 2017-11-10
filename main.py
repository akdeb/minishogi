from utils import *
import sys
import pprint
from objects import *

# will do this after logic implemented correctly
def fileMode(path):

    if path is None:
        path = sys.argv[2]
    #pprint.pprint(retVal)

    game = playGame(parseTestCase(path))
    return

def playGame(ret):
    g = Minishogi(ret)
    return g

def intMode():
    pass
