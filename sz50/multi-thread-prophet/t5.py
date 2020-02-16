from fbprophet import Prophet
import pystan
import tushare as ts
import pandas as pd
import numpy as np

data = ts.get_sz50s()

datelist = ['2019-03-04', '2019-03-11', '2019-03-18', '2019-03-25',
            '2019-04-01', '2019-04-08', '2019-04-15', '2019-04-22', '2019-04-29',
            '2019-05-06', '2019-05-13', '2019-05-20', '2019-05-27',
            '2019-06-03', '2019-06-10', '2019-06-17', '2019-06-24',
            '2019-07-01', '2019-07-08', '2019-07-15', '2019-07-22', '2019-07-29',
            '2019-08-05', '2019-08-12', '2019-08-19', '2019-08-26',
            '2019-09-02', '2019-09-09', '2019-09-16', '2019-09-23']

results = pd.DataFrame(columns=['code',
                                '03-04', '03-11', '03-18', '03-25',
                                '04-01', '04-08', '04-15', '04-22', '04-29',
                                '05-06', '05-13', '05-20', '05-27',
                                '06-03', '06-10', '06-17', '06-24',
                                '07-01', '07-08', '07-15', '07-22', '07-29',
                                '08-05', '08-12', '08-19', '08-26',
                                '09-02', '09-09', '09-16', '09-23'])

for each in range(40, 50):
    d = data['code'].iloc[each]
    # 获取个股数据并做初步处理
    temp = ts.get_hist_data(code = d, start='2017-06-01', end='2019-12-01').sort_index(ascending=True)
    temp['line'] = range(0, len(temp))
    temp['date'] = temp.index
    temp.index = temp['line']

    predict_list = []
    predict_list.append(d)

    # 创建数据框
    new_data = pd.DataFrame(index=range(0, len(temp)), columns=['date', 'close'])

    for i in range(0, len(temp)):
        new_data['date'][i] = temp['date'][i]
        new_data['close'][i] = temp['close'][i]

    #print(new_data)

    for i in datelist:
        # 获取特定列
        a = new_data.loc[new_data['date'] == i].index.tolist()
        if len(a) != 0:
            print(a[0])
        if len(a) == 0:
            predict_list.append(0)
            continue
        pin = a[0]

        n = new_data.copy()
        n['date'] = pd.to_datetime(n.date, format='%Y-%m-%d')
        n.index = n['date']

        # 准备数据
        n.rename(columns={'close': 'y', 'date': 'ds'}, inplace=True)
        train = n[:pin]  # 2017-2018年为训练集
        valid = n[pin:]  # 2019年为测试集

        # 拟合模型
        model = Prophet()
        model.fit(train)

        # 预测
        close_prices = model.make_future_dataframe(periods=1)
        forecast = model.predict(close_prices)
        predict_list.append(forecast['yhat'][pin])

    results.loc[each] = predict_list

results.to_csv('t5_predict.csv')