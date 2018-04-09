# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email:  shlll7347@gmail.com
# @Date:   2018-03-20 22:45:19
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-09 10:54:36
# @License: MIT LICENSE

from downloader import Downloader
from myparser import Parser
from datapipe import CsvWriter
from pynput import keyboard
import crash_on_ipy


class Schedule(object):
    """The Scheduler class."""

    def __init__(self):
        start_url = "http://news.ifeng.com/"
        allow_domin = "news.ifeng.com"
        para_url_reg = r"http://news.ifeng.com/a/\d{8}/\d{8}_\d.shtml"
        csv_filename = "data/csv/ifeng.csv"
        csv_header = ["url", "title", "date", "news"]
        self.stopflag = False
        listener = keyboard.Listener(on_press=self._on_press)
        listener.start()
        self.downloader = Downloader(start_url, allow_domin)
        self.parser = Parser(para_url_reg, allow_domin)
        self.csvwriter = CsvWriter(csv_filename, csv_header)

    def spider_scheduler(self):
        count = 0
        while not self.stopflag:
            try:
                url, content = self.downloader.download_url()
            except Exception:
                continue
            print("loop%d: %s" % (count, url))
            item, urls = self.parser.parse_html(url, content)
            if item:
                self.csvwriter.write_line(item)
            count += 1
            self.downloader.add_urls(urls)

    def _on_press(self, key):
        if key.char == 'q':
            self.stopflag = True
            return False


if __name__ == "__main__":
    schedule = Schedule()
    schedule.spider_scheduler()
