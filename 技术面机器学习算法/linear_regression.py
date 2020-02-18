import pandas as pd
import numpy as np
import datetime
import math
import os
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import sys
sys.path.append('..')
from data_out import *

# 读取文件
path = os.path.abspath("..")
path = path + "\data.csv"
ZGPA = pd.read_csv(path,index_col='date',parse_dates=True)

# 文件的内容处理
df = ZGPA[['open',  'high',  'low',  'close', 'volume']]
df['HL_PCT'] = (df['high'] - df['low']) / df['close'] * 100.0
df['PCT_change'] = (df['close'] - df['open']) / df['open'] * 100.0
df = df[['close', 'HL_PCT', 'PCT_change', 'volume']]
df = df.sort_index(ascending=True, axis=0)

# 预测股票交易收市值，这里预测70天
forecast_col = 'close'
forecast_out = int(math.ceil(0.01 * len(df)) * 10)#对70天后的数据进行预测

# 设置实际值
rowset = []
for i in range(0,forecast_out):
    rowset.append(df['close'].iloc[len(df) - forecast_out + i])

# 重新构建X和y，X为[‘Close’, ‘HL_PCT’, ‘PCT_change’, ‘Volume’]，y为[‘label’]表示forecast_out天后的股票值，使用preprocessing.scale对数据集进行scaling。
# X_lately 表示后forecast_out天 的数据集，既对应的y值为NAN
df['label'] = df[forecast_col].shift(-forecast_out)#这里将原来的数据进行截取了
#print(df['label'])
X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]
df.dropna(inplace=True)
y = np.array(df['label'])

# 选择数据集80%作为训练集，20%作为测试集
# 使用sklearn提供的Linear Regression函数进行建模，最后使用测试集进行测试，计算相应的精确度
X_train, X_test, y_train ,y_test =train_test_split(X,y,test_size=0.2)
clf = LinearRegression()
clf.fit(X_train,y_train)
accuracy = clf.score(X_test,y_test)
#print(accuracy)

# forecast_set是我们通过训练集训练出的模型和我们的最近的数据进行的预测
# 把我们的预测集放入之前的DataFrame，最后绘图得到股票走势图
forecast_set = clf.predict(X_lately)
#print(forecast_set,accuracy,forecast_out)
df['Forecast']=np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
print(last_date,last_unix)
one_day = 86400
next_unix = last_unix + one_day

# 遍历预测结果，用它往df追加行
# 这些行除了Forecast字段，其他都设为np.nan
for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += 86400
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]

# 回传实际值
df['row'] = np.nan
for i in range(0, forecast_out):
    df['row'].iloc[len(df) - forecast_out + i] = rowset[i]

df_f = df['Forecast']
df_r = df['row']
rms = np.sqrt(np.mean(np.power((np.array(df_f[-forecast_out:])-np.array(df_r[-forecast_out:])),2)))
print(rms)

# 图表
draw_plot(df['close'], df['Forecast'], df['row'], u'线性回归算法对中国平安收盘价的预测')
# df['close'].plot()
# df['Forecast'].plot()
# df['row'].plot()
# df.to_csv("test.csv")
# plt.show()