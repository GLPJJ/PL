#! python3.4
# @ guliping

# Http 模块
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
# json解析模块
import json

#HEADERS = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
HEADERS = {"Content-type": "application/json", "Accept": "text/plain"}

# 启动钉钉通知消息


def ding_text(token, content, numbers, is_all):
    """
    token：Token令牌
    content：通知内容
    numbers：通知列表
    is_all：是否全员通知
    """
    # https://oapi.dingtalk.com/robot/send?access_token=75dc4036476a829d8d4bcfefcc674310c7c1cd3ee373c9851ad64e0f184b2494

    print("ding_text")
    conn = http.client.HTTPSConnection("oapi.dingtalk.com")
    print(conn)

    tempHead = dict(HEADERS)
    #print("tempHead = ",tempHead);

    params_content = {"content": content}
    print(params_content)

    params_at = {"atMobiles": numbers, "isAtAll": is_all}
    print(params_at)
    dictParams = {'msgtype': 'text', "text": params_content, "at": params_at}
    print(dictParams)

    json_params = json.dumps(dictParams)
    print(json_params)

    # params =  urllib.parse.urlencode(dictParams)
    # print(params)

    try:
        conn.request("POST", "/robot/send?access_token="
                     + token, json_params, tempHead)

        response = conn.getresponse()
        data = response.read()

        # print(type(data))
        print(response.status, response.reason,
              data.decode(), sep=' ; ')  # 指定分隔符
    except Exception as e:
        print(str(e))
    else:
        pass
    finally:
        pass


if __name__ == '__main__':
    # main()
    numbers = ["15088603329"]

    # 查看系统运行状态 pip install psutil
    # https://pypi.python.org/pypi/psutil
    # import psutil
    # print(psutil.cpu_percent())  # 查看CPU
    # print("*"*60)
    # vm = psutil.virtual_memory()
    # print(type(vm), vm)
    # print("*"*60)
    # print(vm.total, vm.available, vm.percent)  # 查看虚拟内存
    # print("*"*60)
    # print(psutil.disk_partitions())  # 查看硬盘分区
    # print("*"*60)
    # print(psutil.disk_usage('/'))  # 查看硬盘使用
    # print("*"*60)
    # print(psutil.net_io_counters(pernic=True))  # 查看网络链接
    # print(psutil.net_connections()) #查看网络连接

    """
	Token令牌
	通知内容
	通知列表
	是否全员通知
	"""
    # ding_text("75dc4036476a829d8d4bcfefcc674310c7c1cd3ee373c9851ad64e0f184b2494",
    #           "Hello World", numbers, False)

    #https://oapi.dingtalk.com/robot/send?access_token=761dd7ffb3ce446f9bebb24b002a5581a41af0a0d7644cf4196f6a5d8b2efdde
    ding_text("761dd7ffb3ce446f9bebb24b002a5581a41af0a0d7644cf4196f6a5d8b2efdde",
              "Hello World", numbers, False)
