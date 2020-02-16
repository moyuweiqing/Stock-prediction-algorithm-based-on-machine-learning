import tushare as ts
import pandas as pd
import numpy as np

datelist = ['03-04', '03-11', '03-18', '03-25',
            '04-01', '04-08', '04-15', '04-22', '04-29',
            '05-06', '05-13', '05-20', '05-27',
            '06-03', '06-10', '06-17', '06-24',
            '07-01', '07-08', '07-15', '07-22', '07-29',
            '08-05', '08-12', '08-19', '08-26',
            '09-02', '09-09', '09-16', '09-23']

df = pd.DataFrame(columns=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
data = pd.read_csv('predict.csv')
print(data)

for d in datelist:
    data = data.sort_values(by=d, ascending=False)
    a = []
    for i in range(0, 10):
        a.append(str(data['code'].iloc[i]))
    print(a)