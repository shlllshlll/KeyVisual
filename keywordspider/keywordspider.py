# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-09 22:14:22
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-10 14:55:53
# @License: MIT LICENSE

from . import spider
from .mykeyword import Keyword
from . import assorules
from . import crash_on_ipy


def working(
        run_spider=True, run_keyword=True, run_assorule=True, max_count=500):
    if run_spider:
        myspider = spider.Spider(max_count=500)
        myspider.start_working()

    if run_keyword:
        mykeyword = Keyword()
        mykeyword.working()

    if run_assorule:
        myassorules = assorules.Assokeyword()
        fre_df, con_df = myassorules.working(
            min_support=0.02, min_confidence=0.1,
            find_rules=True, max_len=4)
        fre_df.to_csv("data/csv/ifeng_frequent.csv", encoding="utf-8")
        con_df.to_csv("data/csv/ifeng_confidence.csv", encoding="utf-8")
