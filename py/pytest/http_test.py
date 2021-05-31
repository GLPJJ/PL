#! python3.4
# @ guliping

# Http 模块
import urllib.request
import http.client
import urllib.parse
# 日期
from datetime import datetime, date, time
# UTC time
import time as _time
# 随机数
import random
# md5 sh1 加密模块
import hashlib
# json
import json

IS_TEST = False
# 必须要增加这个headers，否则会提示参数错误
HEADERS = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}

# 'Content-type': 'application/x-www-form-urlencoded',
# 'Connection':'keep-alive',
# 'Cache-Control':'max-age=0',
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

# HEADERS = {
# 		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 		'Accept-Language':'zh-CN,zh;q=0.9',
# 		'Connection':'keep-alive',
# 		'Upgrade-Insecure-Requests':'1',
# 		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
# 	}


HTTP_HEADER_TOKEN = "Dddi23*DOO#LKD3"


def get_sign(rand, time):
    array = [str(rand), str(time), HTTP_HEADER_TOKEN]
    #print("array =", array,type(array))
    array.sort()  # 对array 进行排序
    #print("array =", array)

    result = ""
    for s in array:
        result += s
    return hashlib.sha1(bytes(result, encoding="utf_8")).hexdigest()


def get_md5(params):
    s = HTTP_HEADER_TOKEN

    keys = params.keys()
    keys = sorted(keys)
    for key in keys:
        s = s+str(key)+str(params[key])
    #print("md5 origin =",s)
    return hashlib.md5(bytes(s, "utf_8")).hexdigest()


def add_head(params):
    utcTime = int(_time.time())
    #print("utcTime = ",utcTime)
    randNum = int(random.random()*(9999-1000))+1000
    #print("randNum = ",randNum)

    sign1 = get_sign(randNum, utcTime)
    #print("sign1 = ",sign1)

    sign2 = get_md5(params)
    #print("sign2 = ",sign2)

    head = {}
    head["04B29480233F4DEF5C875875B6BDC3B1"] = ""  # sign1
    head["34D1C35063280164066ECC517050DA0B"] = randNum
    head["07CC694B9B3FC636710FA08B6922C42B"] = utcTime
    head["8D777F385D3DFEC8815D20F7496026DC"] = ""  # sign2 # md5
    head["my-app-ver"] = "1.4.2"  # app 版本号
    head["area"] = "86"  # app 地区版本

    return head

# 参加普通比赛


def join_in(conn, uid, code):
    print("current uid is ", uid, "do join in!")

    tempHead = dict(HEADERS)
    #print("tempHead = ",tempHead);

    dictParams = {'uid': uid, 'code': code, "os": 1,
                  "from_tid": "14786427"}  # 1 android
    authHead = add_head(dictParams)
    #print("authHead = ",authHead);
    tempHead.update(authHead)
    #print("tempHead = ",tempHead);

    params = urllib.parse.urlencode(dictParams)
    # print(params)

    try:
        conn.request("POST", "/game/join", params, tempHead)

        response = conn.getresponse()
        data = response.read()
        print(response.status, response.reason, data, sep=';')  # 指定分隔符
    except Exception as e:
        print(str(e))
    else:
        pass
    finally:
        pass

# 战鱼德州圈 比赛报名


def check_in(conn, uid, code):
    '''
    conn：HTTPConnection连接
    uid: 用户ID
    code: 指定需要加入的牌局
    '''
    print("current uid is ", uid, "do check in!")

    tempHead = dict(HEADERS)
    #print("tempHead = ",tempHead);

    dictParams = {'uid': uid, 'code': code, "os": 1,
                  "from_tid": "14786427"}  # 1 android , 书本 1418543
    authHead = add_head(dictParams)
    #print("authHead = ",authHead);
    tempHead.update(authHead)
    #print("tempHead = ",tempHead);

    params = urllib.parse.urlencode(dictParams)
    # print(params)

    try:
        conn.request("POST", "/game/mttcheckin", params, tempHead)

        response = conn.getresponse()
        data = response.read()
        print(response.status, response.reason, data, sep=';')  # 指定分隔符
    except Exception as e:
        print(str(e))
    else:
        pass
    finally:
        pass


def check_in_number(conn, num, code):
    formalUids = [110191, 110192, 110195, 103265, 109886,
                  102243, 104859, 134975, 135061, 110457, 135569]

    if(IS_TEST):
        for uid in range(10000, 10000+num):
            check_in(conn, uid, code)
    else:
        end = min(len(formalUids), num)
        for uid in range(0, end):
            check_in(conn, formalUids[uid], code)


