# python 3.6

# pip install pandas
# pip install lxml

# 根据提示语 安装缺少的模块
# pip install requests
# pip install bs4
# pip install tushare

# 交易部分
# pip install tesseract
# 搜tesseract 单独下载,并且需要放到path目录
# TESSDATA_PREFIX 标记到环境变量中 训练数据位置 C:\Program Files (x86)\Tesseract-OCR\tessdata

import quant.haigui as quant_strategy
import tushare
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime
import time

import math
import os
import sys

import json
import file_helper


class QuantMatplot(object):
    """docstring for QuantMatplot"""

    def __init__(self):
        super(QuantMatplot, self).__init__()


class QuantOrder(object):
    """docstring for QuantOrder"""

    def __init__(self):
        super(QuantOrder, self).__init__()


class QuantAccountData(object):
    def __init__(self):
        """ 
                构造函数 
        """


class QuantUserData(object):
    def __init__(self):
        """ 
                构造函数 
        """


class QuantStockContext(object):
    def __init__(self, start, end, frequency):
        """ 
            构造函数 
        """
        # 开始日期 format：YYYY-MM-DD 为空时取上市首日
        self.start_time = start

        # 结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
        self.end_time = end

        # 数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
        self.frequency = frequency

        # 自定义数据
        self.user_data = QuantUserData()
        print("self.user_data =", id(self.user_data))

        self.account = QuantAccountData()
        self.order = QuantOrder()
        self.account_initial = QuantAccountData()
        self.matplot = QuantMatplot()
        self.matplot.date = []
        self.matplot.my = []
        self.matplot.standard = []


# 收盘价购买,没有滑点
STOCK_FLOAT = 0.0


