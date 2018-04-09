# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-03-30 10:28:00
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-04-09 10:53:12
# @License: MIT LICENSE

import pandas as pd
import assorules as asr


class Assokeyword(object):

    def read_data(self, filename="data/csv/ifeng_key.csv"):
        news_item = pd.read_csv(filename, encoding="utf8")     # 从csv文件中读取数据
        keywords = list(map(lambda x: x.split(
            '/'), news_item["keywords"]))   # 从数据中提取关键词数据
        del news_item     # 删除无用的变量
        self.key_df = pd.DataFrame(keywords)
        del keywords

    def find_frequence_item(self):
        # if not self.key_df:
        #     raise ValueError(
        #         "Please use read_dat() to build a keyword dataframe.")
        key_column, key_tr_array = asr.transaction_encoder(self.key_df)
        df_tr = pd.DataFrame(key_tr_array, columns=key_column)
        # df_tr.loc[:, ("中非", "非洲", "习近平")].head()
        # 提取出现一次以上的关键词
        res_df = asr.apriori(df_tr, min_support=0.03, min_confidence=0.1,
                             find_rules=True, max_len=4, use_colnames=True)
        return res_df


if __name__ == "__main__":
    assoKeyword = Assokeyword()
    assoKeyword.read_data()
    fre_df, con_df = assoKeyword.find_frequence_item()
    fre_df.to_csv("data/csv/ifeng_frequent.csv", encoding="utf-8")
    con_df.to_csv("data/csv/ifeng_confidence.csv", encoding="utf-8")
