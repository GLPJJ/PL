import json
import numpy as np


def init_local_context(context, fromFile=False):

    # 限制最多买入的单元数
    context.user_data.limit_unit = 6  # 4(乐视)

    # 0.5(乐视) #收市均价较历史最高价跌去10% 我们止盈 0.2
    context.user_data.HistoryHighPercent = 0.2

    data = None
    cur_file = __file__
    context.user_data.data_file = cur_file[:cur_file.rfind(
        "\\")]+"/haigui.temp"
    if fromFile:  # 如果读取来自文件的
        try:
            with open(context.user_data.data_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            pass

    if data:  # 如果有数据
        # 上一次买入价
        context.user_data.last_buy_price = data['last_buy_price']
        # 是否持有头寸标志
        # context.account.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY
        context.user_data.hold_flag = data['hold_flag']

        # 现在买入1单元的security数目
        context.user_data.unit = data['unit']
        # 买入次数
        context.user_data.add_time = data['add_time']

        # 持有的时候所经历过的最高价
        context.user_data.HistoryHigh = data['HistoryHigh']  # 历史最高价,
    else:
        # 上一次买入价
        context.user_data.last_buy_price = 0
        # 是否持有头寸标志
        # context.account.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY
        context.user_data.hold_flag = False
        # 现在买入1单元的security数目
        context.user_data.unit = 0
        # 买入次数
        context.user_data.add_time = 0

        # 持有的时候所经历过的最高价
        context.user_data.HistoryHigh = 0  # 历史最高价,


def quant_init(context, fromFile):
    # 设置ATR值回看窗口
    context.user_data.T = 19  # 19 226.3723  2

    # 认为未来将上涨
    # 设置买入atr倍数
    context.user_data.BuyAtr = 0.5  # 0.5 226.3723 0.35
    # 设置卖出atr倍数
    context.user_data.SellAtr = 1.6  # 1.6  226.3723 2

    context.user_data.BuyUnit = 0.0035  # 0.0035 244.21 0.01

    init_local_context(context, fromFile)


def save_to_file(context):
    # 都需要保存到文件
    save_to = {'last_buy_price': context.user_data.last_buy_price, 'hold_flag': context.user_data.hold_flag,
               'unit': context.user_data.unit, 'add_time': context.user_data.add_time, 'HistoryHigh': context.user_data.HistoryHigh}
    with open(context.user_data.data_file, "w") as file:
        json.dump(save_to, file)


def quant_need_count(context):

    return context.user_data.T+2


def handle_data(context, k_data):
    # print(context.account)
    # if context.user_data.IsFirstInHandle:
    #     context.user_data.hold_flag = context.account_initial.huobi_cny_btc >= HUOBI_CNY_BTC_MIN_ORDER_QUANTITY
    #     #print(str(context.account_initial.huobi_cny_btc)+";"+str(context.account.huobi_cny_btc))
    #     context.user_data.IsFirstInHandle = False

    # 获取历史数据
    hist = k_data[:len(k_data)-1]  # DataFrame
    # print("hist.index=",hist.index)

    # 获取当前行情数据
    hist_end_data = k_data.iloc[len(hist)]
    #print("hist_end_data =\n",hist_end_data)
    #print("hist_end_data.open =",hist_end_data.open);
    price = hist_end_data.close
    print("当前价格 =", price, "len =", len(hist.index))

    if len(hist.index) < (context.user_data.T + 1):
        print("bar的数量不足, 等待下一根bar...")
    else:
        # 计算最高价和收市均值
        last_seg_high = hist["high"][-context.user_data.T:]
        # print(last_seg_high)
        last_seg_high_max = np.max(last_seg_high)
        print("last_seg_high_max", last_seg_high_max)
        context.user_data.HistoryHigh = max(
            last_seg_high_max, context.user_data.HistoryHigh)
        print("历史最高价 =", context.user_data.HistoryHigh)

        last_seg_close = hist["close"][-context.user_data.T:]
        last_seg_close_2 = hist["close"][int(-context.user_data.T/2):]
        # print(last_seg_close)
        # print("last_seg_close"+("*"*50))
        # print(last_seg_close_2)
        # last_seg_close_mean = np.mean(last_seg_close)
        last_seg_close_mean_2 = np.mean(last_seg_close_2)
        # print("收bar均值 =",last_seg_close_mean)
        print("收bar后半均值 =", last_seg_close_mean_2)

        # 1 计算ATR
        atr = calc_atr(hist.iloc[:len(hist)-1])
        print("atr = ", atr)

        # 2 判断加仓或止损
        if context.user_data.hold_flag and context.account.stock > 0:  # 先判断是否持仓
            temp = 0
            print("判断历史最高价是否与我们收bar均值背离")
            deviate_high = context.user_data.HistoryHigh * \
                (1-context.user_data.HistoryHighPercent)
            if last_seg_close_mean_2 < deviate_high:
                # if price < deviate_high:
                print("正在背离", last_seg_close_mean_2, "<", deviate_high)
                temp = -1
            else:
                print("没有背离,判断是加仓还是止损")
                cash_amount = min(context.account.money,
                                  context.user_data.unit * price)
                print("可能买入金额:", cash_amount)

                temp = add_or_stop(
                    price, context.user_data.last_buy_price, atr, context)

            if temp == 1:  # 判断加仓
                if context.user_data.add_time < context.user_data.limit_unit:  # 判断加仓次数是否超过上限
                    print("产生加仓信号")
                    print("min("+str(context.account.money)+"," +
                          str(context.user_data.unit)+"*"+str(price))
                    # 不够1 unit时买入剩下全部
                    cash_amount = min(context.account.money,
                                      context.user_data.unit * price)

                    context.user_data.last_buy_price = price
                    context.user_data.add_time += 1
                    save_to_file(context)
                    print("正在买入 "+context.security +
                          " ;下单金额为 "+str(cash_amount)+" 元")
                    context.order.buy(context.security, price, cash_amount)
                else:
                    print("加仓次数已经达到上限，不会加仓")
            elif temp == -1:  # 判断止损
                # 重新初始化参数！重新初始化参数！重新初始化参数！非常重要！
                init_local_context(context)
                save_to_file(context)
                # 卖出止损
                print("产生止损信号;正在卖出 "+str(context.security) +
                      ";卖出数量为 "+str(context.account.stock))
                context.order.sell(context.security, price,
                                   context.account.stock)
        # 3 判断入场离场
        else:
            print("判断是进场还是离场")
            value = context.account.money * context.user_data.BuyUnit
            unit_temp = calc_unit(value, atr)
            cash_amount = min(context.account.money, unit_temp * price)
            print("可能买入金额:", cash_amount)

            out = in_or_out(context, hist.iloc[:len(
                hist) - 1], price, context.user_data.T)
            if out == 1:  # 入场
                if not context.user_data.hold_flag:
                    print("账户余额money = "+str(context.account.money)+",art="+str(atr))
                    context.user_data.unit = unit_temp
                    print("入场单元 context.user_data.unit=" +
                          str(context.user_data.unit)+"*"+str(price))
                    context.user_data.add_time = 1
                    context.user_data.hold_flag = True

                    context.user_data.last_buy_price = price
                    save_to_file(context)
                    # 有买入信号，执行买入
                    print("产生入场信号;正在买入 " + context.security +
                          " ;下单金额为 "+str(cash_amount)+" 元")
                    context.order.buy(context.security, price, cash_amount)
                else:
                    print("已经入场，不产生入场信号")
            elif out == -1:  # 离场
                if context.account.stock > 0:  # context.user_data.hold_flag is True
                    # 重新初始化参数！重新初始化参数！重新初始化参数！非常重要！
                    init_local_context(context)
                    save_to_file(context)
                    # 有卖出信号，且持有仓位，则市价单全仓卖出
                    print("产生止盈离场信号;正在卖出 " + context.security +
                          " ;卖出数量为 "+str(context.account.stock))
                    context.order.sell(
                        context.security, price, context.account.stock)
                else:
                    print("尚未入场或已经离场，不产生离场信号")


# 用户自定义的函数，可以被handle_data调用: 唐奇安通道计算及判断入场离场
# data是日线级别的历史数据，price是当前分钟线数据（用来获取当前行情），T代表需要多少根日线
def in_or_out(context, data, price, T):
    up = np.max(data["high"].iloc[-T:])
    # 这里是T/2唐奇安下沿，在向下突破T/2唐奇安下沿卖出而不是在向下突破T唐奇安下沿卖出，这是为了及时止损
    down = np.min(data["low"].iloc[-int(T / 2):])
    print("当前价格为: %s, 唐奇安上轨为: %s, 唐奇安下轨为: %s" % (price, up, down))
    # 当前价格升破唐奇安上沿，产生入场信号
    if price >= up:
        print("价格突破唐奇安上轨")
        return 1
    # 当前价格跌破唐奇安下沿，产生出场信号
    elif price <= down:
        print("价格跌破唐奇安下轨")
        return -1
    # 未产生有效信号
    else:
        print("价格未产生有效信号")
        return 0

# 用户自定义的函数，可以被handle_data调用
# 判断是否加仓或止损:当价格相对上个买入价上涨 0.5ATR时，再买入一个unit; 当价格相对上个买入价下跌 2ATR时，清仓


def add_or_stop(price, lastprice, atr, context):
    buyArtPrice = lastprice + context.user_data.BuyAtr * atr
    sellArtPrice = lastprice - context.user_data.SellAtr * atr
    print("当前价格为: %s, 加仓价格: %s, 止损价格: %s" % (price, buyArtPrice, sellArtPrice))
    if price >= buyArtPrice:
        print("当前价格比上一个购买价格上涨超过"+str(context.user_data.BuyAtr) +
              "个ATR("+str(buyArtPrice)+")")
        return 1
    elif price <= sellArtPrice:
        print("当前价格比上一个购买价格下跌超过"+str(context.user_data.SellAtr) +
              "个ATR("+str(sellArtPrice)+")")
        return -1
    else:
        print("当前价格在我们的波动返回内("+str(sellArtPrice)+"~"+str(buyArtPrice)+")")
        return 0

# 用户自定义的函数，可以被handle_data调用：ATR值计算


def calc_atr(data):  # data是日线级别的历史数据
    tr_list = []
    for i in range(len(data)):
        tr = max(data["high"].iloc[i] - data["low"].iloc[i], data["high"].iloc[i] -
                 data["close"].iloc[i - 1], data["close"].iloc[i - 1] - data["low"].iloc[i])
        tr_list.append(tr)

    # print("calc_atr tr_list =",tr_list)
    atr = np.array(tr_list).mean()
    return atr

# 用户自定义的函数，可以被handle_data调用
# 计算unit


def calc_unit(per_value, atr):
    return per_value / atr
