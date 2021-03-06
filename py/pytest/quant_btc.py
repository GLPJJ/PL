# 注：该策略仅供参考和学习，不保证收益。

# !/usr/bin/env python
# -*- coding: utf-8 -*-

# 策略代码总共分为三大部分，1)PARAMS变量 2)initialize函数 3)handle_data函数
# 请根据指示阅读。或者直接点击运行回测按钮，进行测试，查看策略效果。

# 策略名称：海龟交易策略
# 策略详细介绍：https://wequant.io/study/strategy.turtle_trading.html
# 关键词：趋势跟随、资金管理、分批建仓、动态止损。
# 方法：
# 1)利用唐安奇通道来跟踪趋势产生买卖信号；
# 2)利用ATR（真实波幅均值）分批加仓或者减仓；
# 3)并且动态进行止盈和止损。


import numpy as np

# 阅读1，首次阅读可跳过:
# PARAMS用于设定程序参数，回测的起始时间、结束时间、滑点误差、初始资金和持仓。
# 可以仿照格式修改，基本都能运行。如果想了解详情请参考新手学堂的API文档。
PARAMS = {
    "start_time": "2016-01-01 00:00:00",  # 回测的起始时间
    "end_time": "2017-09-08 00:00:00",  # 回测的结束时间
    "commission": 0.002,  # 此处设置交易佣金
    "slippage": 0.001,  # 此处设置交易滑点
    "account_initial": {"huobi_cny_cash": 100000,
                        "huobi_cny_btc": 0},
}


# 阅读2，遇到不明白的变量可以跳过，需要的时候回来查阅:
# initialize函数是两大核心函数之一（另一个是handle_data），用于初始化策略变量。
# 策略变量包含：必填变量，以及非必填（用户自己方便使用）的变量
def initialize(context):
    # context.log.info("进入初始化函数")
    """
    设置回测频率
    "1m" – 每1分钟生成数据，从00分00秒开始计算一分钟，01分00秒属于下一分钟，不重复计算，以此类推
    "5m" – 每5分钟生成数据，原理同上
    "15m" – 每15分钟生成一行数据，原理同上
    "30m" – 每30分钟生成一行数据，原理同上
    "60m" – 每60分钟生成一行数据，原理同上
    "4h" – 每4小时生成一行数据，从00:00:00开始计算4小时，04:00:00属于下一个4小时，不重复计算，以此类推
    "1d" – 每天生成一行数据，从00:00:00开始计算一天，24:00:00属于次日00:00:00，不重复计算
    "1w" – 每周生成一行数据，从周日00:00:00开始计算一周，周六24:00:00属于下周日00:00:00，不重复计算
    "1M" – 每月生成一行数据，从每月1日00:00:00开始计算一月，每月最后一天24:00:00属于下个月1日00:00:00，不重复计算
    """
    context.frequency = "1d"

    '''
    设置回测基准 -- 基准线
    "huobi_cny_btc" – 火币人民币比特币现货
    "huobi_cny_ltc" – 火币人民币莱特币现货
    "huobi_cny_eth" – 火币人民币以太坊现货
    '''
    context.benchmark = "huobi_cny_btc"

    '''
    设置回测标的 -- 回测线
    "huobi_cny_btc" – 火币人民币比特币现货
    "huobi_cny_ltc" – 火币人民币莱特币现货
    "huobi_cny_eth" – 火币人民币以太坊现货
    '''
    context.security = "huobi_cny_btc"

    # 设置ATR值回看窗口
    context.user_data.T = 10  # >= 1

    # 认为比特币未来将上涨
    # 设置买入atr倍数
    context.user_data.BuyAtr = 0.5
    # 设置卖出atr倍数
    context.user_data.SellAtr = 3.6  # 4#3.6

    context.user_data.BuyUnit = 0.01

    context.user_data.IsFirstInHandle = True
    # 自定义的初始化函数
    init_local_context(context)

    #all_securities = context.data.get_all_securities()
    # context.log.info(context.account)

    #context.log.info("进入初始化函数 end")
    # 至此initialize函数定义完毕。

