from .external import *


def not_supported():
    from inspect import stack
    print("Function '%s' is not supported for this client." % stack()[1][3])
