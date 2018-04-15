# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-13 00:45:47
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-13 01:19:35
# @License: MIT LICENSE

from lxml import etree
from .inst_parser import Parser


class IfengParser(Parser):
    """The html content parser."""

    def __init__(self, para_url_reg, urls_queue, allow_domin=None):
        super().__init__(para_url_reg, urls_queue, allow_domin)

    def working(self, url, content):
        """Parser the html content.

        Arguments:
            url {str} -- The input url.
            content {str} -- The html content.

        Returns:
            dict, list -- The news item dict and urls list.
        """
        root = etree.HTML(content)
        news_item = None
        # text = etree.tostring(root, encoding="utf-8").decode("utf-8")

        # If the url is a paragraph url.
        if self._para_url_pat.match(url):
            # Extract the news title date and news
            title = root.xpath("//title/text()")
            date = root.xpath(
                "//span[@class='ss01']/text() |"
                " //div[@class='yc_tit']/p[1]/span[1]/text()")
            news = self._get_news_para(
                root,
                "//div[@id='main_content']/p/text() |"
                " //div[@id='yc_con_txt']/p[not(@class)]//text()")
            if title and date and news.replace("\n", ""):
                news_item = self._get_news_item(
                    url, str(title[0].replace("'", '"')), str(date[0]), news)

        # Extract urls from page.
        urls = self._get_page_links(root)
        self._urls_queue.push(urls)
        return news_item
