import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import tensorflow as tf
import sys
sys.path.append('..')
from data_out import *

# 获取数据
path = os.path.abspath("..")
path = path + "\data.csv"
ZGPA = pd.read_csv(path)
ZGPA.index = ZGPA['date']
ZGPA = ZGPA.sort_index(ascending=True, axis=0)

# 创建数据框
new_data = pd.DataFrame(index=range(0,len(ZGPA)),columns=['Date', 'Close'])
for i in range(0,len(ZGPA)):
    new_data['Date'][i] = ZGPA.index[len(ZGPA) - i - 1]
    new_data['Close'][i] = ZGPA["close"][i]

# 设置索引
new_data.index = new_data.Date
new_data.drop('Date', axis=1, inplace=True)

# 创建训练集和验证集
dataset = new_data.values

print(dataset)
train = dataset[0:402,:]# 2017-2018年为训练集
#print(train)
valid = dataset[402:,:]# 2019年为测试集

# 将数据集转换为x_train和y_train
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

x_train, y_train = [], []
for i in range(60,len(train)):
    x_train.append(scaled_data[i-60:i,0])
    y_train.append(scaled_data[i,0])
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

# 创建和拟合LSTM网络
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=50))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

# 使用过去值来预测246个值
inputs = new_data[len(new_data) - len(valid) - 60:].values
inputs = inputs.reshape(-1,1)
inputs  = scaler.transform(inputs)

X_test = []
for i in range(60,inputs.shape[0]):
    X_test.append(inputs[i-60:i,0])
X_test = np.array(X_test)
#print(X_test)

X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
closing_price = model.predict(X_test)
closing_price = scaler.inverse_transform(closing_price)

rms = np.sqrt(np.mean(np.power((valid-closing_price),2)))
print(rms)

valid = new_data[402:]
valid['Predictions'] = closing_price
#print(valid['Predictions'])
#print(type(closing_price))
# 图表
train = new_data[:402]
valid = new_data[402:]
train.to_csv('train.csv')
valid['Predictions'] = closing_price
valid.to_csv('valid.csv')
# draw_plot(train['Close'], valid['Predictions'], valid['Close'], u'LSTM算法对中国平安收盘价的预测')
# print(train['Close'])
# print(valid['Close'])
print(valid['Predictions'])
plt.plot(train['Close'], label = '训练集')
plt.plot(valid['Close'], label = '真实值')
plt.plot(valid['Predictions'], label = '预测值')
plt.legend()
plt.xlabel(u'天数')
plt.ylabel(u'股价')
plt.title(u'LSTM算法对中国平安收盘价的预测')
plt.show()