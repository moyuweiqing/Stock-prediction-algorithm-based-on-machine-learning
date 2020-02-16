import tushare as ts
import pandas as pd
import numpy as np

df = pd.DataFrame(columns=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

data = pd.read_csv('row_data2.csv')
data['1_day'] = data['3月4日'] / data['3月3日']
data['2_day'] = data['3月11日'] / data['3月10日']
data['3_day'] = data['3月18日'] / data['3月10日']
data['4_day'] = data['3月25日'] / data['3月24日']
data['5_day'] = data['4月1日'] / data['3月31日']
data['6_day'] = data['4月8日'] / data['4月7日']
data['7_day'] = data['4月15日'] / data['4月14日']
data['8_day'] = data['4月22日'] / data['4月21日']
data['9_day'] = data['4月29日'] / data['4月28日']
data['10_day'] = data['5月6日'] / data['5月5日']
data['11_day'] = data['5月13日'] / data['5月12日']
data['12_day'] = data['5月20日'] / data['5月19日']
data['13_day'] = data['5月27日'] / data['5月26日']
data['14_day'] = data['6月3日'] / data['6月2日']
data['15_day'] = data['6月10日'] / data['6月9日']
data['16_day'] = data['6月17日'] / data['6月16日']
data['17_day'] = data['6月24日'] / data['6月23日']
data['18_day'] = data['7月1日'] / data['6月30日']
data['19_day'] = data['7月8日'] / data['7月1日']
data['20_day'] = data['7月15日'] / data['7月14日']
data['21_day'] = data['7月22日'] / data['7月21日']
data['22_day'] = data['7月29日'] / data['7月28日']
data['23_day'] = data['8月5日'] / data['8月4日']
data['24_day'] = data['8月12日'] / data['8月11日']
data['25_day'] = data['8月19日'] / data['8月18日']
data['26_day'] = data['8月26日'] / data['8月25日']
data['27_day'] = data['9月2日'] / data['9月1日']
data['28_day'] = data['9月9日'] / data['9月8日']
data['29_day'] = data['9月16日'] / data['9月15日']
data['30_day'] = data['9月23日'] / data['9月22日']

data = data.sort_values(by='1_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[0] = a

data = data.sort_values(by='2_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[1] = a

data = data.sort_values(by='3_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[2] = a

data = data.sort_values(by='4_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[3] = a

data = data.sort_values(by='5_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[4] = a

data = data.sort_values(by='6_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[5] = a

data = data.sort_values(by='7_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[6] = a

data = data.sort_values(by='8_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[7] = a

data = data.sort_values(by='9_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[8] = a

data = data.sort_values(by='10_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[9] = a

data = data.sort_values(by='11_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[10] = a

data = data.sort_values(by='12_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[11] = a

data = data.sort_values(by='13_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[12] = a

data = data.sort_values(by='14_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[13] = a

data = data.sort_values(by='15_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[14] = a

data = data.sort_values(by='16_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[15] = a

data = data.sort_values(by='17_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[16] = a

data = data.sort_values(by='18_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[17] = a

data = data.sort_values(by='19_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[18] = a

data = data.sort_values(by='20_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[19] = a

data = data.sort_values(by='21_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[20] = a

data = data.sort_values(by='22_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[21] = a

data = data.sort_values(by='23_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[22] = a

data = data.sort_values(by='24_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[23] = a

data = data.sort_values(by='25_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[24] = a

data = data.sort_values(by='26_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[25] = a

data = data.sort_values(by='27_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[26] = a

data = data.sort_values(by='28_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[27] = a

data = data.sort_values(by='29_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[28] = a

data = data.sort_values(by='30_day', ascending=False)
a = []
for i in range(0, 10):
    a.append(data['code'].iloc[i])
df.loc[29] = a

l = df.iloc[0].tolist()
df.to_csv('prophet.csv')
print(df)