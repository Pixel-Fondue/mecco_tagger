#python

import lx, lxu, modo, traceback

DEBUG = True

try:
    import util
    import presets
    import items
    import manage
    import shadertree
    import selection
    import scene
    from commander import *
    from var import *
    from PopupClass import *
    from PolysConnectedByTag import *
except:
    traceback.print_exc()
