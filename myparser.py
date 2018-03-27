# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-22 21:21:05
# @Last Modified by:   Mr.Shi
# @Last Modified time: 2018-03-26 13:59:24
# @License: MIT LICENSE

import re
from lxml import etree


class Parser(object):
    """The html content parser."""

    def __init__(self, para_url_reg, allow_domin=None):
        """Initialize the Parser class.

        Arguments:
            para_url_reg {object} -- The compiled regular expression object.

        Keyword Arguments:
            allow_domin {string} -- The allowed url domin. (default: {None})
        """
        self.allow_domin = allow_domin
        self.para_url_pat = re.compile(para_url_reg)

    def parse_html(self, url, content):
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
        if self.para_url_pat.match(url):
            # Extract the news title date and news
            title = root.xpath("//title/text()")
            date = root.xpath(
                "//span[@class='ss01']/text() |"
                " //div[@class='yc_tit']/p[1]/span[1]/text()")
            news = self._get_news_para(
                root,
                "//div[@id='main_content']/p/text() |"
                " //div[@id='yc_con_txt']/p[not(@class)]//text()")
            if title and date and news:
                news_item = self._get_news_item(
                    url, str(title[0]), str(date[0]), news)

        # Extract urls from page.
        urls = self._get_page_links(root)
        return news_item, urls

    def _get_news_item(self, url, title, date, news):
        """Return a news item dict"""
        return {"url": url, "title": title, "date": date, "news": news}

    def _get_news_para(self, root, xpath):
        """Return the news paragraph."""
        para = ""
        for news in root.xpath(xpath):
            para += str(news) + "\n"
        return para

    def _get_page_links(self, root):
        """Get links from html content."""
        # TODO(SHLLL): To optimize the urls filter flow.
        urls = filter(
            lambda x: self.para_url_pat.match(x),
            root.xpath("//*[@href]/@href"))
        urls = [str(url).replace('\n', '') for url in urls]
        return urls


if __name__ == "__main__":
    import requests

    para_url_reg = r"http://news.ifeng.com/a/\d{8}/\d{8}_\d.shtml"
    parser = Parser(para_url_reg)
    url = "http://news.ifeng.com/a/20180324/57025940_0.shtml"
    response = requests.get(url)
    response.encoding = "utf-8"
    parser.parse_html(url, response.text)
