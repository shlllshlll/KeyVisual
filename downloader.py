# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-22 21:19:13
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-03-28 00:35:15
# @License: MIT LICENSE

import binascii
from collections import deque
import requests
from requests.exceptions import HTTPError


class Downloader(object):
    """The url downloader class."""

    def __init__(self, start_url=None, allow_domin=None):
        """Initialize the Downloader class"""
        self.allow_domin = allow_domin
        if isinstance(start_url, str):
            url_list = [start_url]
            url_set = [binascii.crc32(start_url.encode("utf-8"))]
        else:
            url_list = []
            url_set = []
        self.urls_queue = deque(url_list)
        self.urls_set = set(url_set)
        user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.146 Safari/537.36")
        self._headers = {'User-Agent': user_agent}

    def add_urls(self, urls):
        """Add urls to queue.

        This function add the urls list to the queue, and eliminate
        the input urls at the same time.

        Arguments:
            urls {list} -- The urls list to enqueue.
        """
        for url in urls:
            url_crc = binascii.crc32(url.encode("utf-8"))
            if url_crc in self.urls_set:
                continue
            self.urls_set.add(url_crc)
            self.urls_queue.append(url)

    def download_url(self):
        """Download a url from queue.

        This Function down a url from the url queue,and raise a
        error when the queue is empty or the response code is not
        200 or the domin is not allowed.When succeed, return url
        and the response.

        Returns:
            str, str -- The url and response text.

        Raises:
            IndexError -- Means the queue is empty.
            ValueError -- Means the url is not allowed.
            HTTPError -- Means the response is not 200.
        """
        try:
            url = self.urls_queue.popleft()
        except IndexError as e:
            print(e)
            raise
        else:
            # It the url not allowed, then raise error
            if self.allow_domin not in url:
                raise ValueError("Url not allowed: %s" % url)
            response = requests.get(url=url, headers=self._headers)
            if not response.status_code == requests.codes.ok:
                raise HTTPError("Status code not ok: %d" %
                                response.status_code)
            response.encoding = "utf-8"
            return url, response.text


if __name__ == "__main__":
    downloader = Downloader()
    downloader.add_urls(["http://news.ifeng.com/a/20180321/56923852_0.shtml"])
    downloader.download_url()
