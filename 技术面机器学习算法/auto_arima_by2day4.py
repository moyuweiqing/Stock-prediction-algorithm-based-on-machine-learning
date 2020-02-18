# 自回归积分滑动平均模型
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import os
#from statsmodels.tsa.arima_model import ARIMA
from pmdarima import auto_arima
import sys
sys.path.append('..')
from data_out import *


# 获取数据
path = os.path.abspath("..")
path = path + "\data.csv"
ZGPA = pd.read_csv(path)
ZGPA.index = ZGPA['date']
data = ZGPA.sort_index(ascending=True, axis=0)

forecast = []
for i in range(150, 208):
    # 划分训练集和测试集
    train = data[:402 + i]# 2017-2018年的为训练接
    valid = data[402 + i:]# 2019年的为测试集

    # 对收盘价进行测试
    training = train['close']
    validation = valid['close']

    # 使用2017-2018的数据进行训练
    model = auto_arima(training, start_p=1, start_q=1,max_p=2, max_q=2, m=2,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True)
    #model = ARIMA(train,order=(1, 1, 1))
    model.fit(training)

    # 使用2019年的数据进行预测
    forecast.append(model.predict(n_periods=1))
    #forecast = pd.DataFrame(forecast,index = valid.index,columns=['Prediction'])

print(forecast)
# rms = np.sqrt(np.mean(np.power((np.array(valid['close'])-np.array(forecast['Prediction'])),2)))
# print(rms)

# print(forecast)
# 图表

# train.to_csv('train.csv')
# forecast.to_csv('f.csv')
# valid.to_csv('valid.csv')
draw_plot(train['close'], forecast['Prediction'], valid['close'], u'自回归积分滑动平均模型对中国平安收盘价的预测')
# plt.plot(train['close'], label = u'训练集')
# plt.plot(valid['close'], label = u'真实值')
# plt.plot(forecast['Prediction'], label = u'预测值')
# plt.legend()
# plt.xlabel(u'天数')
# plt.ylabel(u'股价')
# plt.title(u'自回归积分滑动平均模型对中国平安收盘价的预测')
# plt.show()