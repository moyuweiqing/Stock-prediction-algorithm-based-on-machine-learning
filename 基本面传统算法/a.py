# 非AI预测
import tushare as ts
import pandas as pd
import time

#profit_2016 = ts.get_profit_data(2016, 4)
# time.sleep(2)
# profit_2017 = ts.get_profit_data(2017, 4)
# time.sleep(2)
# profit_2018 = ts.get_profit_data(2018, 4)
# profit_2016.index = profit_2016['code']
# profit_2017.index = profit_2017['code']
# profit_2018.index = profit_2018['code']
hs300 = ts.get_hs300s()
first_choose = [600000,600009,600016,600018,600036,600048,600066,600085,600104600153,600176,600233,600271,600276,600309,600340,600346,600352,600383,600398,600406,600436,600487,600519,600522,600535,600566,600585,600606,600660,600663,600674,600688,600690,600703,600704,600705,600741,600809,600867,600886,600887,600900,600919,601009,601012,601021,601138,601155,601166,601169,601186,601216,601229,601238,601288,601298,601318,601328,601398,601577,601668,601818,601838,601877,601888,601939,601985,601988,601997,601998,603156,603160,603259,603260,603288,603833,603858,603986,1,2,69,333,402,408,538,568,596,651,661,786,858,895,963,1979,2001,2007,2008,2027,2032,2050,2081,2120,2142,2146,2179,2202,2236,2271,2294,2304,2310,2311,2352,2410,2415,2460,2466,2468,2475,2508,2555,2558,2624,2739,2773,2925,300003,300015,300033,300124,300136,300144,300296,300408,300498]
second_choose = [600066,
600068,
600111,
600489,
600886,
600900,
601633,
601766,
601808,
601899,
601997,
603259,
603833,
603986,
69,
876,
961,
2024,
2027,
2044,
2065,
2241,
2311,
2415,
2475,
2601,
2714,
2938,
300015,
300033,
300059,
300072,
300144,
300433,
300498]

# 筛选过去三年roe均大于10的股票
def first_round(hs300):
    global first_choose
    # result1 = pd.merge(hs300, profit_2016, on='code')
    # result1.drop_duplicates(subset=['code'], keep='first', inplace=True)
    # result1.to_csv('test.csv', encoding='gbk')
    result2 = pd.merge(hs300, profit_2017, on='code')
    result2.drop_duplicates(subset=['code'],keep='first',inplace=True)
    result2.to_csv('test1.csv', encoding='gbk')
    result3 = pd.merge(hs300, profit_2018, on='code')
    result3.drop_duplicates(subset=['code'], keep='first', inplace=True)
    result3.to_csv('test2.csv', encoding='gbk')
    for i in range(0, 300):
        match = True
        if result1['roe'].iloc[i] < 10:
            match = False
            break
        if result2['roe'].iloc[i] < 10:
            match = False
            break
        if result3['roe'].iloc[i] < 10:
            match = False
            break
        if match == True:
            first_choose.append(result1['code'].iloc[i])
        print(first_choose)

# first_round(hs300)

def second_round(list):
    temp1 = ts.get_profit_data(2019, 1)
    #temp1.to_csv('2019_1.csv', encoding='gbk')
    temp2 = ts.get_profit_data(2019, 2)
    #temp2.to_csv('2019_2.csv', encoding='gbk')
    # temp1 = pd.read_csv('2019_1.csv')
    # temp2 = pd.read_csv('2019_2.csv')
    temp3 = ts.get_profit_data(2019, 3)
    #temp3.to_csv('2019_3.csv', encoding='gbk')
    # temp3 = pd.read_csv('2019_3.csv')
    result1 = pd.merge(hs300, temp1, on='code')
    result1.drop_duplicates(subset=['code'], keep='first', inplace=True)
    result1.to_csv('2019_1.csv', encoding='gbk')
    result2 = pd.merge(hs300, temp2, on='code')
    result2.drop_duplicates(subset=['code'], keep='first', inplace=True)
    result2.to_csv('2019_2.csv', encoding='gbk')
    result3 = pd.merge(hs300, temp3, on='code')
    result3.drop_duplicates(subset=['code'], keep='first', inplace=True)
    result3.to_csv('2019_3.csv', encoding='gbk')

    temp1['code'] = temp1['code'].astype('int')
    temp2['code'] = temp1['code'].astype('int')
    temp3['code'] = temp3['code'].astype('int')
    #temp3['code'] = temp1['code'].astype('int')
    # for i in list:
    #     # print(i)
    #     a = temp1.loc[temp1['code'] == i]
    #     b = temp2.loc[temp2['code'] == i]
    #     c = float(b['roe']) - float(a['roe'])
    #     if c > float(a['roe']):
    #         print(c)


