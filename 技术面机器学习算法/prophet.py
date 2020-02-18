import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from fbprophet import Prophet
import pystan
import sys
sys.path.append('..')
from data_out import *

path = os.path.abspath("..")
path = path + "\data.csv"
ZGPA = pd.read_csv(path)
ZGPA.index = ZGPA['date']
ZGPA = ZGPA.sort_index(ascending=True, axis=0)

# 创建数据框
new_data = pd.DataFrame(index=range(0,len(ZGPA)),columns=['Date', 'Close'])

for i in range(0,len(ZGPA)):
    new_data['Date'][i] = ZGPA['date'][i]
    new_data['Close'][i] = ZGPA['close'][i]

new_data['Date'] = pd.to_datetime(new_data.Date,format='%Y-%m-%d')
new_data.index = new_data['Date']

# 准备数据
new_data.rename(columns={'Close': 'y', 'Date': 'ds'}, inplace=True)

forecast_valid = []
# 训练集和预测集
for i in range(0, 1):
    train = new_data[:402 + i]# 2017-2018年为训练集
    valid = new_data[402 + i:]# 2019年为测试集

    # 拟合模型
    model = Prophet()
    model.fit(train)

    # 预测
    close_prices = model.make_future_dataframe(periods=208)
    forecast = model.predict(close_prices)
    forecast_valid.append(forecast['yhat'][402:])

print(forecast_valid)
# forecast_valid = forecast['yhat'][402:]
# rms = np.sqrt(np.mean(np.power((np.array(valid['y'])-np.array(forecast_valid)),2)))
# print(rms)

valid['Predictions'] = 0
valid['Predictions'] = forecast_valid

train.to_csv('train.csv')
valid.to_csv('valid.csv')
# 图表
draw_plot(train['y'], valid['Predictions'], valid['y'], u'Prophet算法对中国平安收盘价的预测')
# plt.plot(train['y'], label = '训练集')
# plt.plot(valid['y'], label = '真实值')
# plt.plot(valid['Predictions'], label = '真实值')
# plt.legend()
# plt.xlabel(u'天数')
# plt.ylabel(u'股价')
# plt.title(u'Prophet算法对中国平安收盘价的预测')
# plt.show()