# 用户自定义的函数，可以被handle_data调用:用于初始化一些用户数据


def init_local_context(context):
    # 上一次买入价
    context.user_data.last_buy_price = 0
    # 是否持有头寸标志
    # context.account.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY
    context.user_data.hold_flag = False
    # 限制最多买入的单元数
    context.user_data.limit_unit = 4
    # 现在买入1单元的security数目
    context.user_data.unit = 0
    # 买入次数
    context.user_data.add_time = 0

# 阅读3，策略核心逻辑：
# handle_data函数定义了策略的执行逻辑，按照frequency生成的bar依次读取并执行策略逻辑，直至程序结束。
# handle_data和bar的详细说明，请参考新手学堂的解释文档。


def handle_data(context):
    context.log.info("进入处理函数")

    # context.log.info(context.account)
    # if context.user_data.IsFirstInHandle:
    #     context.user_data.hold_flag = context.account_initial.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY
    #     #context.log.info(str(context.account_initial.huobi_cny_btc)+";"+str(context.account.huobi_cny_btc))
    #     context.user_data.IsFirstInHandle = False

    # 获取历史数据
    hist = context.data.get_price(
        context.security, count=context.user_data.T + 1, frequency=context.frequency)
    if len(hist.index) < (context.user_data.T + 1):
        context.log.warn("bar的数量不足, 等待下一根bar...")
        return

    # 获取当前行情数据
    price = context.data.get_current_price(context.security)

    # 1 计算ATR
    atr = calc_atr(hist.iloc[:len(hist)-1])

    # 2 判断加仓或止损
    if context.user_data.hold_flag is True and context.account.huobi_cny_btc > 0:  # 先判断是否持仓
        context.log.info("判断是加仓还是止损")
        temp = add_or_stop(
            price, context.user_data.last_buy_price, atr, context)
        if temp == 1:  # 判断加仓
            if context.user_data.add_time < context.user_data.limit_unit:  # 判断加仓次数是否超过上限
                context.log.info("产生加仓信号")
                context.log.info("min("+str(context.account.huobi_cny_cash) +
                                 ","+str(context.user_data.unit)+"*"+str(price))
                cash_amount = min(context.account.huobi_cny_cash,
                                  context.user_data.unit * price)  # 不够1 unit时买入剩下全部
                context.user_data.last_buy_price = price
                if cash_amount >= HUOBI_CNY_BTC_MIN_ORDER_CASH_AMOUNT:
                    context.user_data.add_time += 1
                    context.log.warn("正在买入 "+context.security +
                                     " ;下单金额为 "+str(cash_amount)+" 元")
                    context.order.buy(context.security,
                                      cash_amount=str(round(cash_amount, 2)))
                else:
                    context.log.info("订单无效，下单金额小于交易所最小交易金额")
            else:
                context.log.info("加仓次数已经达到上限，不会加仓")
        elif temp == -1:  # 判断止损
            # 重新初始化参数！重新初始化参数！重新初始化参数！非常重要！
            init_local_context(context)
            # 卖出止损
            context.log.warn("产生止损信号;正在卖出 "+str(context.security) +
                             ";卖出数量为 "+str(context.account.huobi_cny_btc))
            context.order.sell(context.security, quantity=str(
                context.account.huobi_cny_btc))
    # 3 判断入场离场
    else:
        context.log.info("判断是进场还是离场")
        out = in_or_out(context, hist.iloc[:len(
            hist) - 1], price, context.user_data.T)
        if out == 1:  # 入场
            if context.user_data.hold_flag is False:
                context.log.info(
                    "账户余额cny = "+str(context.account.huobi_cny_net)+",art="+str(atr))
                value = context.account.huobi_cny_net * context.user_data.BuyUnit
                context.user_data.unit = calc_unit(value, atr)
                context.log.info("入场单元 context.user_data.unit=" +
                                 str(context.user_data.unit)+"*"+str(price))
                context.user_data.add_time = 1
                context.user_data.hold_flag = True
                context.user_data.last_buy_price = price
                cash_amount = min(context.account.huobi_cny_cash,
                                  context.user_data.unit * price)
                # 有买入信号，执行买入
                context.log.warn(
                    "产生入场信号;正在买入 " + context.security + " ;下单金额为 "+str(cash_amount)+" 元")
                context.order.buy(context.security,
                                  cash_amount=str(round(cash_amount, 2)))
            else:
                context.log.info("已经入场，不产生入场信号")
        elif out == -1:  # 离场
            if context.account.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY:  # context.user_data.hold_flag is True
                # 重新初始化参数！重新初始化参数！重新初始化参数！非常重要！
                init_local_context(context)
                # 有卖出信号，且持有仓位，则市价单全仓卖出
                context.log.warn("产生止盈离场信号;正在卖出 " + context.security +
                                 " ;卖出数量为 "+str(context.account.huobi_cny_btc))
                context.order.sell(context.security, quantity=str(
                    context.account.huobi_cny_btc))
            else:
                context.log.info("尚未入场或已经离场，不产生离场信号")
    context.log.info("进入处理函数 end")


