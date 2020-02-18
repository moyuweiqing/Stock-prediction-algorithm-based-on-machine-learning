# 对季报和股票情况进行合并
import pandas as pd
import tushare as ts

hs300 = ts.get_hs300s()

d2017_1 = pd.read_csv('2017_1_c.csv')
d2017_2 = pd.read_csv('2017_2_c.csv')
d2017_3 = pd.read_csv('2017_3_c.csv')
d2018_1 = pd.read_csv('2018_1_c.csv')
d2018_2 = pd.read_csv('2018_2_c.csv')
d2018_3 = pd.read_csv('2018_3_c.csv')
d2019_1 = pd.read_csv('2019_1_c.csv')
d2019_2 = pd.read_csv('2019_2_c.csv')
d2019_3 = pd.read_csv('2019_3_c.csv')
row_data = pd.read_csv('data.csv')
df = pd.DataFrame(columns=('code', '2017_2', '2017_3', '2018_1', '2018_2', '2018_3', '2019_1', '2019_2', '2017_2_roe', '2017_3_roe', '2018_1_roe', '2018_2_roe',
                           '2018_3_roe', '2019_1_roe', '2019_2_roe', '2019_3_roe', '2019_3_start', '2019_3_true_end'))
for i in range(0, row_data['code'].count()):
    t = row_data['code'].loc[i]
    l0 = d2017_1.loc[d2017_1['code'] == int(t)]
    if l0['roe'].count() < 1:
        continue
    roe0 = l0['roe'].iloc[0]

    l1 = d2017_2.loc[d2017_2['code'] == int(t)]
    if l1['roe'].count() < 1:
        continue
    roe1 = l1['roe'].iloc[0] - roe0

    #t2 = hs300['code'].loc[i]
    l2 = d2017_3.loc[d2017_3['code'] == int(t)]
    if l2['roe'].count() < 1:
        continue
    roe2 = l2['roe'].iloc[0] - roe1 - roe0

    #t3 = hs300['code'].loc[i]
    l3 = d2018_1.loc[d2018_1['code'] == int(t)]
    if l3['roe'].count() < 1:
        continue
    roe3 = l3['roe'].iloc[0]

    #t4 = hs300['code'].loc[i]
    l4 = d2018_2.loc[d2018_2['code'] == int(t)]
    if l4['roe'].count() < 1:
        continue
    roe4 = l4['roe'].iloc[0] - roe3

    #t5 = hs300['code'].loc[i]
    l5 = d2018_3.loc[d2018_3['code'] == int(t)]
    if l5['roe'].count() < 1:
        continue
    roe5 = l5['roe'].iloc[0] - roe4 - roe3

    #t6 = hs300['code'].loc[i]
    l6 = d2019_1.loc[d2019_1['code'] == int(t)]
    if l6['roe'].count() < 1:
        continue
    roe6 = l6['roe'].iloc[0]

    #t7 = hs300['code'].loc[i]
    l7 = d2019_2.loc[d2019_2['code'] == int(t)]
    if l7['roe'].count() < 1:
        continue
    roe7 = l7['roe'].iloc[0] - roe6

    l8 = d2019_3.loc[d2019_3['code'] == int(t)]
    if l8['roe'].count() < 1:
        continue
    roe8 = l8['roe'].iloc[0] - roe7 - roe6
    #row = row_data.loc[row_data['code'] == int(t)]
    #print(row)
    # code = row['code'].iloc[0]
    a2017_2 = row_data['2017_2'].iloc[i]
    a2017_3 = row_data['2017_3'].iloc[i]
    a2018_1 = row_data['2018_1'].iloc[i]
    a2018_2 = row_data['2018_2'].iloc[i]
    a2018_3 = row_data['2018_3'].iloc[i]
    a2019_1 = row_data['2019_1'].iloc[i]
    a2019_2 = row_data['2019_2'].iloc[i]
    start = row_data['2019_3_start'].iloc[i]
    end = row_data['2019_3_true_end'].iloc[i]

    df.loc[i] = [t, a2017_2, a2017_3, a2018_1, a2018_2, a2018_3, a2019_1, a2019_2, roe1, roe2, roe3, roe4, roe5, roe6, roe7, roe8, start, end]

df.to_csv('data2.csv')
print(df)