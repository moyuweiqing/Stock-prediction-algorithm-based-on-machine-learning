# 使用沪深300成分股作为股票池进行测试
import tushare as ts
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import xlrd
import prophetapi

# 移动平均的数据集
l1 = [181, 210, 174, 7, 85, 257, 261, 248, 224, 194]
l2 = [3, 38, 124, 232, 56, 97, 135, 196, 79, 183]
l3 = [291, 298, 175, 204, 242, 247, 246, 262, 270, 278]
l4 = [291, 204, 175, 247, 246, 298, 223, 49, 242, 265]
l5 = [175, 204, 247, 265, 49, 176, 270, 291, 298, 252]
l6 = [247, 265, 270, 175, 49, 298, 291, 62, 243, 204]
l7 = [247, 175, 128, 291, 176, 265, 270, 101, 258, 298]
l8 = [247, 175, 258, 291, 14, 176, 105, 128, 101, 221]
l9 = [247, 258, 175, 182, 176, 291, 207, 14, 243, 101]
l10 = [247, 258, 175, 176, 182, 63, 243, 228, 66, 14]
l11 = [247, 182, 175, 258, 176, 246, 229, 279, 262, 228]
l12 = [182, 175, 176, 247, 229, 262, 246, 49, 92, 291]
l13 = [182, 246, 229, 49, 176, 175, 262, 277, 258, 92]
l14 = [246, 182, 175, 176, 262, 92, 113, 229, 74, 291]
l15 = [182, 246, 175, 176, 92, 291, 229, 113, 277, 68]
l16 = [182, 246, 175, 176, 92, 113, 298, 208, 245, 262]
l17 = [182, 92, 277, 208, 176, 246, 175, 180, 229, 105]
l18 = [182, 277, 298, 218, 176, 180, 246, 175, 208, 245]
l19 = [182, 277, 246, 175, 218, 176, 285, 60, 68, 279]
l20 = [182, 277, 176, 175, 152, 279, 285, 108, 218, 133]

# prophet数据集
m1 = [288, 50, 247, 295, 258, 92, 283, 173, 82, 270]
m2 = [90, 108, 280, 279, 225, 115, 220, 273, 258, 223]
m3 = [85, 280, 194, 203, 278, 144, 126, 113, 253, 175]
m4 = [175, 105, 294, 69, 2, 96, 74, 273, 184, 66]
m5 = [282, 223, 247, 176, 276, 289, 202, 42, 201, 2]
m6 = [288, 50, 295, 247, 283, 258, 92, 173, 82, 179]
m7 = [273, 280, 90, 220, 225, 279, 252, 299, 262, 223]
m8 = [85, 280, 253, 113, 203, 291, 86, 175, 144, 278]
m9 = [175, 273, 105, 74, 66, 294, 2, 227, 254, 246]
m10 = [282, 176, 223, 247, 276, 42, 201, 289, 202, 2]
m11 = [90, 273, 220, 280, 279, 225, 247, 258, 108, 252]
m12 = [85, 113, 280, 203, 253, 144, 291, 86, 247, 182]
m13 = [105, 175, 74, 273, 152, 66, 265, 87, 227, 294]
m14 = [223, 176, 282, 247, 276, 201, 42, 289, 2, 202]
m15 = [288, 50, 247, 295, 92, 258, 283, 82, 173, 90]
m16 = [90, 108, 280, 279, 273, 220, 225, 252, 92, 247]
m17 = [85, 280, 203, 253, 49, 65, 113, 144, 86, 126]
m18 = [105, 74, 152, 175, 273, 182, 87, 298, 265, 291]
m19 = [223, 282, 247, 176, 276, 289, 42, 201, 182, 203]
m20 = [288, 50, 247, 295, 283, 92, 258, 173, 49, 270]

