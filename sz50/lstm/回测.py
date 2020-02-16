import tushare as ts
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import xlrd

l1 = ['601628', '601166', '601336', '601989', '600036', '600196', '600519', '600837', '600009', '601818']
l2 =  ['600837', '600703', '600036', '601166', '600009', '600547', '600585', '601989', '601398', '600519']
l3 =  ['601012', '600036', '601166', '601688', '600519', '600309', '600837', '600585', '600031', '600340']
l4 =  ['601336', '600036', '600030', '600009', '601688', '600837', '600547', '600585', '600340', '600519']
l5 =  ['601989', '600036', '600519', '600837', '600009', '600030', '601888', '601688', '600309', '601012']
l6 =  ['601989', '600837', '600585', '600036', '601336', '601688', '601012', '601166', '601888', '600030']
l7 =  ['600036', '601989', '600585', '600519', '601166', '600837', '600196', '600340', '601888', '600009']
l8 =  ['601989', '600009', '600036', '601601', '601336', '601888', '601166', '600585', '600519', '601318']
l9 =  ['600837', '600036', '600009', '600703', '600519', '601688', '601888', '600030', '601166', '600547']
l10 = ['600009', '601166', '600519', '600036', '600276', '600837', '601318', '600196', '601888', '600585']
l11 =['600009', '601012', '600036', '600031', '600547', '600519', '601888', '601688', '600585', '601166']
l12 =['601012', '600036', '600009', '600519', '600340', '600585', '601166', '601888', '601398', '600547']
l13 =['600036', '600585', '601166', '601688', '601012', '600519', '601398', '600837', '600009', '601939']
l14 =['600036', '600547', '601012', '600585', '600009', '600519', '601601', '601888', '600837', '601989']
l15 =['600547', '600036', '600837', '600009', '601166', '601398', '601939', '600048', '600000', '600585']
l16 =['600036', '600547', '600585', '600009', '600519', '601989', '601888', '601166', '600837', '600340']
l17 =['601688', '600837', '600036', '600547', '600030', '600009', '600519', '601888', '601012', '601318']
l18 =['600009', '601888', '600585', '600036', '600837', '600340', '601989', '600519', '601012', '600547']
l19 =['601989', '600585', '600036', '600009', '600547', '600519', '601888', '600196', '601318', '601166']
l20 =['600009', '600036', '601888', '600547', '601601', '601012', '600519', '601628', '600837', '601166']
l21 =['600547', '600036', '601012', '600009', '600837', '601688', '601601', '601166', '600048', '601888']
l22 =['601012', '600036', '600009', '601888', '601166', '600585', '600519', '601989', '600547', '601688']
l23 =['601888', '600036', '600009', '600547', '600519', '601012', '601166', '601989', '600837', '601336']
l24 =['600547', '600036', '600519', '600009', '601888', '601989', '601166', '601012', '600585', '600276']
l25 =['600547', '600009', '600519', '601888', '600036', '601989', '600196', '601318', '600585', '600837']
l26 =['600519', '600009', '601888', '601012', '600036', '600196', '600276', '601601', '600837', '600585']
l27 =['600547', '600519', '601888', '601012', '601989', '600009', '600036', '600276', '600837', '600585']
l28 =['600837', '600585', '600036', '600009', '600519', '601888', '601989', '600030', '601688', '601166']
l29 =['600837', '600703', '600036', '600585', '600009', '601318', '601888', '601989', '600048', '600519']
l30 =['600703', '600519', '601888', '600036', '600585', '600009', '601012', '600547', '601989', '600837']

datelist = ['2019-03-04', '2019-03-11', '2019-03-18', '2019-03-25',
            '2019-04-01', '2019-04-08', '2019-04-15', '2019-04-22', '2019-04-29',
            '2019-05-06', '2019-05-13', '2019-05-20', '2019-05-27',
            '2019-06-03', '2019-06-10', '2019-06-17', '2019-06-24',
            '2019-07-01', '2019-07-08', '2019-07-15', '2019-07-22', '2019-07-29',
            '2019-08-05', '2019-08-12', '2019-08-19', '2019-08-26',
            '2019-09-02', '2019-09-09', '2019-09-16', '2019-09-23']

from pylab import * #改变plot字体，适应中文
mpl.rcParams['font.sans-serif'] = ['SimHei']


f = open('trade_data.txt', 'w')
f2 = open('strategy_data.txt', 'w')

