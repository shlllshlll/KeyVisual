# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-24 17:33:18
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-10 15:10:30
# @License: MIT LICENSE


class DataSaver(object):

    def __init__(self, writer):
        self._writer = writer

    def working(self, data):
        self._writer.working(data)


class DataReader(object):

    def __init__(self, reader):
        self._reader = reader

    def working(self):
        return self._reader.working()
