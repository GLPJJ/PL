import pandas  # pip install pandas
'''
pip install -i 国内镜像地址 包名

e.g. pip install -i  https://pypi.tuna.tsinghua.edu.cn/simple pandas 这是临时指定镜像地址

清华：https://pypi.tuna.tsinghua.edu.cn/simple

阿里云：http://mirrors.aliyun.com/pypi/simple/

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

华中理工大学：http://pypi.hustunique.com/

山东理工大学：http://pypi.sdutlinux.org/ 

豆瓣：http://pypi.douban.com/simple/
'''

import os
import math

def orderLog(fsv):
    print(fsv)
    csv = fsv.replace(".tsv", ".csv")
    dir = fsv[:fsv.rfind("/")]

    all = []
    with open(fsv, "r+") as f:
        for line in f:
            print("循环读取文件行", line, end="")  # 读取的行内容带有换行符 \n
            words = line.split("	")
            words[1] = "id-"+str(words[1])
            words[2] = "id-"+str(words[2])
            all.append(words)
            # print(words)
            # print(all)
            # break
    df = pandas.DataFrame(all)
    df.to_csv(csv)

def almsLog(fsv):
    print(fsv)
    csv = fsv.replace(".tsv", ".csv")
    dir = fsv[:fsv.rfind("/")]

    all = {}
    with open(fsv, "r+") as f:
        for line in f:
            # print("循环读取文件行", line, end="")  # 读取的行内容带有换行符 \n
            words = line.split("	")
            # words[1] = "id-"+str(words[1])
            # words[2] = "id-"+str(words[2])
            # all[words[2]] = {}

            dayName = words[2][:-1]
            print(dayName)
            day = {}
            uids = words[1].split(",")
            for i in range(len(uids)):
                uid = uids[i]
                if uid not in day:
                    day[uid] = 1
                else:
                    day[uid] = day[uid] + 1
            all[dayName] = day
            # print(words)
            # all.append(words)
            # print(words)
            # print(all)
            # break

    # df = pandas.DataFrame(all)
    # df.to_csv(csv)

    for k, v in all.items():
        for k1, v1 in v.items():
            # if(v1>3):
            print(k, k1, v1)

def readRate(file,key,all):
    if not key:
        raise "need key"

    with open(file, "rb") as f:
        f.seek(0,2) #定位文件末尾
        total = f.tell()

        f.seek(0,0) #定位文件首
        prePercent = 0

        buf = f.read()
        content = buf.decode("utf-8")
        
        pos = 0
        while True:
            pos = content.find(key,pos)
            # print("pos=",pos,"total=",total)
            if pos == -1:
                break

            lastNewline = content.rfind("\n", 0, pos)
            # print("lastNewline=",lastNewline)
            # print("pos=",content[pos:content.find("\n",pos+1)])
            # f.seek(lastNewline,0) #定位文件首
            # for line in f :
            # cur = f.tell()
            percent = math.floor(pos*100/total)
            print("\r"*(prePercent+6)+"*"*percent+str(percent)+"/100",end="")
            prePercent = percent
            
            # one = line.decode("utf-8")
            nextNewline = content.find("\n",lastNewline+1)
            one = content[lastNewline:content.find("\n",nextNewline)]
            pos = nextNewline
            # print("lastNewline=",one,end="")
            # break
            if one.find("fish nil") != -1:
                continue

            row = []
            try:
                #日期
                start = one.find("[")
                end = one.find("]")
                tm = one[start+1:end]
                row.append(tm)

                #子弹ID
                start = one.find(",")
                start = one.find(",",start+1)
                end = one.find(",",start+1)
                bullet = one[start+1:end]
                row.append(bullet)

                start = one.find("<fish[")
                #是否捕获
                row.append(int(one[start-1:start]))
                end = one.find(",",start)
                #鱼类型
                row.append(int(one[start+6:end]))
                start = end
                #鱼倍数
                end = one.find(",",start+1)
                row.append(int(one[start+1:end]))

                #获取金币奖励
                start = end
                end = one.find("+",start+1)
                row.append(int(one[start+1:end]))

                #个人龙珠奖池
                start = end
                end = one.find("<",start+1)
                row.append(int(one[start+1:end]))

                #今日输赢
                start = one.find("[",end+1)
                end = one.find(",",start+1)
                row.append(int(one[start+1:end]))

                #当前金币
                start = end
                end = one.find(",",start+1)
                row.append(int(one[start+1:end]))

                #子弹
                start = end
                end = one.find(",",start+1)
                row.append(int(one[start+1:end]))

                #概率体现
                start = one.find("[",end+1)
                end = one.find(">",start+1)
                row.append(int(one[start+1:end]))

                #随机数
                start = end
                end = one.find("=",start+1)
                row.append(int(one[start+1:end]))

                #鱼本身概率
                start = end
                end = one.find("*",start+1)
                row.append(float(one[start+1:end]))

                #鱼群变化概率
                start = end
                end = one.find("*",start+1)
                row.append(float(one[start+1:end]))

                #库存概率
                start = end
                end = one.find("*",start+1)
                row.append(float(one[start+1:end]))

                #个人概率=
                start = end
                end = one.find("{",start+1)
                row.append(float(one[start+1:end]))

                #个人新手
                start = end
                end = one.find("*",start+1)
                row.append(float(one[start+1:end]))

                #个人破产
                start = one.find("(",end+1)
                end = one.find(",",start+1)
                row.append(float(one[start+1:end]))

                #个人充值
                start = end
                end = one.find(")",start+1)
                row.append(float(one[start+1:end]))

                #个人输赢
                start = end+1
                end = one.find("*",start+1)
                row.append(float(one[start+1:end]))

                #个人流水保护
                start = end
                end = one.find("*",start+1)
                row.append(float(one[start+1:end]))

                #桌子流水保护
                start = end
                end = one.find("}",start+1)
                row.append(float(one[start+1:end]))

                #后台控制
                start = end+1
                end = one.find(",",start+1)
                row.append(float(one[start+1:end]))

                #单行测试
                # print(row)
                # break

                all.append(row)
            except Exception as e:
                pass
            
    print(" finish")

