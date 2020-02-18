# 乱来的
import tushare as ts
import pandas as pd

hs300 = ts.get_hs300s()
ts.set_token('dc60f140542542d2d520eb9d694310cc06da8451cadf709262db1f63')
pro = ts.pro_api()
#print(hs300)
stock_list = []
q = []
for i in range(0, 300):
    stock_list.append(hs300['code'].iloc[i])

for i in range(0, 300):
    if stock_list[i].startswith('60'):
        q.append(str(stock_list[i]+'.SH'))
    elif stock_list[i].startswith('00'):
        q.append(str(stock_list[i]+'.SZ'))
    else:
        q.append(str(stock_list[i]+'.SH'))
print(q)
temp1 = ts.get_profit_data(2018, 1)
for i in stock_list[:1]:
    t = temp1.loc[temp1['code'] == i]
    print(t['roe'].iloc[0])

print(stock_list)
for i in range(0, 10):
    a = ts.get_hist_data(hs300['code'].loc[i], start='2012-05-01', end='2012-12-31')
    print(a)
# for i in range(0, 300):
#     #a = ts.get_hist_data(hs300['code'].loc[i], start='2017-05-01', end='2017-12-31')
#     a = pro.daily(ts_code = str(q[i]), start_date='20170501', end_date='20171231')
#     if a.empty:
#         print(i)