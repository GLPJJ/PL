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

from web3 import Web3
from pathlib import (
    Path,
)

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


def sendToMyAddress(ethNodeUrl,destAddress,srcAddress,srcPrivateKey,gas=21000)->bool:
    '''
        @destAddress 目标地址
        @srcAddress 源地址
        @srcPrivateKey 源地址私钥
        @gas 目前用常量21000,可以通过这个方法估算eth.estimate_gas({'to': ethToAddress, 'from':ethFromAddress, 'value': value})
    '''
    try:
        w3 = Web3(Web3.HTTPProvider(ethNodeUrl))
        print("w3.isConnected()=",w3.isConnected())
        if not w3.isConnected():
            return False

        eth = w3.eth
        ethToAddress = destAddress
        ethFromAddress = srcAddress
        valueLimit = Web3.toWei(3, 'ether') #3个ETH
        print("获取接收地址的eth余额",eth.get_balance(destAddress))
        srcBalance = eth.get_balance(srcAddress)
        print("获取发送地址的eth余额",srcBalance)

        if srcBalance < valueLimit:
            print("乞讨地址上的数量不足=",srcBalance,"<",valueLimit)
            return False
        
        nowGasPrice = eth.gas_price
        print("eth.gas_price=",nowGasPrice)
        # print("last gas=",block.gasUsed)
        print("estimate_gas",gas)

        signed_txn = eth.account.sign_transaction(dict(
            #这个nonce必须是这个用法，否则交易会失败，取的是当前这个地址已经交易的数量
            nonce=eth.get_transaction_count(srcAddress) , 
            gasPrice=nowGasPrice, #1GWEI=e3MWEI=e6KWEI=e9WEI
            gas=gas, #使用估算的gas
            to=destAddress,
            value=srcBalance-gas*nowGasPrice,
            data=b'',
          ),
          srcPrivateKey,
        )
        print("signed_txn.hash=",signed_txn.hash.hex())
        sendResult = eth.send_raw_transaction(signed_txn.rawTransaction)
        print("txn=",signed_txn.hash.hex(),"is sending")
        # waitResult = eth.wait_for_transaction_receipt(sendResult,timeout=60)
        # print(waitResult)
    except Exception as e:
        print("Exception:",e)
        return False
    return True

if __name__ == '__main__':
    random.seed(time.time())
    print(math.floor(time.time()))
    nonce = getNonce(8)
    print(nonce)
    print(nonce[:-1])

    #项目eth节点url
    myEthInfuraUrl = 'https://ropsten.infura.io/v3/a0331ef417e84fd8a14323bd5f9bde4a'
    #目标地址
    myEthDestAddress = "0x572E492ccA2508A12e97308d0F91a7371acbfDAD" #1
    #乞讨地址
    myEthDatas = [
    {'address':"0xb6B146651b69C8bA7EE5e8dFA64a051fE06565a4","private_key":""},#2
    {'address':"0x73FCc2A4B2a1BC7F2357bb89d6bAE768673ab7e8","private_key":""},#3
    {'address':"0x09379F629570922c4B09Bd5912Ef12c6315209D9","private_key":""},#4
    {'address':"0x60EEd3cde0a1B77e4B76e938A67b1Bc65eA658d7","private_key":""},#5
    {'address':"0xa4ee950B6089CA0b1C646b77729eA471a6836B87","private_key":""},#6
    {'address':"0xB58964ECE18C713fcEDaDc1e76861493f43cee5C","private_key":""},#7
    {'address':"0xA440729AEf12B47537dE434D99c60bf46af922C2","private_key":""},#8
    {'address':"0x6ae4f198aA644d326b13787D6317A5f1f466Af2E","private_key":""},#9
    {'address':"0x980cc2F02C005F3b86F029fDc11e5c350f626e7c","private_key":""},#10
    {'address':"0x8459c9F1Fc3D57D04a8AfA47779040bD7c727dfe","private_key":""},#11
    ]

    cnt = 0
    def do(threadID,address):
        #每个地址请求5次
        global cnt
        cnt += 1
        if cnt >= 50:
            print("sleep...")
            time.sleep(600.1) #休息10.1秒
            cnt = 0
        httpsPost(threadID,"faucet.metamask.io","/v0/request",{},
                address,{"content-type": "application/rawdata"})

    #由于同一IP限制访问，先做同步请求，一个一个去请求eth
    ethDataPre = None
    while True:
        for i in range(len(myEthDatas)):
            ethData = myEthDatas[i]
            for j in range(5):
                do(i,ethData['address'])
                time.sleep(2.1)

            #请求5次之后查看一下地址上的数量,收集一下。
            if ethDataPre:
                sendToMyAddress(myEthInfuraUrl,myEthDestAddress,ethDataPre['address'],ethDataPre['private_key'])
            ethDataPre = ethData

