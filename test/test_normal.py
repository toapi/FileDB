import time
from FileDB import disk_save, disk_get, db_save, db_get

html = "<html>hello, world!</html>"
url = "http://www.baidu.com/test"


def test_disk():
    disk_save(url, html)
    res = disk_get(url)
    assert res == html


def test_db():
    db_save(url, html)
    res = db_get(url)
    assert res == html


def test_disk_expiration():
    disk_save(url, html)
    time.sleep(5)
    assert disk_get(url, expiration=3) != html


def test_db_expiration():
    db_save(url, html)
    time.sleep(5)
    assert db_get(url, expiration=3) != html