# second_round(first_choose)
# print(first_choose)

# se = []
# for i in second_choose:
#     if i in first_choose:
#         se.append(i)
# print(se)
def sortAndChoose(dict, n): # dict是预测的股票收益率，n是股票个数
    stocks = []
    result = []
    p = sorted([(k, v) for k, v in dict.items()], reverse=True)
    # print(p)
    s = set()
    for i in p:
        s.add(i[1])
    for i in sorted(s, reverse=True)[:n]:
        for j in p:
            if j[1] == i:
                result.append(j)
    for r in result:
        stocks.append(r[0])
    print(stocks)
    #f.write('这天股票的排序选择为' + str(stocks)+'\n')
    return stocks

dic = {
    600066: 1.28,
    600886: 1.57,
    600900: 1.7,
    601997: 0.38,
    603259: 0.45,
    603833: 0.4,
    603986: 0.67,
    69: 2.19,
    2027: 0.36,
    2311: 0.83,
    2415: 0.68,
    2475: 1.69,
    300015: 0.84,
    300033: 0.25,
    300144: 0.17,
    300498: 6.95
}

choose_stock = ['300498', '000069', '600900', '002475', '600886', '600066', '300015', '002311', '002415', '603986']
# sortAndChoose(dic, 10)
# print(choose_stock)
start = 0
end = 0
for i in choose_stock:
    temp = ts.get_hist_data(i, start='2019-10-28', end='2019-11-08').sort_index(ascending=True)
    print(temp.head())
    start += temp['close'].iloc[0]
    end += temp['close'].iloc[-1]
print(start)
print(end)
hs300 = ts.get_hist_data(code='hs300', start='2019-10-28', end='2019-11-08').sort_index(ascending=True)
print(hs300.head())
print(hs300['close'].iloc[-1])
print(hs300['close'].iloc[0])

# t1 = ts.get_profit_data(2016, 1)
# t1.to_csv('2016_1.csv', encoding='gbk')
# t2 = ts.get_profit_data(2016, 2)
# t2.to_csv('2016_2.csv', encoding='gbk')
# t3 = ts.get_profit_data(2016, 3)
# t3.to_csv('2016_3.csv', encoding='gbk')
#
# t4 = ts.get_profit_data(2017, 1)
# t4.to_csv('2017_1.csv', encoding='gbk')
# t5 = ts.get_profit_data(2017, 2)
# t5.to_csv('2017_2.csv', encoding='gbk')
# t6 = ts.get_profit_data(2017, 3)
# t6.to_csv('2017_3.csv', encoding='gbk')
#
# t7 = ts.get_profit_data(2018, 1)
# t7.to_csv('2018_1.csv', encoding='gbk')
# t8 = ts.get_profit_data(2018, 2)
# t8.to_csv('2018_2.csv', encoding='gbk')
# t9 = ts.get_profit_data(2018, 3)
# t9.to_csv('2018_3.csv', encoding='gbk')
#
# t10 = ts.get_profit_data(2019, 1)
# t10.to_csv('2019_1.csv', encoding='gbk')
# t11 = ts.get_profit_data(2019, 2)
# t11.to_csv('2019_2.csv', encoding='gbk')
# t12 = ts.get_profit_data(2019, 3)
# t12.to_csv('2019_3.csv', encoding='gbk')