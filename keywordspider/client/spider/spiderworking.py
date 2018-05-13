# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email:  shlll7347@gmail.com
# @Date:   2018-03-20 22:45:19
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-05-13 17:03:06
# @License: MIT LICENSE

import logging
from .instances import *
from .utils import *


class SpiderSingleThread(object):
    """The Scheduler class."""

    def __init__(self, max_count, datawriter, msg_queue=None):
        start_url = ["http://www.ifeng.com", "http://news.ifeng.com"]
        allow_domin = "news.ifeng.com"
        para_url_reg = r"http://news.ifeng.com/a/\d{8}/\d{8}_\d.shtml"
        urls_queue = EliminateQueue(start_url)
        self._urls_queue = urls_queue
        self._fetcher = Fetcher(urls_queue, allow_domin)
        self._parser = IfengParser(para_url_reg, urls_queue, allow_domin)
        self._datasaver = datawriter
        self._max_count = max_count
        self._msg_queue = msg_queue

    def start_working(self):
        logging.info("Spider started...")
        loop_count = 1
        news_count = 1
        while(news_count <= self._max_count):
            try:
                url, content = self._fetcher.working()
            except IndexError:
                logging.error("Url queue is empty.")
                return
            except Exception:
                continue
            item = self._parser.working(url, content)
            self._msg_queue.put('spider', news_count / self._max_count)
            if item:
                logging.info("loop:%s,url:%s,title:%s",
                             loop_count, url, item["title"])
                self._datasaver.working(item)
                news_count += 1
            else:
                logging.info("loop:%s,url:%s,title:None", loop_count, url)
            loop_count += 1
        self._msg_queue.put('spider', 2)
        self._datasaver.close()
        logging.info("Spider ended...")
