import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import tensorflow as tf
import tushare as ts

data = ts.get_sz50s()

datelist = ['2019-03-04', '2019-03-11', '2019-03-18', '2019-03-25',
            '2019-04-01', '2019-04-08', '2019-04-15', '2019-04-22', '2019-04-29',
            '2019-05-06', '2019-05-13', '2019-05-20', '2019-05-27',
            '2019-06-03', '2019-06-10', '2019-06-17', '2019-06-24',
            '2019-07-01', '2019-07-08', '2019-07-15', '2019-07-22', '2019-07-29',
            '2019-08-05', '2019-08-12', '2019-08-19', '2019-08-26',
            '2019-09-02', '2019-09-09', '2019-09-16', '2019-09-23']

datelist2 = ['2019-03-01', '2019-03-08', '2019-03-15', '2019-03-22',
            '2019-03-29', '2019-04-04', '2019-04-12', '2019-04-19', '2019-04-26',
            '2019-04-30', '2019-05-10', '2019-05-17', '2019-05-24',
            '2019-05-31', '2019-06-06', '2019-06-14', '2019-06-21',
            '2019-06-28', '2019-07-05', '2019-07-12', '2019-07-19', '2019-07-26',
            '2019-08-02', '2019-08-09', '2019-08-16', '2019-08-23',
            '2019-08-30', '2019-09-06', '2019-09-12', '2019-09-20']

results = pd.DataFrame(columns=['code',
                                '03-04', '03-11', '03-18', '03-25',
                                '04-01', '04-08', '04-15', '04-22', '04-29',
                                '05-06', '05-13', '05-20', '05-27',
                                '06-03', '06-10', '06-17', '06-24',
                                '07-01', '07-08', '07-15', '07-22', '07-29',
                                '08-05', '08-12', '08-19', '08-26',
                                '09-02', '09-09', '09-16', '09-23'])

for each in range(0, 50):
    d = data['code'].iloc[each]
    # 获取个股数据并做初步处理
    temp = ts.get_hist_data(code = d, start='2017-06-01', end='2019-09-29').sort_index(ascending=True)
    temp2 = ts.get_hist_data(code = d, start='2017-06-01', end='2019-03-03').sort_index(ascending=True)
    l1 = len(temp)
    l2 = len(temp2)
    print(l1)
    if l1 < 400:
        continue;
    print(l2)

    new_data = pd.DataFrame(index=range(0, len(temp)), columns=['Date', 'Close'])
    for i in range(0, len(temp)):
        new_data['Date'][i] = temp.index[i]
        new_data['Close'][i] = temp["close"][i]
    # 设置索引
    new_data.index = new_data.Date
    new_data.drop('Date', axis=1, inplace=True)

    # 创建训练集和验证集
    dataset = new_data.values

    train = dataset[0:l2, :]  # 2017-2018年为训练集
    valid = dataset[l2:, :]  # 2019年为测试集

    # 将数据集转换为x_train和y_train
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(60, len(train)):
        x_train.append(scaled_data[i - 60:i, 0])
        y_train.append(scaled_data[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # 创建和拟合LSTM网络
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

    # 使用过去值来预测144个值
    inputs = new_data[len(new_data) - len(valid) - 60:].values
    inputs = inputs.reshape(-1, 1)
    inputs = scaler.transform(inputs)

    X_test = []
    for i in range(60, inputs.shape[0]):
        X_test.append(inputs[i - 60:i, 0])
    X_test = np.array(X_test)
    # print(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)

    rms = np.sqrt(np.mean(np.power((valid - closing_price), 2)))
    print(rms)

    valid = new_data[l2:]
    valid['Predictions'] = closing_price
    train = new_data[:l2]
    valid = new_data[l2:]
    valid['Predictions'] = closing_price

    date_predicts = []
    date_predicts.append(d)

    for i in range(0, len(datelist)):
        d1 = datelist[i]
        d2 = datelist2[i]
        p = valid.loc[valid.index == d1]
        l1 = p['Predictions'].tolist()
        if len(l1) == 1:
            q = temp.loc[temp.index == d2]
            l2 = q['close'].tolist()
            rate = 0.0
            rate = l2[0] / l1[0]
            date_predicts.append(rate)
        else:
            date_predicts.append(0)
    results.loc[each] = date_predicts
    print('完成'+d)
results.to_csv('predict.csv')