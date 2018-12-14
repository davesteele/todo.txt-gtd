from contextlib import contextmanager
from functools import wraps
import os


def none_on_exception(*exceptions):
    def _none_on_exception(fp):
        @wraps(fp)
        def wrapper(*args, **kwargs):
            try:
                return fp(*args, **kwargs)
            except exceptions:
                return None

        return wrapper

    return _none_on_exception


@contextmanager
def nullfd(fd):
    saveout = os.dup(fd)
    os.close(fd)
    os.open(os.devnull, os.O_RDWR)
    try:
        yield
    finally:
        os.dup2(saveout, fd)
