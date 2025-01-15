import importlib.metadata as importlib_metadata

try:
    __version__ = importlib_metadata.version("django-tapeforms")
except Exception:
    __version__ = "HEAD"
