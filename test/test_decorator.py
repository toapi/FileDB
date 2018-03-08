from FileDB.decorator import disk_save, db_save
from FileDB import disk_get, db_get

html = "<html>hello, world!</html>"
url = "http://www.baidu.com"


def test_disk():

    @disk_save(url, html)
    def store():
        pass

    store()
    res = disk_get(url)
    assert res == html


def test_db():

    @db_save(url, html)
    def store():
        pass

    store()
    res = db_get(url)
    assert res == html
