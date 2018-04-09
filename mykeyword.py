# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-26 17:01:32
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-09 10:54:21
# @License: MIT LICENSE

# import jieba
from jieba import analyse
from datapipe import CsvReader, CsvWriter
import utils


class Keyword(object):

    def __init__(self):
        filenames = ["url", "title", "keywords"]
        # filenames = ["title", "news", "seg", "tfidf", "textrank", "keywords"]
        self.csvwriter = CsvWriter("data/csv/ifeng_key.csv", filenames)
        self.csvreader = CsvReader("data/csv/ifeng.csv")

    def word_segment(self):
        count = 0
        for news_dict in self.csvreader.read_lines():
            url = news_dict["url"]
            title = news_dict["title"]
            news = news_dict["news"]
            # seg = "/".join(jieba.cut(news))
            # tfidf = "/".join(analyse.tfidf(news))
            # textrank = "/".join(analyse.textrank(news))
            keywords = "/".join(analyse.tfidf(news)[:10])
            seg_dict = utils.add_dict(
                url=url, title=title, keywords=keywords)
            # seg_dict = utils.add_dict(
            #     title=title, news=news, seg=seg,
            #     tfidf=tfidf, textrank=textrank, keywords=keywords)
            self.csvwriter.write_line(seg_dict)
            count += 1
            print("loop%d: %s" % (count, title))


if __name__ == "__main__":
    keyword = Keyword()
    keyword.word_segment()
