# -*- coding: utf-8 -*-
# @Author: SHLLL
# @Email: shlll7347@gmail.com
# @Date:   2018-04-03 21:50:02
# @Last Modified by:   SHLLL
# @Last Modified time: 2018-05-12 23:44:52
# @License: MIT LICENSE

# from itertools import combinations
import logging
import pandas as pd
import numpy as np
# from scipy.sparse import csr_matrix


def transaction_encoder(df, sparse=False):
    key_column = np.sort(
        np.unique(df.unstack().dropna().values))   # 提取所有的关键词作为标签并去重
    key_col_map = {}
    for (index,), item in np.ndenumerate(key_column):   # 将关键词-位置数据对存入字典中
        key_col_map[item] = index
    # TODO(SHLLL): 使用稀疏矩阵而不是numpy矩阵
    if(sparse):
        pass
        # indptr = [0]
        # indices = []
        # for row_idx, row in df.iterrows():
        #     for item in row.dropna().drop_duplicates():    # 去除None和重复的元素
        #         col_idx = key_col_map[item]
        #         indices.append(col_idx)
        #     indptr.append(len(indices))
        # non_sparse_values = [1] * len(indices)
        # tr_array = csr_matrix((non_sparse_values, indices, indptr), dtype=bool)
    #     df_tr = pd.SparseDataFrame(key_tr_array, columns=key_column)
    else:
        tr_array = np.zeros((df.shape[0], key_column.shape[0]), dtype=bool)
        for row_idx, row in df.iterrows():
            for item in row.dropna():     # 去除None
                col_idx = key_col_map[item]
                tr_array[row_idx, col_idx] = True
    return key_column, tr_array


def _generate_new_combinations(old_combinations):
    # 将输入的项集扁平化并去重保存
    item_types_in_previous_step = np.unique(old_combinations.flatten())
    # 取出原候选项集中的每一个项
    for old_combination in old_combinations:
        max_combination = max(old_combination)    # 取出该项中包含的最大列序号
        for item in item_types_in_previous_step:  # 取出当前候选集每一个对应的列序号即关键词
            if item > max_combination:
                res = tuple(old_combination) + (item,)     # 组合形成新的候选项集
                yield res
                # TODO(SHLLL): 增加枝叶修剪


def _find_frequent_items(df, min_support, max_len):
    # 这里进行了一项内容，即支持度的过滤
    X = df.values     # 取Dataframe的值存取ndarray中
    ary_col_idx = np.arange(X.shape[1])     # 创建一个列索引序列
    # 计算每个关键词出现的概率即支持度
    support = (np.sum(X, axis=0) / float(X.shape[0]))
    # 将大于最小支持度的支持度存入字典
    support_dict = {1: support[support > min_support]}
    # 这里进行了支持度过滤即由候选集C1生成了频繁项集L1并存入字典中
    itemset_dict = {
        1: ary_col_idx[support > min_support].reshape(-1, 1)}  # 取出支持度对应的编号
    max_itemset = 1
    rows_count = X.shape[0]

    if max_len is None:
        max_len = float('inf')      # 设置max_len为无穷大

    while max_itemset and max_itemset < max_len:
        next_max_itemset = max_itemset + 1
        combin = _generate_new_combinations(
            itemset_dict[max_itemset])
        frequent_items = []
        frequent_items_support = []

        for c in combin:
            together = X[:, c].all(axis=1)  # 这里进行与运算即每一行均为True结果为True
            support = together.sum() / rows_count    # 计算当前项的支持度
            if support >= min_support:    # 提取当前候选项集中的频繁项
                frequent_items.append(c)
                frequent_items_support.append(support)

        if frequent_items:    # 如果找到了频繁项则将对应的项和支持度存入字典
            itemset_dict[next_max_itemset] = np.array(
                frequent_items)
            support_dict[next_max_itemset] = np.array(
                frequent_items_support)
            max_itemset = next_max_itemset
        else:     # 如果没有频繁项则表示当前已无可供寻找的频繁项
            max_itemset = 0
    return itemset_dict, support_dict


