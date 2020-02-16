import tushare as ts
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os

from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

#获取沪深上市公司的基本情况
data = ts.get_stock_basics()
print(data.head())
#data.index = data['code']
data = data.sort_index(ascending=True, axis = 0)
data.to_csv('stock_basics1.csv', encoding = 'gbk')