import matplotlib.pyplot as plt
import os
import 沪深300指数 as hs

from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False		# 显示负号

lstm5 = [1.0103, 0.9914648670107186, 1.0359848484848484, 1.0530575539568345, 1.021471793870779, 0.9904229848363927]
prophet = [1.0188, 1.0066988474041967, 0.9883698009067613, 0.9978213507625272, 0.9971737155546583, 1.0367936925098555, 1.0047651463580667, 1.0103052311316125, 1.0037805350911206, 1.0001917361710286, 1.0056659944300395, 1.010808225729316, 1.0093546253425305, 0.9983171278982798, 0.9998119770612015, 0.9880452040721024, 0.9859075002364514, 0.9732824427480918, 0.9958815454010592, 0.9794952681388014]
movingaverage = [1.0139, 0.9983233060459611, 1.005721613889711, 1.0153116665020252, 1.0246096066416288, 1.0531725637477762, 1.0161068552347279, 0.9946236559139785, 1.0026398122800158, 0.9975581168196913, 0.9943892115365686, 1.0175091502621427, 1.032270837457929, 1.0697651372510157, 1.0496772931742617, 1.0314155942467826, 1.0025445292620865, 0.9829293596152032, 0.9970599393019727, 0.9774816176470589]
lstm = [1.0103, 0.9914648670107186, 0.9981143310837634, 1.0128575700189375, 1.0110403819375373, 1.0396856972349313, 1.0511290162140654, 1.0296156893819335, 1.0450746268656717, 1.0344793421182998, 1.011680855276183, 1.0051474955454365, 1.0062856590271734, 1.0067691712600328, 1.0054379491163332, 1.027216250862834, 1.0071920887024273, 0.9928772070626003, 1.0106340288924558, 0.9947420634920635]

prophet_basic = [1.0188, 1.0219, 1.0028, 1.0076, 0.9879, 1.0257, 1.0332, 1.0294, 1.0355, 1.0433000000000001, 1.0472000000000001, 1.0568000000000002, 1.0682000000000003, 1.0678, 1.0635000000000001, 1.0579000000000003, 1.0424000000000002, 1.0200000000000005, 1.0156000000000003, 0.9936000000000004]
LSTM_basic = [1.0103, 0.999, 1.0057, 1.0162, 1.0165, 1.0453, 1.0567, 1.0395, 1.0503, 1.0441, 1.022, 1.0154, 1.0406, 1.0411, 1.0354, 1.0417, 1.0083, 0.9897, 1.0074, 1.0027]
movingaverage_basic = [1.0139, 1.0164, 1.0161, 1.0242, 1.0289, 1.0578, 1.0268, 1.0097, 1.0177, 1.0135, 1.0024, 1.0208, 1.035, 1.0717, 1.0656, 1.0822, 1.056, 1.0344, 1.0435, 1.0557]

prophet_5 = [1.0103, 0.9746, 1.0193, 1.0052, 0.9743]
moving_average_5 = [1.0139, 1.0282, 1.053, 1.0752, 1.1273]
lstm_5 = [1.0188, 1.0576, 1.0599, 1.0681, 1.0085]
hs300_index = hs.get_hs300_data()
print(hs300_index)
plt.plot(hs300_index, label='基准收益率')
plt.plot(prophet_5, label='prophet模型预测下的收益率')
plt.plot(moving_average_5, label='移动平均收益率')
plt.plot(lstm_5, label='LSTM模型预测下的收益率')
plt.legend()
plt.xlabel(u'天数')
plt.ylabel(u'收益率')
plt.title('沪深300的股票收益率图')
plt.show()