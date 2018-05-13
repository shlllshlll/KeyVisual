# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-30 10:28:00
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-05-12 16:58:02
# @License: MIT LICENSE

import logging
import pandas as pd
from . import apriori as asr


class Assokeyword(object):

    def __init__(self, datareader, freq_datawriter, conf_datawriter, msg_queue):
        news_item = datareader.working()     # 从csv文件中读取数据
        keywords = list(map(lambda x: x.split(
            '/'), news_item["keywords"]))   # 从数据中提取关键词数据
        del news_item     # 删除无用的变量
        self._key_df = pd.DataFrame(keywords)
        del keywords
        self._datareader = datareader
        self._freq_datawriter = freq_datawriter
        self._conf_datawriter = conf_datawriter
        self._msg_queue = msg_queue

    def working(self, min_support=0.03, min_confidence=0.1,
                find_rules=True, max_len=4):
        logging.info("Start finding associate keywords...")
        self._msg_queue.put("assoword", 1)
        # if not self._key_df:
        #     raise ValueError(
        #         "Please use read_dat() to build a keyword dataframe.")
        key_column, key_tr_array = asr.transaction_encoder(self._key_df)
        df_tr = pd.DataFrame(key_tr_array, columns=key_column)
        # df_tr.loc[:, ("中非", "非洲", "习近平")].head()
        # 提取出现一次以上的关键词
        fre_df, con_df = asr.apriori(df_tr, min_support=min_support,
                                     min_confidence=min_confidence,
                                     find_rules=find_rules, max_len=4,
                                     use_colnames=True)
        logging.info("%s", fre_df)
        self._freq_datawriter.working(fre_df)
        if con_df is not None:
            logging.info("%s", con_df)
            self._conf_datawriter.working(con_df)
        logging.info("End finding associate keywords...")
        self._msg_queue.put("assoword", 2)
        self._datareader.close()
        self._freq_datawriter.close()
        self._conf_datawriter.close()
