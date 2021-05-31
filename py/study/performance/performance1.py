import time

def performance1():
    strs = []
    for i in range(1000000):
        strs.append(""+str(i))

    # print(strs)

    log, sep = "",""
    print(time.time(), "普通循环拼接")
    for i in range(len(strs)):
        log += sep + strs[i] #粗糙的字符串拼接。。
        sep = " "
    print(time.time(), log[-1])
    log = ""
    print(time.time(), "strings.join拼接")
    log = " ".join(strs) #性能完胜啊。。
    print(time.time(), log[-1])


if __name__ == '__main__':
    performance1()

