import tushare as ts
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os

from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 获取中国平安三年内K线数据
ZGPA = ts.get_hist_data('000001')
ZGPA.index = pd.to_datetime(ZGPA.index)
# 相关指数
print(ZGPA.tail())#输出最后五行的数据
plt.plot(ZGPA['close'], label=u'收盘价')
plt.plot(ZGPA['ma5'], label='MA5')
plt.plot(ZGPA['ma20'], label='MA20')
plt.legend()
plt.xlabel(u'日期')
plt.ylabel(u'股价')
plt.title(u'中国平安收盘价，MA5，MA20时间序列')
plt.show()

path = os.path.abspath("")
path = path + "\data.csv"
ZGPA.to_csv(path)#写入到csv文件中