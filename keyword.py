# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-26 17:01:32
# @Last Modified by:   Mr.Shi
# @Last Modified time: 2018-03-26 19:55:44
# @License: MIT LICENSE

import jieba
from jieba import analyse
from datapipe import CsvReader, CsvWriter
import utils


class Keyword(object):

    def __init__(self):
        filenames = ["title", "news", "seg", "tfidf", "textrank"]
        self.csvwriter = CsvWriter("ifeng_key.csv", filenames)
        self.csvreader = CsvReader("ifeng.csv")

    def word_segment(self):
        count = 0
        self.csvwriter.__enter__()
        self.csvreader.__enter__()
        for news_dict in self.csvreader.read_lines():
            title = news_dict["title"]
            news = news_dict["news"]
            seg = "/".join(jieba.cut(news))
            tfidf = "/".join(analyse.extract_tags(news))
            textrank = "/".join(analyse.textrank(news))
            seg_dict = utils.add_dict(
                title=title, news=news, seg=seg,
                tfidf=tfidf, textrank=textrank)
            self.csvwriter.write_line(seg_dict)
            count += 1
            print("loop%d: %s" % (count, title))


if __name__ == "__main__":
    keyword = Keyword()
    keyword.word_segment()
