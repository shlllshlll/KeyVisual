# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-10 15:11:51
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-16 20:26:49
# @License: MIT LICENSE

import pymysql
from sqlalchemy import create_engine
import pandas as pd


class _MysqlBase(object):
    _connection = None
    _cursor = None

    def __init__(self):
        self._connect_mysql()

    def __del__(self):
        self._close_mysql()

    def close(self):
        pass
        # self._close_mysql()

    @classmethod
    def _connect_mysql(cls):
        if _MysqlBase._connection is None:
            _MysqlBase._connection = pymysql.connect(
                host='localhost',
                user='shlll',
                password='shihaolei123',
                db='visualize',
                charset='utf8',
            )
            _MysqlBase._cursor = _MysqlBase._connection.cursor()

    @classmethod
    def _close_mysql(cls):
        if _MysqlBase._connection is not None:
            _MysqlBase._connection.close()
            _MysqlBase._connection = None
            _MysqlBase._cursor = None


class MysqlWriter(_MysqlBase):

    def __init__(self, tablename):
        super().__init__()
        self._tablename = tablename
        self._cursor.execute("TRUNCATE TABLE " + tablename)
        self._connection.commit()

    def working(self, data):
        filed = "(" + ",".join(data) + ")"   # 根据传入的字典创建一个field
        value_list = []
        for key in data:
            value_list.append("'" + data[key] + "'")
        values = "(" + ",".join(value_list) + ")"
        sql = "INSERT INTO %s %s VALUES %s;" % (self._tablename, filed, values)
        self._cursor.execute(sql)
        self._connection.commit()


class MysqlReader(_MysqlBase):

    def __init__(self, tablename):
        super().__init__()
        self._tablename = tablename

    def working(self):
        self._cursor.execute("SELECT * FROM " + self._tablename)
        return self._cursor.fetchall()


class _PandasMysqlBase(object):
    _connection = None

    def __init__(self):
        self._connect_mysql()

    def __del__(self):
        self._close_mysql()

    def close(self):
        pass
        # self._close_mysql()

    @classmethod
    def _connect_mysql(cls):
        if _PandasMysqlBase._connection is None:
            engine = create_engine(
                'mysql://shlll:shihaolei123@localhost:3306/visualize?charset=utf8')
            _PandasMysqlBase._connection = engine.connect()

    @classmethod
    def _close_mysql(cls):
        if _PandasMysqlBase._connection is not None:
            _PandasMysqlBase._connection.close()
            _PandasMysqlBase._connection = None


class PandasMysqlWriter(_PandasMysqlBase):

    def __init__(self, tablename):
        super().__init__()
        self._tablename = tablename

    def working(self, df):
        df.to_sql(self._tablename, con=_PandasMysqlBase._connection,
                  if_exists='replace')


class PandasMysqlReader(_PandasMysqlBase):
    def __init__(self, tablename):
        super().__init__()
        self._tablename = tablename

    def working(self):
        df = pd.read_sql("select * from %s;" %
                         self._tablename, con=_PandasMysqlBase._connection)
        return df
