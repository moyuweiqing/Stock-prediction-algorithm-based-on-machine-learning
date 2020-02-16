# 使用沪深300成分股作为股票池进行测试
import tushare as ts
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import xlrd

# prophet数据集
l1 = ['601888', '601088', '601766', '600340', '600048', '601668', '601988', '601398', '601288', '601328']
l2 = ['601888', '600340', '601088', '601766', '600690', '601111', '600029', '601398', '601988', '601328']
l3 = ['601888', '600340', '600690', '601088', '601111', '601766', '600029', '601989', '601398', '601328']
l4 = ['601888', '601066', '601766', '601398', '600340', '601138', '601818', '601328', '601988', '601989']
l5 = ['601088', '600276', '601888', '601766', '601066', '601138', '601328', '600340', '601398', '601988']
l6 = ['601066', '601319', '600276', '601328', '601138', '601668', '601766', '600340', '601088', '601818']
l7 = ['601066', '600276', '601688', '601888', '600050', '601088', '601328', '601766', '601628', '600690']
l8 = ['601066', '600276', '601688', '600703', '601319', '601088', '600030', '601328', '601888', '600837']
l9 = ['601989', '601111', '600276', '601688', '600340', '601319', '601766', '600029', '601088', '600309']
l10 = ['601066', '601319', '603993', '601688', '601989', '601138', '600030', '601211', '600031', '601766']
l11 = ['601066', '600030', '601688', '601111', '601989', '600050', '601319', '600837', '601628', '600703']
l12 = ['600703', '601066', '601688', '601111', '600030', '600837', '601989', '601628', '600029', '600050']
l13 = ['600703', '601111', '600050', '601989', '600837', '601628', '600030', '600029', '601211', '600196']
l14 = ['601111', '600703', '600196', '600837', '600030', '601211', '600029', '600309', '601688', '601989']
l15 = ['600196', '601336', '601989', '600690', '600519', '601888', '600887', '600703', '603259', '600029']
l16 = ['600196', '601888', '600690', '600519', '600050', '600029', '601989', '600887', '600104', '601668']
l17 = ['600196', '601888', '600690', '600050', '600887', '601989', '601229', '600519', '600585', '600104']
l18 = ['600196', '600050', '601229', '600690', '601888', '600519', '600887', '601989', '601988', '600104']
l19 = ['603993', '600703', '601318', '601628', '600030', '601336', '601688', '600837', '601888', '600309']
l20 = ['601229', '601888', '600050', '600104', '601088', '600690', '601328', '600519', '600309', '600585']
l21 = ['601888', '600309', '600703', '600690', '600519', '600585', '600887', '600050', '600104', '601336']
l22 = ['601888', '600519', '603993', '600585', '600690', '600887', '601088', '601328', '600309', '600050']
l23 = ['600585', '601888', '600340', '600887', '601088', '600519', '600019', '600050', '601398', '601328']
l24 = ['600887', '600340', '601888', '600050', '600585', '600019', '601336', '601111', '601088', '600690']
l25 = ['600340', '600887', '601888', '600585', '601111', '600019', '600690', '601336', '601088', '601328']
l26 = ['600887', '600340', '601888', '601111', '600690', '601398', '600050', '601988', '601288', '601939']
l27 = ['600340', '601111', '600887', '601888', '601336', '601688', '600050', '600036', '600029', '601398']
l28 = ['601888', '600340', '600887', '601111', '601088', '601398', '601988', '600048', '601939', '600690']
l29 = ['601088', '600340', '601888', '600048', '601601', '600519', '600029', '603993', '600028', '600036']
l30 = ['601888', '600887', '600340', '600690', '601111', '600036', '601088', '600029', '601989', '601398']

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
yield_list = []
preds = pd.DataFrame(np.random.randn(300, 20))
count = 0

# 去除停牌股票
def removeSuspendedStock():
    # 去除测试日期中有停牌的股票
    # 209 290
    for i in range(0, 300):
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-09-02', end='2019-09-30')
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
    true_day = datelist[day]
    total = 0
    f.write('计算第'+str(day)+'天的股价\n')
    for i in range(0, len(stocklist)):
        temp = ts.get_hist_data(stocklist[i], start='2019-03-04', end='2019-09-30').sort_index(ascending=True)
        price = temp['close'].loc[temp.index == true_day]
        price = price.iloc[0]
        # print(price)
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
        temp = ts.get_hist_data(stocklist[i], start='2019-03-04', end='2019-09-30').sort_index(ascending=True)
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
def countYield(cash, stocks):
    y = 0.0
    y = (cash + stocks)/10000
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
            temp = ts.get_hist_data(holdStocks[i], start='2019-03-04', end='2019-09-30').sort_index(ascending=True)
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
            temp = ts.get_hist_data(predictStocks[i], start='2019-03-04', end='2019-09-30').sort_index(ascending=True)
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
yield_list.append(countYield(cash, total_true_asset))
for i in range(1, 30):
    # getDayStock2(i)
    # choosed_stocks = sortAndChoose(day_yield, 10)
    choosed_stocks = r0(i+1)
    my_stocks, total_asset, cash = stockExchange(my_stocks, choosed_stocks, i, total_asset, cash)
    total_true_asset = countTotalStockAsset(my_stocks, 100, i)
    print(total_true_asset)
    # total_win_number = countOneDay(my_stocks, i, total_win_number)
    yield_list.append(countYield(cash, total_true_asset))
    f2.write('第'+str(i)+'天的结果'+'\n')
    f2.write('持有股票为'+str(my_stocks)+'\n')
    f2.write('总资产为'+str(total_asset)+'\n')
    f2.write('目前的胜数为'+str(total_win_number)+'\n')
    f2.write('股票总资产为'+str(total_true_asset)+'\n')
    f2.write('胜率为'+str(total_win_number/(10 * (i + 1)))+'\n\n')
    f.write('\n\n')
print(yield_list)
f.close()
f2.close()