class Diskwalk(object):
    def __init__(self, path, recursive=True):
        """ 
                构造函数 
                @path       指定目录
                @recursive  是否遍历子目录
        """
        self.path = path
        self.recursive = recursive

    def walk(self, func=None):
        """ 
                遍历目录和文件
                @func(dirpath, file)       指定回调, 回传当前路径和文件

                @return     返回 文件名数组,全路径文件名数组  一一对应
        """
        path_collection = []
        files = []
        for dirpath, dirnames, filenames in os.walk(self.path):

            # print("dirpath=",dirpath)
            # print("dirnames=",dirnames)
            # print("filenames=",filenames)

            for file in filenames:
                dirpath = dirpath.replace("\\", "/")
                if(func and callable(func)):
                    func(dirpath, file)

                files.append(file)
                # fullpath=os.path.join(dirpath,file)
                fullpath = dirpath+"/"+file
                path_collection.append(fullpath)

            if(not self.recursive):
                break

        return files, path_collection

if __name__ == '__main__':
    import sys
    print(sys.argv, len(sys.argv))

    uid = "rid3"
    if len(sys.argv) >= 2:
        uid = sys.argv[1]
    print(uid,type(uid))

    # # orderLog("D:/glp/Github/fishing_server/sql/select___from_order_log_where__channel_2.tsv")
    # # almsLog("D:/glp/Github/fishing_server/sql/SELECT____COUNT________GROUP_CONCAT_uid_.tsv")

    all = []
    dir = "/home/logs/fish/UKFL"
    filter1 = None #"fish_UKFL_20200724_00.log"
    filter2 = None #"fish_UKFL_20200724_00.log"
    def walk1(file):
        path = file
        print("get "+path)

        if filter1 and file < filter1 or filter2 and file > filter2:
            return
        if file.endswith(".log"):
            print("deal with "+path)
            readRate(path, uid, all)
    _,files = Diskwalk(dir, False).walk()
    files.sort()
    for i in range(len(files)):
        walk1(files[i])
        # break

    # 测试单个文件
    # dir = "D:/work/捕鱼服务器"
    # readRate("/home/logs/fish/UKFL/fish_UKFL_20200723_07.log","198953",all)
    # readRate("/home/logs/fish/UKFL/fish_UKFL_20200721_05.log","198953",all)
    # readRate("C:/Users/Administrator/Desktop/198953_all","198953",all)
    # readRate("D:/work/捕鱼服务器/fish_UKFL_20200723_07.log","_198953",all)
    # readRate("D:/work/捕鱼服务器/fish_UKFL_20200723_07.log","rid3",all)

    if len(all) > 0:
        df = pandas.DataFrame(all,columns=["时间","子弹ID","是否捕获","鱼种","倍数","捕获金币","龙珠个人奖池","今日输赢","当前金币",
            "子弹","计算的概率*10w","随机数","鱼本身概率","鱼群变化概率","库存概率","个人概率=","新手","max(破财",
            "充值)","个人输赢","个人流水保护","桌子流水保护","后台控制"])
        path = dir+"/"+uid+".csv"
        df.to_csv(path)
        print("save to",path)
    else:
        print("no record")

