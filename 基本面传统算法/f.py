# 与真实值进行比较
import pandas as pd
import numpy as np
import tushare as ts

df = pd.read_csv('data3.csv')
df = df.iloc[:10]
print(df)

total_start = 0.0
total_true_end = 0.0
total_predict_end = 0.0

for i in range(0, 10):
    total_start += df['start'].iloc[i]
    total_true_end += df['true'].iloc[i]
    total_predict_end += df['predict'].iloc[i]

hs300 = ts.get_hist_data(code='hs300', start='2019-10-28', end='2019-11-08').sort_index(ascending=True)
s = 0.0
e = 0.0
for i in range(0, 5):
    s += hs300['close'].iloc[i]
    e += hs300['close'].iloc[-1 - i]

print('预测收益率为'+ str(total_predict_end/total_start))
print('真实收益率为'+str(total_true_end/total_start))
print('沪深300为'+str(e/s))