# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-10 14:51:32
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-13 08:59:53
# @License: MIT LICENSE

import logging
import keywordspider as kwspider
import keywordspider.crash_on_ipy


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(filename)s[line:%(lineno)d]"
                        " - %(levelname)s: %(message)s")
    kwspider.working(run_spider=True, run_keyword=True, run_assorule=True,
                     max_count=500, use_sql=True)