# 获取沪深300成分股
total_asset = 10000
hs300 = ts.get_hs300s()
suspend = [] # 停牌股票
day_yield = {} # 沪深300成分股一天的预测收益率
choosed_stocks = [] # 机器学习选择的股票排序
choose_stocks_buffer = [] # 股票价格缓冲池
choose_stocks_number_buffer = [] # 每支股票持有数量缓冲池
my_stocks = [] # 持有股票池
total_win_number = 0 # 总胜场数
total_win_rate = 0.0 # 总胜率
total_true_asset = 0 # 实际市场总价
stocks_buy_price = {} # 股票维持的天数
cash = 10000 # 剩余现金
yield_list = pd.DataFrame(columns=['yield'])
asset = pd.DataFrame(columns=['number'])
preds = pd.DataFrame(np.random.randn(300, 20))
count = 0

# 去除停牌股票
def removeSuspendedStock():
    # 去除测试日期中有停牌的股票
    # 209 290
    for i in range(0, 300):
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-03-04', end='2019-09-29')
        row = temp.iloc[:,0].size
        if(row != 20):
            suspend.append(i)
            continue

#print(suspend)

# 获取一天股票预测值，使用预言家算法
def getDayStock(day): # 这里的day是实际天数-1天，与表格相适应
    for i in range(0, 12):
        if i in suspend:
            continue
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-01-02', end='2019-09-30')
        temp = temp.sort_index(ascending=True)
        # print(temp.head())
        new_data = pd.DataFrame(index=range(0, len(temp)), columns=['Date', 'Close'])
        for j in range(0, len(temp)):
            new_data['Date'][j] = temp.index[j]
            new_data['Close'][j] = temp['close'][j]

        new_data['Date'] = pd.to_datetime(new_data.Date, format='%Y-%m-%d')
        new_data.index = new_data['Date']

        # 准备数据
        new_data.rename(columns={'Close': 'y', 'Date': 'ds'}, inplace=True)
        row = temp.iloc[:, 0].size
        # print(temp.head())
        # temp.to_csv('test.csv')
        training_number = row - 20 + day
        training_set = new_data[: training_number]
        validation_set = new_data[training_number:training_number + 1]
        prediction = prophetapi.make_prediction(training_set, validation_set)
        day_yield[i] = prediction
    f.write('预测第'+str(day)+'天的股票走势情况\n')

# 移动平均法
def getDayStock2(day):
    global count
    global preds
    for i in range(0, 300):
        if i in suspend:
            continue
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-01-02', end='2019-09-30').sort_index(ascending=True)
        new_data = pd.DataFrame(index=range(0, len(temp)), columns=['Date', 'Close'])
        for j in range(0, len(temp)):
            new_data['Date'][j] = temp.index[j]
            new_data['Close'][j] = temp['close'][j]
        # predition = moving_averageapi.make_prediction(new_data, day)
        a = 0
        if day == 0:
            a = new_data['Close'][133 + day: 163].sum() + preds[0][i]
        else:
            for j in range(0, day):
                a = new_data['Close'][133 + day: 163].sum() + preds[j][i]
        b = a / 30
        preds[day][i] = b
        #print(b)
        #print(preds[day])
        if day == 0:
            c = b / new_data['Close'][162]
        else:
            c = b / preds[day - 1][i]
        day_yield[i] = c
    count += 1
    print(day_yield)

# 将预测之后的股票进行排序和选择
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
    f.write('这天股票的排序选择为' + str(stocks)+'\n')
    return stocks

# 查看股票是否已经高于总资产
def overCapital(stocklist, stocknumber, totalCapital):
    total = 0
    for i in range(0, len(stocklist)):
        total += stocklist[i] * stocknumber[i]
        if totalCapital < total:
            f.write('不能买入价格为'+str(stocklist[i])+'的股票， \n')
            # f.write('over price is ' + str(stocklist[i]) + '\n')
            return False
    f.write('买了价格为'+str(stocklist[i])+'的股票后，股票总资产为 ' + str(total) + '\n')
    return True