# 用户自定义的函数，可以被handle_data调用: 唐奇安通道计算及判断入场离场
# data是日线级别的历史数据，price是当前分钟线数据（用来获取当前行情），T代表需要多少根日线
def in_or_out(context, data, price, T):
    up = np.max(data["high"].iloc[-T:])
    # 这里是T/2唐奇安下沿，在向下突破T/2唐奇安下沿卖出而不是在向下突破T唐奇安下沿卖出，这是为了及时止损
    down = np.min(data["low"].iloc[-int(T / 2):])
    context.log.info("当前价格为: %s, 唐奇安上轨为: %s, 唐奇安下轨为: %s" % (price, up, down))
    # 当前价格升破唐奇安上沿，产生入场信号
    if price > up:
        context.log.info("价格突破唐奇安上轨")
        return 1
    # 当前价格跌破唐奇安下沿，产生出场信号
    elif price < down:
        context.log.info("价格跌破唐奇安下轨")
        return -1
    # 未产生有效信号
    else:
        context.log.info("价格未产生有效信号")
        return 0

# 用户自定义的函数，可以被handle_data调用
# 判断是否加仓或止损:当价格相对上个买入价上涨 0.5ATR时，再买入一个unit; 当价格相对上个买入价下跌 2ATR时，清仓


def add_or_stop(price, lastprice, atr, context):
    buyArtPrice = lastprice + context.user_data.BuyAtr * atr
    sellArtPrice = lastprice - context.user_data.SellAtr * atr
    if price >= buyArtPrice:
        context.log.info(
            "当前价格比上一个购买价格上涨超过"+str(context.user_data.BuyAtr)+"个ATR("+str(buyArtPrice)+")")
        return 1
    elif price <= sellArtPrice:
        context.log.info(
            "当前价格比上一个购买价格下跌超过"+str(context.user_data.SellAtr)+"个ATR("+str(sellArtPrice)+")")
        return -1
    else:
        context.log.info(
            "当前价格在我们的波动返回内("+str(sellArtPrice)+"~"+str(buyArtPrice)+")")
        return 0

# 用户自定义的函数，可以被handle_data调用：ATR值计算


def calc_atr(data):  # data是日线级别的历史数据
    tr_list = []
    for i in range(len(data)):
        tr = max(data["high"].iloc[i] - data["low"].iloc[i], data["high"].iloc[i] - data["close"].iloc[i - 1],
                 data["close"].iloc[i - 1] - data["low"].iloc[i])
        tr_list.append(tr)
    atr = np.array(tr_list).mean()
    return atr


# 用户自定义的函数，可以被handle_data调用
# 计算unit
def calc_unit(per_value, atr):
    return per_value / atr
