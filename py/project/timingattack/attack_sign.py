import codecs
# Http 模块
import http.client
import urllib.parse
# json解析模块
import json
import gzip
import time
import math
import copy

import threading
import random

import sys
sys.path.append(__file__[:__file__.rfind("\\")]+"\\..")
import file_helper

GLOBAL_LOCK = threading.RLock()  # 折返锁，同一线程可锁定多次
GLOBAL_HEADS = {"Content-type": "application/x-www-form-urlencoded", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
    "Accept-Encoding": "gzip", 'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9', "cache-control": "max-age=0",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

GLOBAL_HEADS2 = {"Content-type": "application/x-www-form-urlencoded", 
    "Accept": "text/html,application/xhtml+xml,application/xml", 
    'Connection': 'keep-alive'}


def getNonce(l=8):
    bs = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    for i in range(l):
        res += bs[random.randint(0,len(bs)-1)]
    return res

def sign(params,prefix,subfix):
    keys = []
    for k,_ in params.items():
        keys.append(k)
    keys.sort()
    
    middle = ""
    for i in range(len(keys)):
        middle += keys[i]+"="+params[keys[i]]+"&"
    text = prefix+middle[:-1]+subfix
    print("md5["+text+"]")
    return file_helper.md5_str(text)


def logSafeInThreads(log):
    with GLOBAL_LOCK:
        print(log)

def httpGet(testID,host,method,params,needSign=False,prefix="web_",subfix="_game",heads=None):
    conn = http.client.HTTPConnection(host)
    getRequest(conn,testID,host,method,params,needSign,prefix,subfix,heads)

def httpsGet(testID,host,method,params,needSign=False,prefix="web_",subfix="_game",heads=None):
    conn = http.client.HTTPSConnection(host)
    getRequest(conn,testID,host,method,params,needSign,prefix,subfix,heads)

def getRequest(conn,testID,host,method,params,needSign,prefix,subfix,heads):
    vals = ""
    for k,v in params.items():
        vals += k+"="+v+"&"
    if len(vals) > 0 or needSign:
        method += "?"+vals[:-1]

    headFor = copy.deepcopy(GLOBAL_HEADS) #GLOBAL_HEADS2

    if needSign:
        if not heads:
            heads = {}
        if "curtime" not in heads:
            heads["curtime"] = str(math.floor(time.time()))
        if "nonce" not in heads:
            heads["nonce"] = getNonce(8)

        headForSign = copy.deepcopy(heads)
        headForSign.update(params)
        method += "&sign="+sign(headForSign,prefix,subfix)


    if heads:
        headFor.update(heads)

    print("https://"+host+method,"heads=",heads)
    conn.request("GET", method, None, headFor)
    response = conn.getresponse()
    # print(response.status, response.reason)

    data = ""
    # print("info=",response.info())
    # print("info end")
    if response.info().get('Content-Encoding') == 'gzip':
        print("gziped")
        data = gzip.decompress(response.read()).decode("utf-8")
    else:
        data = response.read().decode("utf-8")


    log = "{0:04d}-[{1}.{2:07d}] result={data}".format(testID,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        int(str(time.time()).split(".")[1]),data=data)
    logSafeInThreads(log)

def getRequest2(conn,testID,host,method,params,needSign,prefix,subfix,heads):
    vals = ""
    for k,v in params.items():
        print(k,v)
        vals += k+"="+v+"&"
    print("len(vals)=",len(vals),vals)
    if len(vals) > 0 or needSign:
        method += "?"+vals[:-1]

    print("method=",method)
    headFor = copy.deepcopy(GLOBAL_HEADS)
    if heads:
        headFor.update(heads) #插入新增的head

    print("https://"+host+method,"heads=",heads)
    msBegin = time.time()*1000
    print("begin time(毫秒)=",msBegin)
    conn.request("GET", method, None, headFor)
    response = conn.getresponse()
    msEnd = time.time()*1000
    print("end time(毫秒)=",msEnd)
    data = ""
    if response.info().get('Content-Encoding') == 'gzip':
        print("gziped")
        data = gzip.decompress(response.read()).decode("utf-8")
    else:
        data = response.read().decode("utf-8")


    log = "{0:04d}-[{1}.{2:07d}] result={data}".format(testID,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        int(str(time.time()).split(".")[1]),data=data)
    logSafeInThreads(log)
    return msEnd - msBegin

class AsyncWork(threading.Thread):
    count = 0
    # lock = threading.RLock()  # 折返锁，同一线程可锁定多次

    def __init__(self,do,threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.do = do

    # 重载run函数
    def run(self):
        self.do(self.threadID)

if __name__ == '__main__':
    random.seed(time.time())
    print(math.floor(time.time()))
    # nonce = getNonce(8)
    # print(nonce)
    # print(nonce[:-1])
    # print(sign({"nonce":nonce,"anonce":nonce},"start","end"))

    dictPrefixTime = {}
    lockUpdate = threading.RLock()
    def updateTime(prefix,ms_avg):
        with lockUpdate:
            dictPrefixTime[prefix] = ms_avg

    def do(threadID):
        # httpsGet(threadID,"www.fanyu123.cn","/testlogin/test",{},True)
        # httpGet(threadID,"192.168.0.168:7101","/updateCfg",{"token":"auth_notify"},True)

        httpsGet(threadID,"www.fanyu123.cn","/testlogin/login",{
                    'desc':'Windows7','emulator':'0','flavors':'AOfficial','platform':'0',
                    'pwd':'9cbf8a4dcb8e30682b927f352d6559a0','qiye':'1','uname':'glp002',
                    'uuid':'EA308AD4-47E4-DD74-3EDE-70644471340A','uuid2':'undefined',
                    'ver':'2.0.2.184'},True,"","",{"nonce":"LzqNVE","curtime":"1703099098"})
        pass

    def do2(param):
        print("param=",param)
        prefix,size,limit = param["prefix"],param["size"],param["limit"]
        sign = prefix + '0'*(size-len(prefix))

        #https://www.fanyu123.cn/auth/login?desc=Windows%207&emulator=0&flavors=AOfficial&platform=0&pwd=9cbf8a4dcb8e30682b927f352d6559a0&qiye=1&uname=glp002&uuid=EA308AD4-47E4-DD74-3EDE-70644471340A&uuid2=undefined&ver=2.0.2.184&sign=c769f982dde84a1ea80037473d2225ae heads={"nonce":"LzqNVE","curtime":"1603099098"}
        ms = 0
        for i in range(limit):
            conn = http.client.HTTPSConnection("www.fanyu123.cn")
            ms += getRequest2(conn,param["threadID"],"www.fanyu123.cn","/testlogin/login",{
                    'desc':'Windows7','emulator':'0','flavors':'AOfficial','platform':'0',
                    'pwd':'9cbf8a4dcb8e30682b927f352d6559a0','qiye':'1','uname':'glp002',
                    'uuid':'EA308AD4-47E4-DD74-3EDE-70644471340A','uuid2':'undefined',
                    'ver':'2.0.2.184','sign':sign},False,"","",{"nonce":"LzqNVE","curtime":"1703099098"})
        updateTime(prefix,ms/limit)

    # for i in range(1000):
    #     do(1)

    do(1)

    #多线程并行
    limit = 1000
    aws = []
    # for i in range(limit):
    #     aws.append(AsyncWork(do,i))

    # limit = 16
    # prefix = "0123456789abcdef"
    # for i in range(limit):
    #     aws.append(AsyncWork(do2,{"threadID":i,"prefix":prefix[i:i+1],"size":32,"limit":500}))

    # for i in range(limit):
    #     aws[i].start()

    # for i in range(limit):
    #     aws[i].join()

    # print(dictPrefixTime)
