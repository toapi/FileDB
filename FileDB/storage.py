#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
store the html content and url
"""

import time
import hashlib
import os
from sqlalchemy import create_engine


class DiskStore:

    """
    DiskStore will create a hidden file --html at local path
    You can give a path like: "/Users/toapi/" or "/Users/toapi"
    then the hidden file --html will created in given path "/User/toapi/.html"
    file name is a hash of url
    about get function:
    you can give 3 params: url, default and expiration
    url: the source url you want to request
    default: return to you the default if instance can not find url source stored in disk
    expiration: means that you do not need source stored over expiration
    """

    path = os.getcwd()

    def __init__(self, path='./'):

        try:
            os.listdir(path)
        except Exception as e:
            raise TypeError("Please input correct path")

        if path.endswith("/"):
            if not os.path.exists(path + ".html"):
                os.makedirs(path + ".html")
            self.path = path + ".html/"
        else:
            if not os.path.exists(path + "/.html"):
                os.makedirs(path + "/.html")
            self.path = path + "/.html/"

    def save(self, url, html):

        file_name = hashlib.md5(url.encode()).hexdigest()
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(self.path + file_name, "w", encoding="utf-8") as f:
            f.write(html)
        return True

    def get(self, url, default=None, expiration="inf"):

        file_name = hashlib.md5(url.encode()).hexdigest()
        file_path = self.path + file_name

        try:
            # file change date
            change_date = os.stat(file_path).st_ctime
            if (time.time() - change_date) > float(expiration):
                # delete file
                os.remove(file_path)
                return default

            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
            return data
        except FileNotFoundError as e:
            return default


class DBStore:
    """
    about storage, storage is a dict including keys DB_URL and NAME
    support database: mysql, postgresql, sqlite, oracle e.t.
    Mysql:
        db_url: "mysql://name:password@host/dbname",
    and so on
    about get function:
    you can give 3 params: url, default and expiration
    url: the source url you want to request
    default: return to you the default if instance can not find url source stored in disk
    expiration: means that you do not need source stored over expiration
    """
    MYSQL_SQL = """CREATE TABLE IF NOT EXISTS `FileDB`(
                   `url` VARCHAR(100),
                   `html` MEDIUMTEXT NOT NULL,
                   `create_time` FLOAT NOT NULL,
                   PRIMARY KEY ( `url` )) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8;"""
    SQLITE_SQL = """CREATE TABLE IF NOT EXISTS FileDB(
                    url VAR(100) PRIMARY KEY,
                    html TEXT,
                    create_time FLOAT);"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_url = "sqlite:///"+os.path.join(basedir, 'data.sqlite')

    def __init__(self, db_url=db_url):

        self.db = create_engine(db_url)
        if db_url.startswith("mysql"):
            self.db.execute(self.MYSQL_SQL)
        elif db_url.startswith("sqlite"):
            self.db.execute(self.SQLITE_SQL)
        else:
            self.db.execute(self.MYSQL_SQL)

    def save(self, url, html):

        file_name = hashlib.md5(url.encode()).hexdigest()
        html_store = html.replace("\"", "toapi###$$$###toapi")
        html_store = html_store.replace("\'", "toapi***$$$***toapi").encode("unicode-escape")
        sql = """SELECT html 
                 FROM FileDB
                 WHERE url="{}";""".format(file_name)
        row = self.db.execute(sql).first()
        if row:
            sql = """UPDATE FileDB 
                     SET html="{}", create_time="{}" 
                     WHERE url="{}";""".format(html_store, time.time(), file_name)
            self.db.execute(sql)
            return True
        else:
            self.db.execute("""INSERT INTO FileDB (url, html, create_time) VALUES ("{}", "{}", "{}");""".format(
                file_name, html_store, time.time()))
            return True

    def get(self, url, default=None, expiration="inf"):

        file_name = hashlib.md5(url.encode()).hexdigest()
        row = self.db.execute("SELECT html, create_time FROM FileDB where url='{}';".format(file_name)).first()
        try:
            origin_data = dict(row).get("html")
            create_time = dict(row).get("create_time")
            if (time.time() - create_time) > float(expiration):
                self.db.execute("DELETE FROM FileDB WHERE url='{}';".format(file_name))
                return default
            data = eval(origin_data).decode("unicode-escape")
            data = data.replace("toapi###$$$###toapi", "\"").replace("toapi***$$$***toapi", "\'")
        except TypeError as e:
            return default
        return data