def stock_buy(name, price, cash):
    count = int(cash/price//100*100)
    if(count >= 100):
        # 直接认为买入成功 价格+误差
        buy_money = (price+STOCK_FLOAT)*count
        fee = context.account.commission*buy_money  # 佣金
        if(fee < context.account.commission_base):
            fee = context.account.commission_base

        context.account.money -= buy_money  # 减去买入金额
        context.account.money -= fee  # 减去费用
        context.account.stock += count
        print("buy 买入["+name+"]成功 剩余现金 =", context.account.money, ",持有股票 =",
              context.account.stock, "成交额 =", buy_money, "总费用 =", fee, "印花税 =", 0)
        return True
    else:
        print("buy 买入["+name+"]失败 现金不足买入一手!!!")
        return False


def stock_sell(name, price, count):
    # 直接认为买入成功 价格-误差
    sell_money = (price-STOCK_FLOAT)*count
    fee = context.account.commission*sell_money  # 佣金
    if(fee < context.account.commission_base):
        fee = context.account.commission_base
    fee1 = context.account.tax*sell_money  # 印花税
    fee += fee1

    context.account.money += sell_money  # 加上卖出金额
    context.account.money -= fee  # 减去费用
    context.account.stock -= count
    print("sell 卖出["+name+"]成功 剩余现金 =", context.account.money, ",持有股票 =",
          context.account.stock, "成交额 =", sell_money, "总费用 =", fee, "印花税 =", fee1)


def summarize(date, price):
    curTotal = context.account.money+context.account.stock*price
    orignTotal = context.account_initial.money
    orignPrice = context.account_initial.price_start

    my_profit = (curTotal-orignTotal)/orignTotal*100
    standard_profit = (price-orignPrice)/orignPrice*100
    print(date+" 当前我的资产总价值 money = ", curTotal, "策略收益 =",
          str(my_profit)+"%", "基准收益 = ", str(standard_profit)+"%")
    print("我的现金 =", context.account.money, "我的股票 =",
          context.account.stock, "*", price)

    context.matplot.date.append(date)
    context.matplot.my.append(my_profit)
    context.matplot.standard.append(standard_profit)


def draw_figure(context):
    fig = plt.figure("盈利分析", figsize=(18, 6))

    date_times = [datetime.datetime.strptime(
        x, '%Y-%m-%d') for x in context.matplot.date]
    # print(date_times[0])

    dates = matplotlib.dates.date2num(date_times)

    # 设置标题
    fig.suptitle('stock profit', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(dates, context.matplot.standard)
    ax.plot(dates, context.matplot.my, 'r')

    # x轴标签旋转角度
    plt.xticks(rotation=90)
    # for label in ax.xaxis.get_ticklabels():
    #   label.set_rotation(45)

    ax.set_xlabel("date")
    ax.set_ylabel("%")

    print("len(context.matplot.date) =", len(context.matplot.date))
    #print("matplotlib.ticker.Locator.MAXTICKS =",matplotlib.ticker.Locator.MAXTICKS)
    interval = math.ceil(len(context.matplot.date) / 30)
    print("interval =", interval)
    interval = 1 if interval == 0 else interval
    ax.xaxis.set_major_locator(mdates.DayLocator(
        bymonthday=range(1, 31), interval=interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

    # plt.savefig("easyplot.jpg")
    plt.show()

# 开始日期 format：YYYY-MM-DD 为空时取上市首日
# 结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
# 数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D


"""
159915  起始日期为 2011-12-09
300033  2009-12-25
300104  2010-08-31
"""
# "2011-09-08","2014-09-08"
context = QuantStockContext("2017-08-15", "", "D")  # 2015-08-10
context.security = "159915"

context.order.buy = stock_buy
context.order.sell = stock_sell
context.summarize = summarize
#print("context.user_data =",id(context.user_data))

context.account_initial.money = 2000  # 起始持有RMB数量
context.account_initial.stock = 0  # 起始持有股票数量
context.account.commission = 0.00025  # 万二点五佣金
context.account.commission_base = 5  # 佣金最低额
context.account.tax = 0.001  # 印花税  交易上海的股票需要过户费,我暂且忽略过户费

# 海龟策略


def main(fromFile=False):
    # 初始化我的账户钱和股票数量
    data = None
    account_file = "account.temp"
    if fromFile:  # 如果读取来自文件的
        try:
            with open(account_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            pass

    if data:
        context.account.money = data['money']
        context.account.stock = data['stock']
        #context.start_time = data['today']
    else:
        context.account.money = context.account_initial.money
        context.account.stock = context.account_initial.stock

    print("tushare version =", tushare.__version__)
    print("*"*100)
    # print("quant_stock 当前目录=",os.getcwd())
    # print(sys.path[0])
    # 上面两种方式在脚本被其他脚本引入的时候的目录不准确,是引入他们的文件的目录
    print(file_helper.get_curpy_dir(__file__))

    account_stock = {}
    try:
        with open("account_stock", "r") as file:
            account_stock = json.load(file)
    except FileNotFoundError:
        print("再见")
        return  # 再见

    # 测试实盘登陆账号 中信
    # tushare.set_broker("csc",account_stock["account"],account_stock["pwd"])
    # context.trader = tushare.trader.trader.TraderAPI("csc")
    # context.trader.login()
    # print(context.trader.baseinfo())

    # return

    k_data = tushare.get_k_data(
        context.security, start=context.start_time, end=context.end_time, ktype=context.frequency)
    print(k_data)
    # print(type(k_data))
    # print(len(k_data))

    # 测试 pandas.core.series.Series 和 pandas.core.frame.DataFrame
    # k_data_seg = k_data[1399:1410] # [1399,1410)             这里弄个开区间
    # print(k_data_seg)
    # print(k_data_seg[-10:])#取最后10行数据
    # print("***1")
    # print(k_data_seg[5:])#取第5行到后面的数据
    # print("***2")
    # #下面这个访问，指定第1401行到第1406行(行数由总索引指定)，指定 high列
    # print(k_data_seg.loc[1401:1406,["high"]]) #[1401:1406]    这里弄个闭区间，卧槽
    # print("**")
    # print(k_data_seg.loc[5:7,["high"]]) # 空数据
    # print("**")
    # print(k_data_seg.loc[-7:-5,["high"]]) # 空数据，不支持负行数索引
    # print("***3")
    # #下面这个访问，指定第1行到第2行(行数由当前分片所决定)，指定 2、3列
    # print(k_data_seg.iloc[1:2,[2,3]]) #[1:2) 这里又是开区间...
    # print("**")
    # print(k_data_seg.iloc[1401:1406,[2,3]]) #空数据  卧槽，，真烦，行数代表意义不统一
    # print("**")
    # print(k_data_seg.iloc[-10:-9,[2,3]]) # 支持负行数索引
    # print("***4")
    # k_data_seg_high = k_data_seg["high"]
    # print(k_data_seg_high,type(k_data_seg_high)) # 访问指定列
    # print("**")
    # print(k_data_seg_high[1:3])
    # print(k_data_seg_high[-10:-8])
    # # last_seg_high_max = np.max(k_data_seg_high[1:3])
    # # print("last_seg_high_max",last_seg_high_max)
    # #pandas.core.series.Series 转换成数组然后再访问
    # k_data_seg_high_arra =  k_data_seg_high[1:3].get_values()
    # print(k_data_seg_high_arra,type(k_data_seg_high_arra))
    # print(k_data_seg_high_arra[0]) #numpy.ndarray
    # return

    k_data_start = k_data.iloc[0]
    # print(k_data_start)
    if data:
        context.account_initial.price_start = data['price_start']
    else:
        context.account_initial.price_start = k_data_start.open
    print(k_data_start.date + " first open =",
          context.account_initial.price_start)

    # 初始化量化策略
    quant_strategy.quant_init(context, fromFile)
    # 获取策略要求的bar数量
    needCount = quant_strategy.quant_need_count(context)
    #print("needCount =",needCount)
    # print(k_data[0:needCount])
    for i in range(len(k_data)):
        # print("i",i)
        k_data_seg = []

        realIndex = i+1
        if realIndex < needCount:
            k_data_seg = k_data[0:realIndex]
        else:
            k_data_seg = k_data[realIndex-needCount:realIndex]

        # DataFrame 只支持正向的索引,不支持负数访问
        # print(k_data_seg.loc[0:5,["close"]])

        # print(k_data_seg)
        if len(k_data_seg) != 0:
            print("进入处理函数    "+(">"*100))
            quant_strategy.handle_data(context, k_data_seg)
            print("进入处理函数 end"+("<"*100))

            hist_end_data = k_data_seg.iloc[len(k_data_seg)-1]  # 获取当前时间段内的收盘价
            # print(hist_end_data.close)
            context.summarize(hist_end_data.date, hist_end_data.close)  # 总结财富

    # 先保存到文件
    save_to = {'money': context.account.money, 'stock': context.account.stock,
               "price_start": context.account_initial.price_start, "today": str(datetime.date.today())}
    with open(account_file, "w") as file:
        json.dump(save_to, file)

    # 然后绘制图表
    draw_figure(context)


if __name__ == '__main__':
    main()