#LSTM
n1 = [201,52,65,181,248,257,137,7,115,54]
n2 = [133,277,176,175,152,161,235,87,53,242]
n3 = [161,133,235,87,53,152,277,71,175,285]
n4 = [161,35,235,285,87,152,133,53,49,246]
n5 = [285,35,161,133,235,49,265,22,298,297]
n6 = [285,35,298,22,49,235,108,265,161,133]
n7 = [285,298,108,35,22,241,49,133,210,235]
n8 = [285,108,133,241,210,22,35,82,298,235]
n9 = [285,108,133,241,210,82,235,283,49,35]
n10 = [108,285,82,133,241,49,210,283,235,22]
n11 = [108,82,133,235,285,283,241,49,158,194]
n12 = [108,82,235,49,194,133,241,158,65,285]
n13 = [82,108,235,49,65,298,194,241,158,100]
n14 = [82,65,235,108,298,49,228,241,246,158]
n15 = [82,65,246,228,298,235,195,108,49,188]
n16 = [82,246,195,228,298,65,235,108,278,262]
n17 = [82,246,195,228,298,175,278,1,65,57]
n18 = [246,82,228,195,260,1,175,57,278,241]
n19 = [246,260,1,175,228,195,57,82,294,176]
n20 = [246,294,175,1,195,260,177,176,57,228]

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
    total = 0
    f.write('计算第'+str(day)+'天的股价\n')
    for i in range(0, len(stocklist)):
        temp = ts.get_hist_data(hs300['code'].loc[stocklist[i]], start='2019-09-02', end='2019-09-30').sort_index(ascending=True)
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
        temp = ts.get_hist_data(hs300['code'].loc[stocklist[i]], start='2019-09-02', end='2019-09-30').sort_index(ascending=True)
        # temp.to_csv('test.csv')
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
        temp = ts.get_hist_data(hs300['code'].loc[i], start='2019-09-02', end='2019-09-30').sort_index(ascending=True)
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
    # 先卖出
    for i in range(0, len(holdStocks)):
        if holdStocks[i] in predictStocks:
            exchange.append(holdStocks[i])
            continue
        else:
            temp = ts.get_hist_data(hs300['code'].loc[holdStocks[i]], start='2019-09-02', end='2019-09-30').sort_index(ascending=True)
            total_asset += (temp['open'].iloc[day] - stocks_buy_price[holdStocks[i]]) * 100
            f.write('卖出股票' + str(holdStocks[i]) + ', 股数为100, 卖出价为'+ str(temp['open'].iloc[day])+',')
            cash = countCash(cash, 1, temp['open'].iloc[day])
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
            temp = ts.get_hist_data(hs300['code'].loc[predictStocks[i]], start='2019-09-02', end='2019-09-30').sort_index(ascending=True)
            choose_stocks_buffer.append(temp['open'].iloc[day])
            #print(choose_stocks_buffer)
            # print(choose_stocks_buffer)
            # choose_stocks_number_buffer.append(100)
            judge = overCapital(choose_stocks_buffer, choose_stocks_number_buffer, total_asset)
            if judge == False:
                # print(temp['open'].iloc[0])
                choose_stocks_buffer.pop()
                continue
            else:
                cash = countCash(cash, 0, temp['open'].iloc[day])
                exchange.append(predictStocks[i])
                stocks_buy_price[predictStocks[i]] = temp['open'].iloc[day]
    f.write('股票的买入价为' + str(stocks_buy_price)+'\n')
    f.write('这一天我的股票集为'+ str(exchange)+'\n')
    return exchange, total_asset, cash

#moving_average
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
        return l20

#prophet
def r1(i):
    if i == 1:
        return m1
    elif i == 2:
        return m2
    elif i == 3:
        return m3
    elif i == 4:
        return m4
    elif i == 5:
        return m5
    elif i == 6:
        return m6
    elif i == 7:
        return m7
    elif i == 8:
        return m8
    elif i == 9:
        return m9
    elif i == 10:
        return m10
    elif i == 11:
        return m11
    elif i == 12:
        return m12
    elif i == 13:
        return m13
    elif i == 14:
        return m14
    elif i == 15:
        return m15
    elif i == 16:
        return m16
    elif i == 17:
        return m17
    elif i == 18:
        return m18
    elif i == 19:
        return m19
    elif i == 20:
        return m20

#LSTM
def r2(i):
    if i == 1:
        return n1
    elif i == 2:
        return n2
    elif i == 3:
        return n3
    elif i == 4:
        return n4
    elif i == 5:
        return n5
    elif i == 6:
        return n6
    elif i == 7:
        return n7
    elif i == 8:
        return n8
    elif i == 9:
        return n9
    elif i == 10:
        return n10
    elif i == 11:
        return n11
    elif i == 12:
        return n12
    elif i == 13:
        return n13
    elif i == 14:
        return n14
    elif i == 15:
        return n15
    elif i == 16:
        return n16
    elif i == 17:
        return n17
    elif i == 18:
        return n18
    elif i == 19:
        return n19
    elif i == 20:
        return n20

# removeSuspendedStock()
# getDayStock2(0)
# choosed_stocks = sortAndChoose(day_yield, 10)
choosed_stocks = l1
# print(choosed_stocks)
cash = firstDayHold(choosed_stocks, cash)
total_true_asset = countTotalStockAsset(my_stocks, 100, 0)
total_win_number = countOneDay(my_stocks, 1, total_win_number)
f.write('\n\n')
f2.write('第0天的结果'+'\n')
f2.write('持有股票为'+str(my_stocks)+'\n')
f2.write('总资产为'+str(10000)+'\n')
f2.write('目前的胜数为'+str(total_win_number)+'\n')
f2.write('股票总资产为'+str(total_true_asset)+'\n')
f2.write('胜率为'+str(total_win_number/10)+'\n\n')
print(total_true_asset)
yield_list.append(countYield(cash, total_true_asset))
for i in range(1, 20):
    # getDayStock2(i)
    # choosed_stocks = sortAndChoose(day_yield, 10)
    choosed_stocks = r0(i+1)
    my_stocks, total_asset, cash = stockExchange(my_stocks, choosed_stocks, i, total_asset, cash)
    total_true_asset = countTotalStockAsset(my_stocks, 100, i)
    total_win_number = countOneDay(my_stocks, i, total_win_number)
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