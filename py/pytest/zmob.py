#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python 2.7
# MOB 短信请求byhttp

"""
请求发起短信请求

请求地址: https://webapi.sms.mob.com/sms/sendmsg

请求方式: POST

请求参数

参数名	参数类型	描述	是否必填
appkey	string	应用appkey	必填
phone	string	电话号码	必填(不带区号电话号码 13121222212)
zone	string	区号	必填(区号86)
返回结果

{status:200}
附录

错误编码

返回值	错误描述
200	发送或校验验证码成功
405	请求参数中的appkey为空
406	非法的appkey
456	请求参数中的手机号码或者国家代码为空
457	手机号码格式错误
458	AppKey或手机号码在黑名单中
460	未开启发送短信功能，请联系我们
462	应用下同一手机号1分钟内发送短信的次数超过2次
463	手机号码超出当天发送短信的限额
467	请求校验验证码频繁（5分钟校验超过3次）
468	用户提交校验的验证码错误
469	没有打开发送Http-api的开关
470	账户短信余额不足
471	请求ip和绑定ip不符
475	应用信息不存在，检查appKey是否低于2.0版本
477	当前手机号码在SMSSDK平台内每天最多可发送短信10条，包括客户端发送和WebApi发送
478	当前手机号码在当前应用下12小时内最多可发送文本验证码5条.
"""


import urllib
import urllib2
import json


class MobSMS:
    def __init__(self, appkey):
        self.appkey = appkey
        self.url = 'https://webapi.sms.mob.com/sms/sendmsg'

    def verify_sms_code(self, zone, phone, debug=False):
        if debug:
            return 200

        data = {'appkey': self.appkey, 'zone': zone, 'phone': phone}
        data = urllib.urlencode(data)
        req = urllib2.Request(self.url, data)
        o = urllib2.urlopen(req)
        if o.getcode() == 200:
            j = json.loads(o.read())
            return j.get("status")
        return 500


if __name__ == '__main__':
    mobsms = MobSMS('1eb63d197f5c7')

    # print mobsms.verify_sms_code(86, 15000003329)
