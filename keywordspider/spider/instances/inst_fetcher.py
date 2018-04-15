# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-22 21:19:13
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-13 01:30:46
# @License: MIT LICENSE

import requests
from requests.exceptions import HTTPError


class Fetcher(object):
    """The url downloader class."""

    def __init__(self, urls_queue, allow_domin=None):
        """Initialize the Downloader class"""
        self.allow_domin = allow_domin
        self._urls_queue = urls_queue
        user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.146 Safari/537.36")
        self._headers = {'User-Agent': user_agent}

    def working(self):
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
        # try:
        url = self._urls_queue.pop()
        # except IndexError as e:
        #     logging.error(e)
        #     raise
        # else:
        # # It the url not allowed, then raise error
        # if self.allow_domin not in url:
        #     raise ValueError("Url not allowed: %s" % url)
        response = requests.get(url=url, headers=self._headers)
        if not response.status_code == requests.codes.ok:
            raise HTTPError("Status code not ok: %d" %
                            response.status_code)
        response.encoding = "utf-8"
        return url, response.text