# 计算股票总资产
def countTotalStockAsset(stocklist, stocknumber, day):
    total = 0
    f.write('计算第'+str(day)+'天的股价\n')
    for i in range(0, len(stocklist)):
        temp = ts.get_hist_data(stocklist[i], start='2019-03-04', end='2019-09-29').sort_index(ascending=True)
        price = temp['close'].iloc[day]
        total += price * stocknumber
        f.write('第'+ str(i)+'支股票代码是'+str(stocklist[i])+',  ')
        f.write('买入价为'+str(stocks_buy_price[stocklist[i]])+', ')
        f.write('当前价格为'+str(price)+',  ')
        f.write('资产为'+str(price * stocknumber)+',  ')
        f.write('目前股票市场的总资产为'+str(total)+'\n')
    return total

# 计算剩余现金
def countCash(cash, state, number):
    if state == 0: # 买入
        cash -= number * 100
        f.write('现金剩余' + str(cash))
    else: # 卖出
        cash +=number * 100
        f.write('现金剩余' + str(cash))
    return cash

# 第一天的股票买入
def firstDayHold(stocklist, cash):
    # f.write('我的股票列表为：'+str(stocklist))
    for i in range(0, len(stocklist)):
        temp = ts.get_hist_data(stocklist[i], start='2019-03-04', end='2019-09-29').sort_index(ascending=True)
        # temp.to_csv('test.csv')
        # print(temp.iloc[0])
        f.write('买入价为'+str(temp['open'].iloc[0]))
        choose_stocks_buffer.append(temp['open'].iloc[0])
        choose_stocks_number_buffer.append(100)
        # print(choose_stocks_buffer)
        # print(choose_stocks_buffer[i] * choose_stocks_number_buffer[i])
        judge = overCapital(choose_stocks_buffer, choose_stocks_number_buffer, total_asset)
        if judge == False:
            #print(temp['open'].iloc[0])
            choose_stocks_buffer.pop()
            #choose_stocks_number_buffer.remove()
            continue
        else:
            cash = countCash(cash, 0, temp['open'].iloc[0])
            my_stocks.append(stocklist[i])
            stocks_buy_price[stocklist[i]] = temp['open'].iloc[0]
    f.write('股票的买入价集合为' + str(stocks_buy_price)+'\n')
    f.write('第一天买入的股票为' + str(my_stocks)+'\n')
    return cash
    # print(my_stocks)
        # temp.to_csv('test.csv')

# 计算一天的股票情况
def countOneDay(stocklist, day, total_win_number): #stocklist是选择的股票集，day是第几天
    win_number = 0
    win_rate = 0.0
    for i in range(0, len(stocklist)):
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-03-03', end='2019-09-29').sort_index(ascending=True)
        # 计算一天胜场和胜率
        if temp['close'].iloc[day - 1] > temp['open'].iloc[day - 1]:
            #print(temp['close'].iloc[day - 1])
            #print(temp['open'].iloc[day - 1])
            win_number += 1
    #print(win_number)
    total_win_number += win_number
    win_rate = win_number/len(stocklist)
    #print(win_rate)
    return total_win_number

# 计算收益率
def countYield(cash, stocks, day):
    global asset
    y = 0.0
    y = (cash + stocks)/10000
    asset.loc[day] = cash + stocks
    return y

# 股票转换
def stockExchange(holdStocks, predictStocks, day, total_asset, cash): #holdStocks是持有的股票，predicStocks是预测的股票，day是第几天
    exchange = []
    true_day = datelist[day]
    # 先卖出
    for i in range(0, len(holdStocks)):
        if holdStocks[i] in predictStocks:
            exchange.append(holdStocks[i])
            continue
        else:
            temp = ts.get_hist_data(holdStocks[i], start='2019-03-04', end='2019-09-29').sort_index(ascending=True)
            after = temp['open'].loc[temp.index == true_day]
            after = after.iloc[0]
            total_asset += (after - stocks_buy_price[holdStocks[i]]) * 100
            f.write('卖出股票' + str(holdStocks[i]) + ', 股数为100, 卖出价为'+ str(after)+',')
            cash = countCash(cash, 1, after)
            f.write(' 此时我的总资产为' + str(total_asset) + '\n')
            # print('还不在的是:'+str(holdStocks[i])+'   ')
            # print(choose_stocks_buffer)
            # print(stocks_day[holdStocks[i]])
            choose_stocks_buffer.remove(stocks_buy_price[holdStocks[i]])
            stocks_buy_price.pop(holdStocks[i])
            # f.write('移除了股票'+str(holdStocks[i])+'\n')
            # print(temp['open'].iloc[stocks_day[holdStocks[i]]])
    # 再买入
    for i in range(0, len(predictStocks)):
        if predictStocks[i] in holdStocks:
            continue
        else:
            temp = ts.get_hist_data(predictStocks[i], start='2019-03-04', end='2019-09-29').sort_index(ascending=True)
            after = temp['open'].loc[temp.index == true_day]
            after = after.iloc[0]
            choose_stocks_buffer.append(after)
            #print(choose_stocks_buffer)
            # print(choose_stocks_buffer)
            # choose_stocks_number_buffer.append(100)
            judge = overCapital(choose_stocks_buffer, choose_stocks_number_buffer, total_asset)
            if judge == False:
                # print(temp['open'].iloc[0])
                choose_stocks_buffer.pop()
                continue
            else:
                cash = countCash(cash, 0, after)
                exchange.append(predictStocks[i])
                stocks_buy_price[predictStocks[i]] = after
    f.write('股票的买入价为' + str(stocks_buy_price)+'\n')
    f.write('这一天我的股票集为'+ str(exchange)+'\n')
    return exchange, total_asset, cash