def join_in_number(conn, num, code):
    formalUids = [110191, 110192, 110195, 103265, 109886,
                  102243, 104859, 134975, 135061, 110457, 135569]

    if(IS_TEST):
        for uid in range(10000, 10000+num):
            join_in(conn, uid, code)
    else:
        end = min(len(formalUids), num)
        for uid in range(0, end):
            join_in(conn, formalUids[uid], code)


def login():
    pass

# 关闭


def http_common_get(conn, url, dict_params=None):
    # print(conn)

    # dictParams = {'live_id': uid, 'code': code, "os": 1,"from_tid":"14786427"} # 1 android
    # authHead = add_head(dictParams)
    #print("authHead = ",authHead);

    tempHead = dict(HEADERS)  # {}
    # tempHead.update(authHead)
    # print("tempHead = ",tempHead);

    params = ""
    if dict_params:
        params = urllib.parse.urlencode(dict_params)
    # print(params)

    data = ""
    ok = True
    try:
        conn.request(method="GET", url=url+"?"+params,
                     body=None, headers=tempHead)
        response = conn.getresponse()
        data = response.read()
        print(response.status, response.reason, sep=';')  # 指定分隔符
    except Exception as e:
        print(str(e))
        ok = False
    else:
        pass
    finally:
        return data, ok


def http_common_post(conn, url, dict_params=None):
    # print(conn)

    # dictParams = {'live_id': uid, 'code': code, "os": 1,"from_tid":"14786427"} # 1 android
    # authHead = add_head(dictParams)
    #print("authHead = ",authHead);

    tempHead = dict(HEADERS)  # {}
    # tempHead.update(authHead)
    print("tempHead = ", tempHead)

    params = ""
    if dict_params:
        params = urllib.parse.urlencode(dict_params)
    print(params)

    data = ""
    ok = True
    try:
        conn.request(method="POST", url=url, body=params, headers=tempHead)
        response = conn.getresponse()
        data = response.read()
        print(response.status, response.reason, sep=';')  # 指定分隔符
    except Exception as e:
        print(str(e))
        ok = False
    else:
        pass
    finally:
        return data, ok


def http_test1(url):
    # url = 'http://122.152.211.208:9720/close?live_uid=2016255'
    f = urllib.request.urlopen(url)
    print(f.read().decode('utf-8'))


if __name__ == '__main__':

    import sys
    print("len(sys.argv) = ", len(sys.argv))
    for i, s in enumerate(sys.argv):
        print("sys.argv["+str(i)+"] =", s)

    # 正式测试的开关 --------------------------------------------------------------------------------------------------------------------------------
    IS_TEST = True

    '''
	请求域名的HttpConnection方法
	'''
    # h1 = http.client.HTTPConnection('www.python.org')    #指定域名
    # h2 = http.client.HTTPConnection('www.python.org:80') #指定域名，端口
    # h3 = http.client.HTTPConnection('www.python.org', 80) #指定域名，端口
    # h4 = http.client.HTTPConnection('www.python.org', 80, timeout=10) #指定域名，端口，超时时间
    url = ""
    if(IS_TEST):
        url = "10.200.1.203:8010"
    else:
        url = "api.sociapoker.com"
    conn = http.client.HTTPConnection(url)

    # 比赛报名
    # 批量报名
    # check_in_number(conn,10,613654)
    # 单独报名
    # check_in(conn,20000,115656)

    # 普通加入
    # join_in_number(conn,10,819798100023);

    # print(http_common("www.baidu.com","",{}).decode("utf_8"))
    # return
    # 关闭所有房间
    conn = http.client.HTTPConnection("122.152.211.208:9720")
    jonStr, ok = http_common_get(conn, "/get_list")  # .decode("utf_8")
    if ok:
        # print(jonStr)
        jsonObj = json.loads(jonStr)
        jsonList = jsonObj["list"]

        for i in range(len(jsonList)):  # len(jsonList)
            # print(i,jsonList[i])
            user = jsonList[i]
            # print(user)
            dictParams = {'live_uid': user["uid"]}

            # print(dictParams)
            # http:// python前面不用加http://
            print(http_common_get(conn, "/close", dictParams))

    # dictParams = {"live_uid":'1000'}
    # print(http_common_get(conn,"/close",dictParams))

    # http_test1()
