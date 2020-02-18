import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

#打开文件
path = os.path.abspath("..")
path = path + "\data.csv"
ZGPA = pd.read_csv(open(path))

ZGPA.index = ZGPA['date']
ZGPA = ZGPA.sort_index(ascending=True, axis=0)

print(ZGPA)
dataset = ZGPA['close']
# print(dataset.head())
# print(dataset[1])

# def count_rsi(start, end):
#     RSI = 0.0
#     bigger = 0
#     smaller = 0
#     for i in (start, end):
#         if dataset[start + 1] > dataset[start]:
#             bigger += dataset[start + 1] - dataset[start]
#         else:
#             smaller += dataset[start] - dataset[start + 1]
#     RSI = bigger / (bigger + smaller) *100
#     return RSI

RSI_set = []
#计算RSI值
for i in range(0, len(ZGPA)-14):
    RSI = 0.0
    bigger_set = 0
    smaller_set = 0
    for j in range(0, 13):
        if dataset[i + j + 1] > dataset[i + j]:
            bigger_set += dataset[i + j + 1] - dataset[i + j]
        else:
            smaller_set += dataset[i + j] - dataset[i + j +1]
    RSI = bigger_set / (bigger_set + smaller_set) * 100
    if i < 5:
        print(bigger_set)
        print(smaller_set)
        print(RSI)
    RSI_set.append(RSI)

dic = {'超买市场（RSI>=80）且实际下跌': 0,
       '超买市场（RSI>=80）但实际上涨': 0,
       '强势市场（50<=RSI<80）且实际下跌': 0,
       '强势市场（50<=RSI<80）但实际上涨': 0,
       '弱式市场（50>RSI>=20）且实际上涨': 0,
       '弱式市场（50>RSI>=20）但实际下跌': 0,
       '超卖市场（RSI<20）且实际上涨': 0,
       '超卖市场（RSI<20）但实际下跌': 0}

for i in range(0, len(ZGPA)-15):
    if (RSI_set[i] >= 80) & (dataset[i + 15] >= dataset[i + 14]):
        dic['超买市场（RSI>=80）但实际上涨'] += 1
    elif (RSI_set[i] >= 80) & (dataset[i + 15] < dataset[i + 14]):
        dic['超买市场（RSI>=80）且实际下跌'] += 1
    elif (RSI_set[i] < 80) & (RSI_set[i] >= 50) & (dataset[i + 15] >= dataset[i + 14]):
        dic['强势市场（50<=RSI<80）但实际上涨'] += 1
    elif (RSI_set[i] < 80) & (RSI_set[i] >= 50) & (dataset[i + 15] < dataset[i + 14]):
        dic['强势市场（50<=RSI<80）且实际下跌'] += 1
    elif (RSI_set[i] < 50) & (RSI_set[i] >= 20) & (dataset[i + 15] >= dataset[i + 14]):
        dic['弱式市场（50>RSI>=20）且实际上涨'] += 1
    elif (RSI_set[i] < 50) & (RSI_set[i] >= 20) & (dataset[i + 15] < dataset[i + 14]):
        dic['弱式市场（50>RSI>=20）但实际下跌'] += 1
    elif (RSI_set[i] < 20) & (dataset[i + 15] >= dataset[i + 14]):
        dic['超卖市场（RSI<20）且实际上涨'] += 1
    else:
        dic['超卖市场（RSI<20）但实际下跌'] += 1

print(dic)
# for i in (0, 10):
#     print(count_rsi(i, i + 9))