#prophet
def r0(i):
    if i == 1:
        return l1
    elif i == 2:
        return l2
    elif i == 3:
        return l3
    elif i == 4:
        return l4
    elif i == 5:
        return l5
    elif i == 6:
        return l6
    elif i == 7:
        return l7
    elif i == 8:
        return l8
    elif i == 9:
        return l9
    elif i == 10:
        return l10
    elif i == 11:
        return l11
    elif i == 12:
        return l12
    elif i == 13:
        return l13
    elif i == 14:
        return l14
    elif i == 15:
        return l15
    elif i == 16:
        return l16
    elif i == 17:
        return l17
    elif i == 18:
        return l18
    elif i == 19:
        return l19
    elif i == 20:
        return l21
    elif i == 21:
        return l21
    elif i == 22:
        return l22
    elif i == 23:
        return l23
    elif i == 24:
        return l24
    elif i == 25:
        return l25
    elif i == 26:
        return l26
    elif i == 27:
        return l27
    elif i == 28:
        return l28
    elif i == 29:
        return l29
    elif i == 30:
        return l30

# removeSuspendedStock()
# getDayStock2(0)
# choosed_stocks = sortAndChoose(day_yield, 10)
choosed_stocks = l1
# print(choosed_stocks)
cash = firstDayHold(choosed_stocks, cash)
total_true_asset = countTotalStockAsset(my_stocks, 100, 0)
# total_win_number = countOneDay(my_stocks, 1, total_win_number)
f.write('\n\n')
f2.write('第0天的结果'+'\n')
f2.write('持有股票为'+str(my_stocks)+'\n')
f2.write('总资产为'+str(10000)+'\n')
# f2.write('目前的胜数为'+str(total_win_number)+'\n')
f2.write('股票总资产为'+str(total_true_asset)+'\n')
# f2.write('胜率为'+str(total_win_number/10)+'\n\n')
print(total_true_asset)
yield_a = countYield(cash, total_true_asset, 0)
yield_list.loc[0] = yield_a
sz50 = ts.get_hist_data(code='sz50', start='2019-03-04', end='2019-09-29').sort_index(ascending=True)
sz50['date'] = sz50.index

j = 1;
for i in range(1, 144):
    if sz50['date'].iloc[i] in datelist:
        choosed_stocks = r0(j+1)
        my_stocks, total_asset, cash = stockExchange(my_stocks, choosed_stocks, j, total_asset, cash)
        j += 1
    total_true_asset = countTotalStockAsset(my_stocks, 100, i)
    print('第'+str(i)+'天')
    print(total_true_asset)
    # total_win_number = countOneDay(my_stocks, i, total_win_number)
    yield_a = countYield(cash, total_true_asset, i)
    yield_list.loc[i] = yield_a
    f2.write('第'+str(i)+'天的结果'+'\n')
    f2.write('持有股票为'+str(my_stocks)+'\n')
    f2.write('总资产为'+str(total_asset)+'\n')
    f2.write('目前的胜数为'+str(total_win_number)+'\n')
    f2.write('股票总资产为'+str(total_true_asset)+'\n')
    f2.write('胜率为'+str(total_win_number/(10 * (i + 1)))+'\n\n')
    f.write('\n\n')
print(yield_list)
yield_list.to_csv('yield_list.csv')
asset.to_csv('asset.csv')
f.close()
f2.close()