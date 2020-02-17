import matplotlib.pyplot as plt
import numpy as np
from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False		# 显示负号

basic = [1.0013746258107434, 1.0097912855479794, 1.0200087310826542, 1.0260347372359888, 1.032385560452353, 1.0288307625145519, 1.0212508315316813, 1.0322374438716115, 1.0284279893563943, 1.011147721603193, 1.0160485614501913, 1.0197644686512557, 1.0226930192915349, 1.0110022035589554, 1.0137098785963745, 1.0058882837186096, 0.998134250789955, 1.0011251663063363, 0.9912195451521703]
prophet = [1.0188, 1.0219, 1.0028, 1.0076, 0.9879, 1.0257, 1.0332, 1.0294, 1.0355, 1.0433000000000001, 1.0472000000000001, 1.0568000000000002, 1.0682000000000003, 1.0678, 1.0635000000000001, 1.0579000000000003, 1.0424000000000002, 1.0200000000000005, 1.0156000000000003, 0.9936000000000004]
ls_basic = [1.0103, 0.999, 1.0057, 1.0162, 1.0165, 1.0453, 1.0567, 1.0395, 1.0503, 1.0441, 1.022, 1.0154, 1.0406, 1.0411, 1.0354, 1.0417, 1.0083, 0.9897, 1.0074, 1.0027]

basic_yield = []
prophet_yield = []
LSTM_yield = []

def count(y, z):
    a = y - 1;
    b = a * 365
    z.append(b)

for i in basic:
    count(i, basic_yield)
for i in prophet:
    count(i, prophet_yield)
for i in ls_basic:
    count(i, LSTM_yield)

def beta(x, y):
    a = np.cov(x,y)
    b = np.cov(y)
    return a/b

print(beta(ls_basic, basic))
plt.plot(basic_yield, label='基准年化收益率')
plt.plot(prophet_yield, label='prophet模型预测下的年化收益率')
#plt.plot(ma, label='移动平均收益率')
plt.plot(LSTM_yield, label='LSTM模型预测下的年化收益率')
plt.legend()
plt.xlabel(u'天数')
plt.ylabel(u'收益率')
plt.title('沪深300的股票收益率图')
plt.show()