def _combinations(
        item, count=1, begin=0, stack=[], stack_invert=None, result=[]):
    # 这里使用了迭代法实现组合的问题
    # 判断是否是numpy的ndarray类型
    if isinstance(item, np.ndarray):
        item = item.tolist()  # 转换为list类型

    if stack_invert is None:    # stack_invert存储与结果相反的元素
        stack_invert = item.copy()

    # 如果已经提取完成所有的元素则返回
    if not count:
        result.append([stack.copy(), stack_invert.copy()])
        return
    # 如果已经达到了list的末尾则直接返回
    if begin == len(item):
        return

    # 针对第begin个元素可以选择把该元素放入组合中
    stack.append(item[begin])
    stack_invert.remove(item[begin])
    _combinations(item, count - 1, begin + 1, stack, stack_invert, result)
    # 或者是选择从begin之后的元素取出来
    stack_invert.append(stack.pop())
    _combinations(item, count, begin + 1, stack, stack_invert, result)

    return result


def _ganerate_asso_rules(df, item, min_conf):
    # 在本函数中我们根据频繁项生成其关联规则
    X = df.values   # 取出DataFrame数据存入ndarray中
    conf_list = []
    # 依次生成1~n-1项后件
    for i in range(1, item.shape[0]):
        result = _combinations(item, count=i, result=[])
        # 依次取出生成的i后件及对应的前件
        for back_item, front_item in result:
            # 接下来计算前后件之间的置信度
            # back_sup = X[:, back_item].all(axis=1).sum()
            front_sup = X[:, front_item].all(axis=1).sum()
            all_sup = X[:, item].all(axis=1).sum()
            confidence = all_sup / front_sup    # 这里计算了置信度
            # 直接打印置信度信息
            # print(str(front_item) + "->" +
            #       str(back_item) + "=" + str(confidence))
            if confidence > min_conf:
                conf_list.append((front_item, back_item, confidence))
    return conf_list


def _find_asso_rules(df, itemset_dict, support_dict, min_conf):
    # 在本函数中我们寻找最终发关联规则a=>b
    # 判断当前频繁项集中存在长度为2以上的项集
    if 2 not in itemset_dict:
        raise ValueError("Support dict dosen't have item langer then 2.")

    conf_list = []
    # 从长度为2开始的频繁项开始遍历
    for k in sorted(itemset_dict)[1:]:
        # 从频繁项集中取出每一个频繁项
        for freq_item in itemset_dict[k]:
            # 对每个频繁项执行置信度计算
            conf_list.extend(_ganerate_asso_rules(df, freq_item, min_conf))
    conf_df = pd.DataFrame.from_records(
        conf_list, columns=["front_item", "back_item", "confidence"])
    return conf_df


def apriori(
        df, min_support=0.5, min_confidence=0.5,
        use_colnames=False, find_rules=False, max_len=None):
    itemset_dict, support_dict = _find_frequent_items(df, min_support, max_len)
    con_df = None
    if find_rules:
        try:
            con_df = _find_asso_rules(
                df, itemset_dict, support_dict, min_confidence)
        except ValueError:
            logging.error("No confidence item found.")
            con_df = None

    all_fre = []
    for k in sorted(itemset_dict):    # 取出字典中的key
        support = pd.Series(support_dict[k])    # 取出对应的支持度
        itemsets = pd.Series([i for i in itemset_dict[k]])   # 取出对应的关键词标号
        res = pd.concat((support, itemsets), axis=1)   # 横向拼接两个Series为Dataframe
        all_fre.append(res)        # 将所有的Dataframe存入到List中

    fre_df = pd.concat(all_fre)    # 纵向拼接所有的Dataframe
    fre_df.columns = ["support", "itemsets"]   # 为数据起一个标题
    if use_colnames:
        mapping = {idx: item for (idx,), item in np.ndenumerate(
            df.columns)}  # 创建一个索引--关键词名的mapping
        fre_df["itemsets"] = fre_df["itemsets"].apply(
            lambda x: "/".join([mapping[i] for i in x]))
        if con_df is not None:
            con_df["front_item"] = con_df["front_item"].apply(
                lambda x: "/".join([mapping[i] for i in x]))
            con_df["back_item"] = con_df["back_item"].apply(
                lambda x: "/".join([mapping[i] for i in x]))
    fre_df = fre_df.reset_index(drop=True)
    return fre_df, con_df


__all__ = ["transaction_encoder", "apriori"]
