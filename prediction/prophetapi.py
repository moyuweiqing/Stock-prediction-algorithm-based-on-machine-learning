import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from fbprophet import Prophet
import pystan

# 出了点问题
def make_new_dataset(dataset):
    new_data = pd.DataFrame(index=range(0, len(dataset)), columns=['Date', 'Close'])
    for i in range(0, len(dataset)):
        new_data['Date'][i] = dataset.index[i]
        new_data['Close'][i] = dataset['close'][i]

    new_data['Date'] = pd.to_datetime(new_data.Date, format='%Y-%m-%d')
    new_data.index = new_data['Date']
    # 准备数据
    new_data.rename(columns={'Close': 'y', 'Date': 'ds'}, inplace=True)
    return new_data

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