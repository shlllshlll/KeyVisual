# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-09 21:33:16
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-09 21:44:01
# @License: MIT LICENSE

import binascii
from collections import deque


class EliminateQueue(object):

    def __init__(self, start_list=[], encoding="utf-8"):
        start_set_list = [binascii.crc32(i.encode(encoding))
                          for i in start_list]
        self._encoding = encoding
        self._queue = deque(start_list)
        self._set = set(start_set_list)

    def push(self, item_list):
        for item in item_list:
            item_crc = binascii.crc32(item.encode("utf-8"))
            if item_crc in self._set:
                continue
            self._set.add(item_crc)
            self._queue.append(item)

    def pop(self):
        return self._queue.popleft()
