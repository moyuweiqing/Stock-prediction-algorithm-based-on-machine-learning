import tushare as ts
import pandas as pd
import numpy as np
from pmdarima import auto_arima

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

lastday = pd.DataFrame(columns=['code',
                                '03-03', '03-10', '03-17', '03-24',
                                '03-31', '04-07', '04-14', '04-21', '04-28',
                                '05-05', '05-12', '05-19', '05-26',
                                '06-02', '06-09', '06-16', '06-23',
                                '06-30', '07-07', '07-14', '07-21', '07-28',
                                '08-04', '08-11', '08-17', '08-25',
                                '09-01', '09-08', '09-15', '09-22'])

for each in range(20, 30):
    d = data['code'].iloc[each]
    # 获取个股数据并做初步处理
    temp = ts.get_hist_data(code = d, start='2017-06-01', end='2019-12-01').sort_index(ascending=True)
    temp['line'] = range(0, len(temp))
    temp['date'] = temp.index
    temp.index = temp['line']

    last_list = []
    predict_list = []
    last_list.append(d)
    predict_list.append(d)
    for i in datelist:

        # 获取特定列
        a = temp.loc[temp['date'] == i].index.tolist()
        if len(a) != 0:
            print(a[0])
        if len(a) == 0:
            predict_list.append(0)
            continue
        pin = a[0]

        # 传入前一期收盘价
        last_list.append(temp['close'].iloc[pin - 1])

        # 划分训练集和测试集
        train = temp[:pin]
        valid = temp[pin:]

        #对收盘价进行测试
        training = train['close']
        #validation = valid['close']

        # 训练
        model = auto_arima(training, start_p=1, start_q=1,max_p=2, max_q=2, m=2,start_P=0, seasonal=True,d=1, D=1, trace=True,error_action='ignore',suppress_warnings=True)
        model.fit(training)

        # 进行预测
        forecast = model.predict(n_periods=1)
        print(forecast[0])

        # 传入预测价
        predict_list.append(forecast[0])

    lastday.loc[each] = last_list
    results.loc[each] = predict_list

results.to_csv('t3_predict.csv')
lastday.to_csv('t3_lastday.csv')