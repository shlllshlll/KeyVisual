# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email:  shlll7347@gmail.com
# @Date:   2018-03-20 22:45:19
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-10 14:57:45
# @License: MIT LICENSE

import logging
from .instances import *
from .utils import *


class SpiderSingleThread(object):
    """The Scheduler class."""

    def __init__(self, max_count, save_in_database=False):
        start_url = ["http://news.ifeng.com/"]
        allow_domin = "news.ifeng.com"
        para_url_reg = r"http://news.ifeng.com/a/\d{8}/\d{8}_\d.shtml"
        csv_filename = "data/csv/ifeng.csv"
        csv_header = ["url", "title", "date", "news"]
        urls_queue = EliminateQueue(start_url)
        self._fetcher = Fetcher(urls_queue, allow_domin)
        self._parser = Parser(para_url_reg, urls_queue, allow_domin)
        csvwriter = CsvWriter(csv_filename, csv_header)
        self._datasaver = DataSaver(csvwriter)
        self._max_count = max_count

    def start_working(self):
        logging.info("Spider started...")
        count = 1
        while(count <= self._max_count):
            try:
                url, content = self._fetcher.working()
            except IndexError:
                logging.error("Url queue is empty.")
                return
            except Exception:
                continue
            item = self._parser.working(url, content)
            if item:
                self._datasaver.working(item)
            logging.info("loop:%s,url:%s,title:%s", count, url, item["title"])
            count += 1
        logging.info("Spider ended...")
