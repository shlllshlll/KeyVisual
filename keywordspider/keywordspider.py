# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-09 22:14:22
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-13 08:38:32
# @License: MIT LICENSE

from . import spider
from .mykeyword import Keyword
from . import assorules


def working(run_spider=True, run_keyword=True,
            run_assorule=True, max_count=500, use_sql=False):
    if run_spider:
        if not use_sql:
            spider_writer = spider.CsvWriter("data/csv/ifeng.csv",
                                             ["url", "title", "date_", "news"])
        else:
            spider_writer = spider.MysqlWriter("ifeng")
        myspider = spider.Spider(max_count, datawriter=spider_writer)
        myspider.start_working()

    if run_keyword:
        if not use_sql:
            keyword_writer = spider.CsvWriter(
                "data/csv/ifeng_key.csv", ["url", "title", "keywords"])
            keyword_reader = spider.CsvReader("data/csv/ifeng.csv")
        else:
            keyword_writer = spider.MysqlWriter("ifeng_key")
            keyword_reader = spider.MysqlReader("ifeng")
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
            asso_fre_writer = spider.PandasMysqlWriter("ifeng_frequent")
            asso_con_writer = spider.PandasMysqlWriter("ifeng_confidence")
            asso_reader = spider.PandasMysqlReader("ifeng_key")
        myassorules = assorules.Assokeyword(
            asso_reader, asso_fre_writer, asso_con_writer)
        myassorules.working(min_support=0.015, min_confidence=0.1,
                            find_rules=True, max_len=4)
