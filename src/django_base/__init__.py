try:
    from .version import version, version_tuple

except ImportError:
    version = None
    version_tuple = tuple()
