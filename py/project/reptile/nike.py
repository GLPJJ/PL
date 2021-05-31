
from bs4 import BeautifulSoup
import http.cookiejar
import urllib.request
import http.client
import urllib.parse

import gzip
#import numpy
import pandas

def get_from_html():
	# "Accept": "text/html"
	# "Accept-Encoding":"utf-8"
	headers = {"Content-type": "application/x-www-form-urlencoded", 
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", 
	"Accept-Encoding": "gzip", 'Connection': 'keep-alive',
	'Accept-Language': 'zh-CN,zh;q=0.9', "cache-control": "max-age=0",
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
	# https://jordan.tmall.com/p/rd750210.htm?spm=a1z10.1-b-s.w5003-18734961396.4.6abd54e18JeQjz&scene=taobao_shop
	conn = http.client.HTTPSConnection("jordan.tmall.com")
	# cj.add_cookie_header()
	conn.request("GET", "/p/rd750210.htm?spm=a1z10.1-b-s.w5003-18734961396.4.6abd54e18JeQjz&scene=taobao_shop", None, headers)
	response = conn.getresponse()
	print(response.status, response.reason)

	data = ""  # response.read()
	print("info=",response.info())
	if response.info().get('Content-Encoding') == 'gzip':
		data = gzip.decompress(response.read()).decode("utf-8")
	else:
		data = response.read().decode("utf-8")

	print("data=",data);
	# print(data.decode('utf-8'))
	return
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

def get_jordan(opener,cj,cookie_str):
	print("*"*100,"[jordan]")
	jordanUrl = 'https://jordan.tmall.com/'
	postdata = urllib.parse.urlencode({
		'cookie': cookie_str, 
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	}).encode('utf-8')
	result = opener.open(jordanUrl, postdata)
	print("*"*100,"status")
	print(result.status, result.reason, type(result))#, dir(result))
	cj.save(ignore_discard=True, ignore_expires=True)
	# print("*"*100,"headers")
	# print(result.headers)
	print("*"*100,"info")
	print(result.info())
	print("*"*100,"data")
	print(result.read().decode("gbk")) #.decode("utf-8")

def taoba_login(username,password,ua):
	print("*"*100,"[login]")
	# /member/login.jhtml?redirectURL=https%3A%2F%2Fjordan.tmall.com%2Fview_shop.htm
	# 超慢的http访问,登录，记录cookie
	filename = 'cookie.txt'
	# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
	cj = http.cookiejar.MozillaCookieJar(filename)
	handler = urllib.request.HTTPCookieProcessor(cj)
	opener = urllib.request.build_opener(handler)

	postdata = urllib.parse.urlencode({
		'TPL_username': username, 
		'TPL_password_2': password,
		'ua': ua,
		'TPL_password':'', 
		'ncoSig':'', 
		'ncoSessionid':'', 
		'ncoToken': '8ece0a939a683a46f9fefcd3311a841174ef419e',
		'slideCodeShow': False,
		'useMobile': False,
		'lang': 'zh_CN',
		'loginsite': 0,
		'newlogin': 0,
		# 'TPL_redirect_url': 'https://www.tmall.com/',
		'from': 'tmall',
		'fc': 'default',
		'style': 'miniall',
		'css_style': '',
		'keyLogin': False,
		'qrLogin': True,
		'newMini': False,
		'newMini2': True,
		'tid': '',
		'loginType': 3,
		'minititle': '',
		'minipara': '',
		'pstrong': '',
		'sign': '',
		'need_sign': '',
		'isIgnore': '',
		'full_redirect': True,
		'sub_jump': '',
		'popid': '',
		'callback': '',
		'guf':'' ,
		'not_duplite_str':'' ,
		'need_user_id':'' ,
		'poy': '',
		'gvfdcname': 10,
		'gvfdcre': '68747470733A2F2F6C6F67696E2E746D616C6C2E636F6D2F3F73706D3D3837352E373933313833362F422E61323232366D7A2E312E363631343432363573673370304D26726564697265637455524C3D68747470732533412532462532467777772E746D616C6C2E636F6D253246',
		'from_encoding': '',
		'sub': True,
		'loginASR': 1,
		'loginASRSuc': 1,
		'allp': 'assets_css=3.0.10/login_pc.css',
		'oslanguage': 'zh-CN',
		'sr': '1920*1080',
		'osVer': '',
		'naviVer': 'chrome|68.03440106',
		'osACN': 'Mozilla',
		'osAV': '5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
		'osPF': 'Win32',
		'miserHardInfo':'', 
		'appkey': '00000000',
		'nickLoginLink': '',
		# 'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?tpl_redirect_url=https://www.tmall.com/&style=miniall&enup=true&newMini2=true&full_redirect=true&sub=true&from=tmall&allp=assets_css=3.0.10/login_pc.css&pms=1552376957081&useMobile=true',
		'showAssistantLink': '',
		'um_token': 'HV02PAAZ0b0f55d97ae27bde5c87647e00b54d99999999',
	}).encode('utf-8')
	# 登录的URL
	loginUrl = 'https://login.taobao.com/member/login.jhtml'
	# 模拟登录，并把cookie保存到变量
	result = opener.open(loginUrl, postdata)
	print("*"*100,"status")
	print(result.status, result.reason, type(result)) #,dir(result))
	cj.save(ignore_discard=True, ignore_expires=True)
	# print("*"*100,"headers")
	# print(result.headers)
	print("*"*100,"info")
	print(result.info())
	print("*"*100,"data")
	print(result.read().decode("gbk")) #.decode("utf-8")

	cookie_str = ""
	for item in cj:
		print("[cookie]",item.name,item.value);
		cookie_str += item.name+"="+item.value+";"

	# get_from_html()
	get_jordan(opener,cj,cookie_str)


def nick_main():
	print("爬取开始")

	print("爬取【天猫Jordan官网】...")
	try:
		get_from_html()
	except Exception as e:
		print("Exception=",e)
		print("爬取【天猫Jordan官网】结果:异常")
	else:
		print("爬取【天猫Jordan官网】结果:正常")
	finally:
		print("爬取【天猫Jordan官网】结束")


if __name__ == '__main__':
	# nick_main()

	# # www.tmall.com
	# # https://jordan.tmall.com/view_shop.htm?spm=a220m.1000858.0.0.688170c6cMIhxm&shop_id=350171485&rn=b81727dabe6a3bf724b2fd4090fc6a66
	conn = http.client.HTTPSConnection("jordan.tmall.com")
	# cj.add_cookie_header()
	headers = {}

	conn.request("GET", "/view_shop.htm", None, headers)
	response = conn.getresponse()
	print("*"*50+"status"+"*"*50)
	print(response.status, response.reason)
	print("*"*50+"info"+"*"*50)
	print(response.info())
	data = response.read()
	print("*"*50+"data"+"*"*50)
	print(data.decode("utf-8"))

	# taoba_login('glp4703','4488d9ae53982c895d5b78292465f29043421f2e4c91b31c156582b4701bbcf14304cb1058ba81a01c58f2bd9ac115e694dc6e679ecfe36a2b795e0b678a0a62ec924bb4d7faa956bf05c07cdc6670c53ed3dbe63f9c28f2e26d0f4ba9a1c2f799e274d530b93ff8bdeec4a09aa458ba00a695673f4c0472b364a7fd0b31c4f3',
	# 	'115#1+Tn711O1TaLSUX0GCFY1CsoE51GBaVN1g4H5sDTr5SlVywCfxaW6njrf91CIkf6web8s9ZcvLTgyUFP8HNcaB6fy5XQmMpWSzL8aw+Qi/JJhUeh3uPc28MfcUUjxsbGeK/0zkaJi7Schae8Aka4aTKbyzemASbneK1rsMZQi/y8h6/4OWNDaTpvs6/nbWnkeKT8yWKpiQJRHZzhb2GVaLBfDzFQOSfkeKT8uWNIi/JJhUU4AWwwaTpfurPKvAGK+JDloRbug7Dv6VXgdPYMTNTW6Cko1vZItDvE8c5df+h+pVM+3UZ83gIuYZO5NZ/lF3lOdXSm2O5bGaNrRKUnSnPHrxNJ0O4/JN7slRAl8ZKctssmKg3r7utd2H+kmBp4lAY6BMU5JgdxUtyapuKy66e15WwKmrP6gOtxQPzJC9JUAzHG/ywk7hOwO7Uv8edz66LTb+blbtMw9QktWDS4m5feQOzB5lfn0oCC7u/s0QK4ZyJeHQof6krMqXL/lO/ZXAV46wlAEM4PERYnBtU+m3N2xVzFu/owg2jZfwHbS7Tx2wWXwiD7t+TDKrsRD/QddGtW8zXC+iMikRLgF89AOV8bS7gJV70Z1EyzZNlZ0UGYerZfutB8aDnQTv6fyDDqbMYjf98TTwhinWB9VrRWOoRf9GMUPsrbr4LKXiQhqF+mf10ggqe1E5+mwyIcc4Teg3GdhTWwwJfEI5yMPEUPdrtIYV+wOZNWWTXY1Rs5/TAWJDuCtqevpguQwpLEyd/BoV9TBoAAwSMRXn5EsnlN3sddOHrrtBjDUcCA1CaH+970wd97ujp215gaZGyeTwGP8HGeoWuRWHmCJtJ+PBsR9lDYqVK1G5Fm6nYuYIcAcsQLyY4mVCqQl0e0kaPqN31e9ZEYiOOoUmQCWdKUznme/SVOZNSMl2Zka1IqcfamiVu2jmenbeMPhKffMq4gBGUp/e769phU1BdgrR7IJE2oBaUJb19hfjt8r5PJiNdD83nVxUhU7IlH0RzgK+CGRrfQKRVexU1LqBndJGH59/ifSJ3vvUBvlc9PTDmrizmthvrAiQ/b8XoY5LWJ1GejOcyDrnvotjoGpEFFxx2+SPYgkOMMMfT4OGcP/W41K7gj1bv2jeQIqGKpiwdmBzQWyvkavB6YlvIKhW5E9rCu75==')


