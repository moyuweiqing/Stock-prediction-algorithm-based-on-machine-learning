import tushare as ts
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import xlrd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import tensorflow as tf

# 获取数据
hs300 = ts.get_hs300s()
suspend = [209, 290]
choosed_stocks = []
f = open('data.txt', 'w')

my_df = pd.DataFrame(np.arange(0.0, 6000.0).reshape(300, 20),columns=range(0, 20))

def getDayStock(day):
    # my_df.to_csv('test.csv')
    for i in range(260, 300):
        if i in suspend:
            continue
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-01-02', end='2019-09-30')
        temp = temp.sort_index(ascending=True)
        if(len(temp) != 183):
            continue
        # temp.to_csv('test.csv')
        # print(temp.head())
        new_data = pd.DataFrame(index=range(0, len(temp)), columns=['Date', 'Close'])
        for j in range(0, len(temp)):
            new_data['Date'][j] = temp.index[j]
            new_data['Close'][j] = temp['close'][j]

        new_data['Date'] = pd.to_datetime(new_data.Date, format='%Y-%m-%d')
        new_data.index = new_data['Date']
        print(new_data.iloc[162]) # 162是8.30

        new_data.index = new_data.Date
        new_data.drop('Date', axis=1, inplace=True)

        # 创建训练集和验证集
        dataset = new_data.values

        train = dataset[0:163, :]  # 1-8月月训练集
        valid = dataset[163:, :]  # 9月为测试集

        # 将数据集转换为x_train和y_train
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        x_train, y_train = [], []
        for j in range(60, len(train)):
            x_train.append(scaled_data[j - 60:j, 0])
            y_train.append(scaled_data[j, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # 创建和拟合LSTM网络
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(1))

        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

        # 使用过去值来预测
        inputs = new_data[len(new_data) - len(valid) - 60:].values
        inputs = inputs.reshape(-1, 1)
        inputs = scaler.transform(inputs)

        X_test = []
        for j in range(60, inputs.shape[0]):
            X_test.append(inputs[j - 60:j, 0])
        X_test = np.array(X_test)
        # print(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        closing_price = model.predict(X_test)
        closing_price = scaler.inverse_transform(closing_price)

        print(i)
        train = new_data[:163]
        valid = new_data[163:]
        valid['Predictions'] = closing_price
        for j in range(0, 20):
            my_df.iloc[i][j] = valid['Predictions'].iloc[j]
        my_df.to_csv('test8.csv')

def sortAndChoose(dict, n): # dict是预测的股票收益率，n是股票个数
    stocks = []
    result = []
    p = sorted([(k, v) for k, v in dict.items()], reverse=True)
    # print(p)
    s = set()
    for i in p:
        s.add(i[1])
    for i in sorted(s, reverse=True)[:n]:
        for j in p:
            if j[1] == i:
                result.append(j)
    for r in result:
        stocks.append(r[0])
    print(stocks)
    f.write(str(stocks)+'\n')
    return stocks

def count_yield(day):
    day_yield = {}
    for i in range(0, 300):
        if day == 0:
            temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-01-02', end='2019-09-30')
            temp = temp.sort_index(ascending=True)
            a = my_df.iloc[i][0] / temp['close'].iloc[162]
            day_yield[i] = a
        else:
            a = my_df.iloc[i][day] / my_df.iloc[i][day - 1]
            day_yield[i] = a
    b = sortAndChoose(day_yield, 10)
    f.write(str(b)+'\n')
    print(b)

getDayStock(0)
# for i in range(0, 20):
#     count_yield(i)
f.close()