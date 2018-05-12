# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-05-10 19:54:19
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-05-12 22:09:07
# @License: MIT LICENSE

import queue
import logging
from multiprocessing import Process
from . import spider
from .mykeyword import Keyword
from . import assorules


class RunSpiderInServer(Process):

    def __init__(self, option, queue):
        # 调用父类的初始化方法
        super().__init__()

        self._queue = QueuePutter(queue)

        # 设置log的记录格式
        logging.basicConfig(level=logging.INFO,
                            format="%(filename)s[line:%(lineno)d]"
                            " - %(levelname)s: %(message)s")

        # 创建数据存取器
        if option['saveMethod'] == 'csv':
            self.spider_writer = spider.CsvWriter(
                "data/csv/ifeng.csv",
                ["url", "title", "datee", "news"])
            self.keyword_writer = spider.CsvWriter(
                "data/csv/ifeng_key.csv", ["url", "title", "keywords"])
            self.keyword_reader = spider.CsvReader("data/csv/ifeng.csv")
            self.asso_fre_writer = spider.PandasCsvWriter(
                "data/csv/ifeng_frequent.csv")
            self.asso_con_writer = spider.PandasCsvWriter(
                "data/csv/ifeng_confidence.csv")
            self.asso_reader = spider.PandasCsvReader("data/csv/ifeng_key.csv")
        else:
            self.spider_writer = spider.MysqlWriter("client_content")
            self.keyword_writer = spider.MysqlWriter("client_keyword")
            self.keyword_reader = spider.MysqlReader("client_content")
            self.asso_fre_writer = spider.PandasMysqlWriter("client_frequent")
            self.asso_con_writer = spider.PandasMysqlWriter(
                "client_confidence")
            self.asso_reader = spider.PandasMysqlReader("client_keyword")

        # 设置爬虫爬取的条目数
        self.max_count = int(option['spiderNum'])
        # 设置最小支持度和置信度
        self.min_support = float(option['minSupp'])
        self.min_confidence = float(option['minConf'])
        # 设置运行对应的模块

        def func(x):
            return x == 'true'
        self.run_server = func(option['runSpider'])
        self.run_keyword = func(option['runKeyword'])
        self.run_assorule = func(option['runAssoword'])

    def run(self):
        self._queue.put("running", 1)
        if self.run_server:
            myspider = spider.Spider(
                self.max_count, datawriter=self.spider_writer, msg_queue=self._queue)
            myspider.start_working()
        if self.run_keyword:
            mykeyword = Keyword(self.keyword_writer,
                                self.keyword_reader, msg_queue=self._queue)
            mykeyword.working()
        if self.run_assorule:
            myassorules = assorules.Assokeyword(
                self.asso_reader, self.asso_fre_writer, self.asso_con_writer, msg_queue=self._queue)
            myassorules.working(
                min_support=self.min_support,
                min_confidence=self.min_confidence,
                find_rules=True, max_len=4)
        self._queue.put("running", 2)


class QueuePutter(object):

    def __init__(self, queue):
        self._queue = queue
        self._data = {"running": 0, "spider": 0, "keyword": 0, "assoword": 0}

    def put(self, key, value):
        try:
            self._queue.get_nowait()
        except queue.Empty:
            pass
        if key in self._data.keys():
            if isinstance(value, float):
                value = round(value, 2)
            self._data[key] = value
        try:
            self._queue.put_nowait(self._data)
        except queue.Full:
            pass
