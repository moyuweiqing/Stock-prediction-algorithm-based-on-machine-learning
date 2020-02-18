import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']

#打开文件
path = os.path.abspath("..")
path = path + "\data.csv"
ZGPA = pd.read_csv(open(path))

# 使用日期和目标变量创建数据框
new_data = pd.DataFrame(index=range(0,len(ZGPA)),columns=['date', 'close'])
ZGPA.index = ZGPA['date']
ZGPA = ZGPA.sort_index(ascending=True, axis=0)

for i in range(0,len(ZGPA)): # 使用收盘价进行处理
     new_data['date'][i] = ZGPA.index[len(ZGPA) - i - 1]
     new_data['close'][i] = ZGPA["close"][i]
# print(new_data)
# print(new_data.loc[402])

train = new_data[:402]#2017-2018的数据为训练集，
valid = new_data[402:]#今年的数据为验证集

valid2 = new_data[550:]
#train['date'].min(), train['date'].max(), valid['date'].min(), valid['date'].max()

# 做出预测
preds = []
for i in range(0,208):
    a = train['close'][len(train)-208+i:].sum() + sum(preds)
    b = a/208
    preds.append(b)

pred2 = []
for i in range(0,5):
    a = train['close'][len(train)-5+i:].sum() + sum(pred2)
    b = a/5
    pred2.append(b)

print(pred2)
# 计算rmse
rms = np.sqrt(np.mean(np.power((np.array(valid['close'])-preds),2)))
print(rms)

# rms = np.sqrt(np.mean(np.power((np.array(valid2['close'])-pred2),2)))
# print(rms)
# 图表
valid['Predictions'] = 0
valid['Predictions'] = preds
valid2['Predictions2'] = 0
valid2['Predictions2'] = pred2
train.to_csv('train.csv')
valid.to_csv('valid.csv')
valid2.to_csv('f.csv')
plt.plot(train['close'], label = u'非预测值（时期数）')
plt.plot(valid['Predictions'], label = u'208天时期预测值')
plt.plot(valid['close'], label = u'真实值')
plt.plot(valid2['Predictions2'], label = u'30天时期预测值')
plt.legend()
plt.xlabel(u'天数')
plt.ylabel(u'股价')
plt.title(u'移动平均法对中国平安收盘价的预测')
plt.show()