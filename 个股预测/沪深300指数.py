import tushare as ts
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os

hs300 = ts.get_hs300s()
from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

def get_hs300_data():
    hs300 = ts.get_hist_data(code='hs300', start='2019-09-02', end='2019-09-30').sort_index(ascending=True)
    print(hs300)
    predict = []
    for i in range(0, 20, 4):
        basic_yield = hs300['close'][i] / hs300['open'][0]
        #print(hs300['date'][i])
        predict.append(basic_yield)
    print(len(predict))
    return predict