#python

import lx, lxu, modo, traceback

DEBUG = True

try:
    import util
    import defaults
    import symbols
    import items
    import manage
    import shadertree
    import selection
    from PolysConnectedByTag import *
except:
    traceback.print_exc()
