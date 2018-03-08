from .storage import DBStore, DiskStore

__version__ = "1.0.0"
disk_store = DiskStore()
db_store = DBStore()


def disk_save(url, html):
    return disk_store.save(url, html)


def disk_get(url, expiration="inf"):
    return disk_store.get(url, expiration=expiration)


def db_save(url, html):
    return db_store.save(url, html)


def db_get(url, expiration="inf"):
    return db_store.get(url, expiration=expiration)
