from functools import wraps
from FileDB import disk_store, db_store


def disk_save(url, html):

    def decorator(func):
        @wraps(func)
        def wrappers(*args, **kwargs):
            disk_store.save(url, html)
            res = func(*args, **kwargs)
            return res
        return wrappers
    return decorator


def db_save(url, html):

    def decorator(func):
        @wraps(func)
        def wrappers(*args, **kwargs):
            db_store.save(url, html)
            res = func(*args, **kwargs)
            return res
        return wrappers
    return decorator
