# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-25 00:41:04
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-03-28 00:35:15
# @License: MIT LICENSE

import sys


class ExceptionHook:
    instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            from IPython.core import ultratb
            self.instance = ultratb.FormattedTB(
                mode='Plain',
                color_scheme='Linux', call_pdb=1)
        return self.instance(*args, **kwargs)


sys.excepthook = ExceptionHook()
