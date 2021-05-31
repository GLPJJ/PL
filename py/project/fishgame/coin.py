import numpy as np

import matplotlib
import matplotlib.pyplot as plt


def catchData(uid,file):
    bills = []
    coins = []
    nowBill = 0
    with open(file,"r") as f:
        for line in f:
            # print("循环读取文件行", line, end="")  # 读取的行内容带有换行符 \n
            if line.find("_"+str(uid)) != -1 and line.find("fish nil") == -1:
                #读取usr位置
                pos = line.find("usr")
                pos1 = line.find(",",pos)
                pos2 = line.find(",",pos1+1)
                coin = int(line[pos1+1:pos2])
                pos3 = line.find("<",pos2+1)
                bullet = int(line[pos2+1:pos3])
                print(uid,"coin=",coin,"bullet=",bullet)
                bills.append(nowBill)
                coins.append(coin)
                nowBill += bullet
    return bills,coins


def coinMain(uid,file):
    x,y = catchData(uid,file)
    # print("bills=",x)
    # print("coins=",y)

    plt.rcParams["font.family"]="SimHei" 
    plt.figure(str(uid))

    fig=plt.figure(num=1)
    fig.suptitle(str(uid), fontsize=14, fontweight='bold')
    ax=fig.add_subplot(1,1,1)
    ax.set_xlabel("流水")
    ax.set_ylabel("金币")

    ax.tick_params(length=10)
    ax.plot(x, y)

    plt.show()

if __name__ == '__main__':
    # coinMain(630322,"F:\\迅雷下载\\fish_UKFL_20210423_00.log")
    coinMain(160027,"F:\\迅雷下载\\fish-js_UKFL_20210423_00.log")
    # for uid in range(101500,101700,1):
    #     coinMain(uid,"F:\\迅雷下载\\fish-js_UKFL_20210422_00.log")