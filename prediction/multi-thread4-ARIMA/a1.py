# 自回归积分滑动平均模型
import tushare as ts
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import xlrd
import matplotlib.pyplot as plt
import os
from pmdarima import auto_arima

from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

hs300 = ts.get_hs300s()
suspend = [209, 290]
day_yield = {}
choosed_stocks = []

def chooseStock(day):
    for i in range(0, 1):
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-01-02', end='2019-09-30').sort_index(ascending=True, axis=0)
        if (len(temp) != 183):
            continue
        train = temp[:163]
        valid = temp[163:]

        # 对收盘价进行测试
        training = train['close']
        validation = valid['close']

        model = auto_arima(training, start_p=1, start_q=1, max_p=3, max_q=3, m=24, start_P=0, seasonal=True, d=1, D=1,
                           trace=True, error_action='ignore', suppress_warnings=True)
        # model = ARIMA(train,order=(1, 1, 1))
        model.fit(training)

        forecast = model.predict(n_periods=20)
        forecast = pd.DataFrame(forecast, index=valid.index, columns=['Prediction'])

        print(forecast)
        print(train['close'])
        plt.plot(train['close'], label = '原数据集')
        plt.plot(forecast['Prediction'], label='ARIMA模型预测下的股票收盘价')
        plt.plot(valid['close'], label='实际值')
        plt.legend()
        plt.show()

chooseStock(0)