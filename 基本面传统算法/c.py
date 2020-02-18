# 获取每年的数据
import tushare as ts
import pandas as pd

hs300 = ts.get_hs300s()

df = pd.DataFrame(columns=('code', '2017_2', '2017_3', '2018_1', '2018_2', '2018_3', '2019_1', '2019_2',  '2019_3_start', '2019_3_true_end'))
# 获取沪深300成分股自2017年5月24日起的交易数据
for j in range(0, 300):
    t2017_2s, t2017_3s, t2018_1s, t2018_2s, t2018_3s, t2019_1s, t2019_2s = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    t2017_2e, t2017_3e, t2018_1e, t2018_2e, t2018_3e, t2019_1e, t2019_2e = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    a2017_2s, a2017_3s, a2018_1s, a2018_2s, a2018_3s, a2019_1s, a2019_2s = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    a2017_2e, a2017_3e, a2018_1e, a2018_2e, a2018_3e, a2019_1e, a2019_2e = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    rate1, rate2, rate3, rate4, rate5, rate6, rate7 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,

    temp = ts.get_hist_data(hs300['code'].loc[j], start='2017-08-28', end='2017-09-08').sort_index(ascending=True)
    if temp['close'].count() < 5:
        continue
    for i in range(0, 5):
        t2017_2s += temp['close'].iloc[i]
        t2017_2e += temp['close'].iloc[-1 - i]
    a2017_2s = t2017_2s / 5
    a2017_2e = t2017_2e / 5
    rate1 = a2017_2e / a2017_2s

    temp = ts.get_hist_data(hs300['code'].loc[j], start='2017-10-23', end='2017-11-03').sort_index(ascending=True)
    if temp['close'].count() < 5:
        continue
    for i in range(0, 5):
        t2017_3s += temp['close'].iloc[i]
        t2017_3e += temp['close'].iloc[-1 - i]
    a2017_3s = t2017_3s / 5
    a2017_3e = t2017_3e / 5
    rate2 = a2017_3e / a2017_3s

    temp = ts.get_hist_data(hs300['code'].loc[j], start='2018-04-23', end='2018-05-04').sort_index(ascending=True)
    if temp['close'].count() < 5:
        continue
    for i in range(0, 5):
        t2018_1s += temp['close'].iloc[i]
        t2018_1e += temp['close'].iloc[-1 - i]
    a2018_1s = t2018_1s / 5
    a2018_1e = t2018_1e / 5
    rate3 = a2018_1e / a2018_1s

    temp = ts.get_hist_data(hs300['code'].loc[j], start='2018-08-27', end='2018-09-07').sort_index(ascending=True)
    if temp['close'].count() < 5:
        continue
    for i in range(0, 5):
        t2018_2s += temp['close'].iloc[i]
        t2018_2e += temp['close'].iloc[-1 - i]
    a2018_2s = t2018_2s / 5
    a2018_2e = t2018_2e / 5
    rate4 = a2018_2e / a2018_2s

    temp = ts.get_hist_data(hs300['code'].loc[j], start='2018-10-22', end='2018-11-02').sort_index(ascending=True)
    if temp['close'].count() < 5:
        continue
    for i in range(0, 5):
        t2018_3s += temp['close'].iloc[i]
        t2018_3e += temp['close'].iloc[-1 - i]
    a2018_3s = t2018_3s / 5
    a2018_3e = t2018_3e / 5
    rate5 = a2018_3e / a2018_3s

    temp = ts.get_hist_data(hs300['code'].loc[j], start='2019-04-22', end='2019-05-03').sort_index(ascending=True)
    if temp['close'].count() < 5:
        continue
    for i in range(0, 5):
        t2019_1s += temp['close'].iloc[i]
        t2019_1e += temp['close'].iloc[-1 - i]
    a2019_1s = t2019_1s / 5
    a2019_1e = t2019_1e / 5
    rate6 = a2019_1e / a2019_1s

    temp = ts.get_hist_data(hs300['code'].loc[j], start='2019-08-26', end='2019-09-06').sort_index(ascending=True)
    if temp['close'].count() < 5:
        continue
    for i in range(0, 5):
        t2019_2s += temp['close'].iloc[i]
        t2019_2e += temp['close'].iloc[-1 - i]
    a2019_2s = t2019_2s / 5
    a2019_2e = t2019_2e / 5
    rate7 = a2019_2e / a2019_2s

    temp = ts.get_hist_data(hs300['code'].loc[j], start='2019-10-28', end='2019-11-08').sort_index(ascending=True)
    if temp['close'].count() < 5:
        continue
    start = 0.0
    end = 0.0
    for i in range(0, 5):
        start += temp['close'].iloc[i]
        end += temp['close'].iloc[-1 - i]
    start = start / 5
    end = end / 5

    df.loc[j] = [str(hs300['code'].loc[j]), rate1, rate2, rate3, rate4, rate5, rate6, rate7, start, end]

df.to_csv('data.csv')