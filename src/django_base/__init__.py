try:
    from version import *

except ImportError:
    __version__ = None
    __version_tuple__ = tuple()
