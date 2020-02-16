import tushare as ts
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import xlrd
from fbprophet import Prophet
import pystan

hs300 = ts.get_hs300s()
suspend = [209, 290]
day_yield = {}
choosed_stocks = []
f = open('data19.txt', 'w')

def make_prediction(training_set, validation_set):
    model = Prophet()
    model.fit(training_set)

    # 预测
    close_prices = model.make_future_dataframe(periods=len(validation_set))
    forecast = model.predict(close_prices)
    forecast_valid = forecast[-1:]
    # print(forecast)
    last_day = forecast[-2:-1]
    #print(last_day)
    #print(forecast_valid)
    # a = forecast_valid['yhat'][1] - last_day['yhat'][1]
    y= (forecast.iat[-1, -1] - forecast.iat[-2, -1]) / forecast.iat[-2, -1]
    # print(y)
    return y
    #forecast_valid = forecast['yhat'][402:]

def getDayStock(day):
    for i in range(0, 300):
        if i in suspend:
            continue
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-01-02', end='2019-09-30')
        temp = temp.sort_index(ascending=True)
        # print(temp.head())
        new_data = pd.DataFrame(index=range(0, len(temp)), columns=['Date', 'Close'])
        for j in range(0, len(temp)):
            new_data['Date'][j] = temp.index[j]
            new_data['Close'][j] = temp['close'][j]

        new_data['Date'] = pd.to_datetime(new_data.Date, format='%Y-%m-%d')
        new_data.index = new_data['Date']

        # 准备数据
        new_data.rename(columns={'Close': 'y', 'Date': 'ds'}, inplace=True)
        row = temp.iloc[:, 0].size
        # print(temp.head())
        # temp.to_csv('test.csv')
        training_number = row - 20 + day
        training_set = new_data[: training_number]
        validation_set = new_data[training_number:training_number + 1]
        prediction = make_prediction(training_set, validation_set)
        day_yield[i] = prediction

def sortAndChoose(dict, n): # dict是预测的股票和收益率，n是股票个数
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

getDayStock(18)
print(day_yield)
choosed_stocks = sortAndChoose(day_yield, 10)