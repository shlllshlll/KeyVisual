# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-22 21:21:05
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-23 00:11:28
# @License: MIT LICENSE

import re


class Parser(object):
    """The html content parser."""

    def __init__(self, para_url_reg, urls_queue, allow_domin=None):
        """Initialize the Parser class.

        Arguments:
            para_url_reg {object} -- The compiled regular expression object.

        Keyword Arguments:
            allow_domin {string} -- The allowed url domin. (default: {None})
        """
        self._urls_queue = urls_queue
        # self._allow_domin = allow_domin
        self._para_url_pat = re.compile(para_url_reg)

    def _get_news_item(self, url, title, date, news):
        """Return a news item dict"""
        return {"url": url, "title": title, "datee": date, "news": news}

    def _get_news_para(self, root, xpath):
        """Return the news paragraph."""
        para = ""
        for news in root.xpath(xpath):
            para += str(news).replace('\xa0', '').replace("'", '"') + "\n"

        return para

    def _get_page_links(self, root):
        """Get links from html content."""
        # TODO(SHLLL): 优化url的过滤流程即不只保留新闻url
        urls = filter(
            lambda x: self._para_url_pat.match(x),
            root.xpath("//*[@href]/@href"))
        urls = [str(url).replace('\n', '') for url in urls]
        return urls
