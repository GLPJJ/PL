import codecs
# Http 模块
import http.client
import urllib.parse
# json解析模块
import json
import gzip
import time

def get_from_html():
    # "Accept": "text/html"
    # "Accept-Encoding":"utf-8"
    headers = {"Content-type": "application/x-www-form-urlencoded", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
    "Accept-Encoding": "gzip", 'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9', "cache-control": "max-age=0",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    # https://jordan.tmall.com/p/rd750210.htm?spm=a1z10.1-b-s.w5003-18734961396.4.6abd54e18JeQjz&scene=taobao_shop
    # https://www.fanyu123.cn/fanyu-portal/user/getActivityReward?uid=199620&type=2&changeType=1
    conn = http.client.HTTPSConnection("www.fanyu123.cn")
    # cj.add_cookie_header()
    conn.request("GET", "/fanyu-portal/user/getActivityReward?uid=199620&type=2&changeType=1", None, headers)
    response = conn.getresponse()
    # print(response.status, response.reason)

    data = ""  # response.read()
    # print("info=",response.info())
    # print("info end")
    if response.info().get('Content-Encoding') == 'gzip':
        print("gziped")
        data = gzip.decompress(response.read()).decode("utf-8")
    else:
        data = response.read().decode("utf-8")


    now = time.localtime()
    print(time.strftime("%Y-%m-%d %H:%M:%S", now),time.time(),"result=",data);
    

if __name__ == '__main__':
    for i in range(1):
        print("test ",i)
        # main_test_fish_bug()
        get_from_html()