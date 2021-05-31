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

#eth模块
#设定pip下载镜像地址
#pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# pip install web3


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

def getNonceNum(l=8):
    bs = "0123456789abcdef"
    res = ""
    for i in range(l):
        res += bs[random.randint(0,len(bs)-1)]
    return int(res,16)


def logSafeInThreads(log):
    with GLOBAL_LOCK:
        print(log+"\n")

def httpGet(testID,host,api,params,heads=None):
    conn = http.client.HTTPConnection(host)
    getRequest(conn,testID,host,api,params,heads)

def httpsGet(testID,host,api,params,heads=None):
    conn = http.client.HTTPSConnection(host)
    getRequest(conn,testID,host,api,params,heads)

def httpPost(testID,host,api,params,body,heads=None):
    conn = http.client.HTTPConnection(host)
    postRequest(conn,testID,host,api,params,heads,body)

def httpsPost(testID,host,api,params,body,heads=None):
    conn = http.client.HTTPSConnection(host)
    postRequest(conn,testID,host,api,params,heads,body)

def getRequest(conn,testID,host,api,params,heads):
    customRequest("GET",conn,testID,host,api,params,heads,None)

def postRequest(conn,testID,host,api,params,heads,body):
    customRequest("POST",conn,testID,host,api,params,heads,body)

def customRequest(method,conn,testID,host,api,params,heads,body):
    vals = ""
    for k,v in params.items():
        vals += k+"="+v+"&"
    if len(vals) > 0:
        api += "?"+vals[:-1]

    headFor = copy.deepcopy(GLOBAL_HEADS)

    if heads:
        headFor.update(heads)

    try:
        print("https://"+host+api,"heads=",heads,"body=",body)
        conn.request(method, api, body, headFor)
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


        log = "{0:04d}-[{1}.{2:07d}] status={status}|result={data}".format(testID,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            int(str(time.time()).split(".")[1]),status=response.status,data=data)
        logSafeInThreads(log)
    except Exception as e:
        print("Exception=",e)

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

    myEthAddress = ["0xb6B146651b69C8bA7EE5e8dFA64a051fE06565a4",#2
    "0x73FCc2A4B2a1BC7F2357bb89d6bAE768673ab7e8",#3
    "0x09379F629570922c4B09Bd5912Ef12c6315209D9",#4
    "0x60EEd3cde0a1B77e4B76e938A67b1Bc65eA658d7",#5
    "0xa4ee950B6089CA0b1C646b77729eA471a6836B87",#6
    "0xB58964ECE18C713fcEDaDc1e76861493f43cee5C",#7
    "0xA440729AEf12B47537dE434D99c60bf46af922C2",#8
    "0x6ae4f198aA644d326b13787D6317A5f1f466Af2E",#9
    "0x980cc2F02C005F3b86F029fDc11e5c350f626e7c",#10
    "0x8459c9F1Fc3D57D04a8AfA47779040bD7c727dfe",#11
    ]

    cnt = 0
    def do(threadID,address):
        #每个地址请求5次
        global cnt
        cnt += 1
        if cnt >= 40:
            print("sleep...")
            time.sleep(120.1) #休息10.1秒
            cnt = 0
        httpsPost(threadID,"faucet.metamask.io","/v0/request",{},
                address,{"content-type": "application/rawdata"})

    #由于同一IP限制访问，先做同步请求，一个一个去请求eth
    while True:
        for i in range(len(myEthAddress)):
            for j in range(5):
                do(i,myEthAddress[i])
    

    # for i in range(1000):
    #     do(i)
    # do(1)

    #下面是创建10个线程，每个线程独立请求eth
    # limit = len(myEthAddress)
    # aws = []
    # for i in range(limit):
    #     aws.append(AsyncWork(do,i)) #创建线程

    # for i in range(limit):
    #     aws[i].start() #启动线程

    # for i in range(limit):
    #     aws[i].join() #等待线程结束
