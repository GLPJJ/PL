#!python3.4
# @ guliping

"""
网络爬虫

Beautifulsoup + request，urllib 编写的小巧爬虫 没有采用scrapy框架
"""

# pip install beautifulsoup4
from bs4 import BeautifulSoup
import http.cookiejar
import urllib.request
import http.client
import urllib.parse

import gzip
#import numpy
import pandas


def get_from_caipiaokong():
    # 超慢的http访问,登录，记录cookie
    filename = 'cookie.txt'
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cj = http.cookiejar.MozillaCookieJar(filename)
    handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(handler)

    postdata = urllib.parse.urlencode({'username': 'jjhhh', 'password': 'e10adc3949ba59abbe56e057f20f883e', 'questionid': 0, 'answer': ''}
                                      ).encode('utf-8')
    # 登录的URL
    loginUrl = 'https://www.caipiaokong.com//member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes'
    # 模拟登录，并把cookie保存到变量
    result = opener.open(loginUrl, postdata)
    print(result.status, result.reason, type(result))
    # print(result.read().decode('utf-8'))
    # 保存cookie到cookie.txt中
    #cj.save(ignore_discard=True, ignore_expires=True)

    # print(cj)
    cookie_str = ""
    for item in cj:
        # print(item.name,item.value);
        cookie_str += item.name+"="+item.value+";"
    cookie_str = cookie_str[:-2]
    # print(cookie_str)
    # #利用cookie请求访问另一个网址，此网址是查询网址
    # gradeUrl = 'https://www.caipiaokong.com/lottery/bjklb.html'
    # # #请求访问查询网址
    # result = opener.open(gradeUrl)
    # print(result.status, result.reason,type(result))
    # #print(result.read().decode('utf-8'))

    # http 登录
    # params = urllib.parse.urlencode({'username':'jjhhh','password':'e10adc3949ba59abbe56e057f20f883e','questionid':0,'answer':''})
    # headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","Accept-Encoding":"utf-8"}
    # conn = http.client.HTTPSConnection("www.caipiaokong.com")
    # conn.request("POST", "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes", params, headers)
    # response = conn.getresponse()
    # print(response.status, response.reason)
    # data = response.read()
    # # print(data.decode('utf-8'))
    # conn.close()

    # http 查询
    params = urllib.parse.urlencode(
        {'username': 'jjhhh', 'password': 'e10adc3949ba59abbe56e057f20f883e', 'questionid': 0, 'answer': ''})
    # "Accept": "text/html"
    # "Accept-Encoding":"utf-8"
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Accept-Encoding": "gzip", 'Cookie': cookie_str, 'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    conn = http.client.HTTPSConnection("www.caipiaokong.com")
    # cj.add_cookie_header()
    conn.request("POST", "/lottery/bjklb.html", None, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = ""  # response.read()
    if response.info().get('Content-Encoding') == 'gzip':
        data = gzip.decompress(response.read()).decode("utf-8")
    else:
        data = response.read().decode("utf-8")

    # print(data);
    # print(data.decode('utf-8'))
    soup = BeautifulSoup(data, 'html.parser')

    # print(soup)#输出整个doc
    # print(soup.body.div)#输出第一个doc的body的第一个div
    # print(soup.body.contents)#以列表的形式输出内容节点，但是中间会包含 '\n' 卧槽
    # for child in soup.body.children:#遍历所有子节点的另一种方式，同样中间会有 '\n'
    #     print(type(child),child)
    # .descendants 可以遍历所有的子孙（多了孙子）节点
    print("*"*100)
    tag_div_1 = soup.body.contents[13]
    # print(tag_div_1)
    # print("*"*100)
    # print(tag_div_1.contents)
    tag_div_2 = tag_div_1.contents[13]
    # print(type(tag_div_2),tag_div_2.contents)
    tag_table_3 = tag_div_2.contents[1].contents[3].contents[0]
    # print(type(tag_table_3))
    # print(tag_table_3)
    # print("*"*100)
    # print(tag_table_3.contents)

    # 期号需要单独获取一下
    tag_time_index_1 = tag_div_1.contents[15].contents[1].contents[1].contents[3]
    # print(tag_time_index_1)
    # print("*"*100)
    # print(tag_time_index_1.contents)
    index_str = tag_time_index_1.contents[6].string
    index_str_pre = "下期期号：第"
    pos_start = index_str.find(index_str_pre)
    pos_end = index_str.find("期，发行机构")
    index_str = index_str[pos_start+len(index_str_pre):pos_end]
    index_int = int(index_str)-1

    names = []
    df = None

    tag_table_contents = tag_table_3.contents
    for i in range(len(tag_table_contents)):
        cur_tag_tr = tag_table_contents[i]
        if(i == 0):
            for child in cur_tag_tr.children:
                # print("列名称",child.string)
                names.append(child.string)  # 当标签中只有一个string的时候 ： <th>号码</th>
            df = pandas.DataFrame(columns=names)
        else:
            cur_tag_tr_contents = cur_tag_tr.contents
            len_tr = len(cur_tag_tr_contents)
            for j in range(len_tr):
                cur_tag_td_contents = cur_tag_tr_contents[j].contents
                if(j == 0):  # 期数
                    time_index = cur_tag_td_contents[0].string
                    # print(time_index)
                    # df.insert(0,i,time_index)

                    time_index = "第"+str(index_int)+"期"
                    df.set_value(i-1, names[j], time_index)
                    index_int -= 1
                elif(j == 1):
                    tag_strong_contents = cur_tag_td_contents
                    cols = []
                    for k in range(len(tag_strong_contents)):
                        cols.append(tag_strong_contents[k].string)
                    # print("号码",cols)
                    # df.insert(1,i,cols)
                    df.set_value(i-1, names[j], cols)
                elif(j == 2):
                    number = cur_tag_td_contents[0].string
                    # print("飞盘",number)
                    # df.insert(2,i,number)
                    df.set_value(i-1, names[j], number)
                elif(j == 3):
                    time_clock = cur_tag_td_contents[0]['title']
                    # print("时间",time_clock)
                    # df.insert(3,i,time_clock)
                    df.set_value(i-1, names[j], str(time_clock))

    print("*"*100)
    # print(df)
    df.to_csv("快乐8_www.caipiaokong.com.csv")
    conn.close()


def get_from_bjfc():
    conn = http.client.HTTPConnection("www.bwlc.net")
    # cj.add_cookie_header()
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Accept-Encoding": "gzip", 'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    conn.request("GET", None, None, headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    data = ""  # response.read()
    if response.info().get('Content-Encoding') == 'gzip':
        data = gzip.decompress(response.read()).decode("utf-8")
    else:
        data = response.read().decode("utf-8")

    # print(data);
    soup = BeautifulSoup(data, 'html.parser')

    print("*"*100)
    tag_div_1 = soup.body.contents[3]
    # print(tag_div_1)
    # print("*"*100)
    # print(tag_div_1.contents)
    tag_div_2 = tag_div_1.contents[3].contents[10].contents[3].contents[19]
    # print(type(tag_div_2))
    # print(tag_div_2)
    # print("*"*100)
    # print(tag_div_2.contents)

    tag_table_3 = tag_div_2.contents[3]
    # print(type(tag_table_3))
    # print(tag_table_3)
    # print("*"*100)
    # print(tag_table_3.contents)

    time_index = tag_table_3.contents[1].string
    # print(time_index)
    tag_number_1 = tag_table_3.contents[5].contents
    number = []
    # print(tag_number_1[1].contents)
    haoma_lst = tag_number_1[1].find_all("li")  # 查找所有的li节点
    # print(haoma_lst)
    for i in range(len(haoma_lst)):
        number.append(haoma_lst[i].string)
    # print(number)
    fp = tag_number_1[3].contents[0].string[1:]
    # print(fp)
    names = ['期数', '号码', '飞盘']
    df = pandas.DataFrame(columns=names)

    df.set_value(0, names[0], time_index)
    df.set_value(0, names[1], number)
    df.set_value(0, names[2], fp)

    # print("*"*100)
    # print(df)
    df.to_csv("快乐8_www.bwlc.net.csv")
    conn.close()


if __name__ == '__main__':
    print("爬取开始")

    print("爬取彩票控...")
    try:
        get_from_caipiaokong()
    except Exception as e:
        print("Exception=", e)
        print("爬取彩票控结果:异常")
    else:
        print("爬取彩票控结果:正常")
    finally:
        print("爬取彩票控结束")

    try:
        get_from_bjfc()
    except Exception as e:
        print("Exception=", e)
        print("爬取北京福彩结果:异常")
    else:
        print("爬取北京福彩结果:正常")
        pass
    finally:
        print("爬取北京福彩结束")

    print("*"*100)
    print("请查看当前目录的两个csv文件 ！！！")
