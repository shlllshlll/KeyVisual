# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-09 22:14:22
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-05-22 16:47:46
# @License: MIT LICENSE

import os
import subprocess
from . import spider
from .mykeyword import Keyword
from . import assorules


def working(run_server=True, run_spider=True, run_keyword=True,
            run_assorule=True, max_count=500, use_sql=False):
    if run_server:
        # 采用非阻塞的方式运行django服务器并屏蔽默认的输出
        FNULL = open(os.devnull, 'w')
        server = subprocess.Popen(
            ['keywordspider/manage.py', 'runserver'], stdout=FNULL)

    if run_spider:
        if not use_sql:
            spider_writer = spider.CsvWriter("data/csv/ifeng.csv",
                                             ["url", "title", "datee", "news"])
        else:
            spider_writer = spider.MysqlWriter("client_content")
        myspider = spider.Spider(max_count, datawriter=spider_writer)
        myspider.start_working()

    if run_keyword:
        if not use_sql:
            keyword_writer = spider.CsvWriter(
                "data/csv/ifeng_key.csv", ["url", "title", "keywords"])
            keyword_reader = spider.CsvReader("data/csv/ifeng.csv")
        else:
            keyword_writer = spider.MysqlWriter("client_keyword")
            keyword_reader = spider.MysqlReader("client_content")
        mykeyword = Keyword(keyword_writer, keyword_reader)
        mykeyword.working()

    if run_assorule:
        if not use_sql:
            asso_fre_writer = spider.PandasCsvWriter(
                "data/csv/ifeng_frequent.csv")
            asso_con_writer = spider.PandasCsvWriter(
                "data/csv/ifeng_confidence.csv")
            asso_reader = spider.PandasCsvReader("data/csv/ifeng_key.csv")
        else:
            asso_fre_writer = spider.PandasMysqlWriter("client_frequent")
            asso_con_writer = spider.PandasMysqlWriter("client_confidence")
            asso_reader = spider.PandasMysqlReader("client_keyword")
        myassorules = assorules.Assokeyword(
            asso_reader, asso_fre_writer, asso_con_writer)
        myassorules.working(min_support=0.03, min_confidence=0.5,
                            find_rules=True, max_len=4)
    if run_server:
        # 这里在运行完成后关闭服务器
        server.kill()   # 执行完成后杀掉杀掉子进程
