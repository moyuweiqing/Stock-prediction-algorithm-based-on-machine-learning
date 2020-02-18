import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
from sklearn import neighbors
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing, svm
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
scaler = MinMaxScaler(feature_range=(0, 1))
import sys
sys.path.append('..')
from data_out import *

path = os.path.abspath("..")
path = path + "\data.csv"
ZGPA = pd.read_csv(path)

df = ZGPA[['open',  'high',  'low',  'close', 'volume']]
df['HL_PCT'] = (df['high'] - df['low']) / df['close'] * 100.0
df['PCT_change'] = (df['close'] - df['open']) / df['open'] * 100.0
df = df[['close', 'HL_PCT', 'PCT_change', 'volume']]
df = df.sort_index(ascending=True, axis=0)

forecast_col = 'close'
forecast_out = int(math.ceil(0.01 * len(df)) * 10)#对70天后的数据进行预测

# 设置实际值
rowset = []
for i in range(0,forecast_out):
    rowset.append(df['close'].iloc[len(df) - forecast_out + i])

# 重新构建X和y，X为[‘Close’, ‘HL_PCT’, ‘PCT_change’, ‘Volume’]，y为[‘label’]表示forecast_out天后的股票值，使用preprocessing.scale对数据集进行scaling。
# X_lately 表示后forecast_out天 的数据集，既对应的y值为NAN
df['label'] = df[forecast_col].shift(-forecast_out)#这里将原来的数据进行截取了

X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]
df.dropna(inplace=True)
y = np.array(df['label'])

# 选择数据集80%作为训练集，20%作为测试集
# 使用sklearn提供的Linear Regression函数进行建模，最后使用测试集进行测试，计算相应的精确度
X_train, X_test, y_train ,y_test =train_test_split(X,y,test_size=0.2)

# 缩放数据
x_train_scaled = scaler.fit_transform(X_train)
x_train = pd.DataFrame(x_train_scaled)
x_valid_scaled = scaler.fit_transform(X_test)
x_valid = pd.DataFrame(x_valid_scaled)

# 使用gridsearch查找最佳参数
params = {'n_neighbors':[2,3,4,5,6,7,8,9]}
knn = neighbors.KNeighborsRegressor()
model = GridSearchCV(knn, params, cv=5)

# 拟合模型并进行预测
model.fit(x_train,y_train)
preds = model.predict(x_valid)

df['Predictions'] = 0
df['Predictions'] = preds

draw_plot(df['close'], df['Predictions'], df['close'], u'K近邻算法对中国平安收盘价的预测')