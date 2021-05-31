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

    headFor = copy.deepcopy(GLOBAL_HEADS)

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
    nonce = getNonce(8)
    print(nonce)
    print(nonce[:-1])
    print(sign({"nonce":nonce,"anonce":nonce},"start","end"))

    def do(threadID):
        httpsGet(threadID,"www.fanyu123.cn","/testlogin/updateCfg",{"token":"auth_notify"},True)
        # httpGet(threadID,"192.168.0.168:7101","/updateCfg",{"token":"auth_notify"},True)

    for i in range(1000):
        do(1)

    # limit = 1000
    # aws = []
    # for i in range(limit):
    #     aws.append(AsyncWork(do,i))

    # for i in range(limit):
    #     aws[i].start()

    # for i in range(limit):
    #     aws[i].join()
