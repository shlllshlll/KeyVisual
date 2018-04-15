# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-26 17:01:32
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-12 21:04:04
# @License: MIT LICENSE

import logging
# import jieba
from jieba import analyse
from . import utils


class Keyword(object):

    def __init__(self, datawriter, datareader):
        self._datasaver = datawriter
        self._datareader = datareader

    def working(self):
        logging.info("Start finding paragraph keywords...")
        count = 1
        for news_dict in self._datareader.working():
            url = news_dict[0]
            title = news_dict[1]
            news = news_dict[3]
            # seg = "/".join(jieba.cut(news))
            # tfidf = "/".join(analyse.tfidf(news))
            # textrank = "/".join(analyse.textrank(news))
            keywords = "/".join(analyse.tfidf(news)[:10])
            seg_dict = utils.add_dict(
                url=url, title=title, keywords=keywords)
            # seg_dict = utils.add_dict(
            #     title=title, news=news, seg=seg,
            #     tfidf=tfidf, textrank=textrank, keywords=keywords)
            logging.info("loop:%s, keyword:%s", count, keywords)
            self._datasaver.working(seg_dict)
            count += 1
        self._datareader.close()
        self._datasaver.close()
        logging.info("End finding paragraph keywords...")
