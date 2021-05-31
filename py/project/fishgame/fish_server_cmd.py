import platform
import os
# yum install python-devel
# yum install patch
# pip install readline #要使用readline必须安装上面的python开发包
import readline  # 引入该包可以再读取input的时候使用delete

# 测试linux服务器网速
# pip install speedtest-cli
# python3 /usr/local/python3/lib/python3.6/site-packages/speedtest.py

# 更新充值配置
# 通知认证服务器
# curl -i http://127.0.0.1:32767/updateCfg?token=auth_notify
# 更新金币配置
# curl -i http://127.0.0.1:56799/reloadGold
#重新加载活动信息
# curl -i http://127.0.0.1:56799/reloadActivity
# 多个参数同时请求，通知支付成功。
# curl http://127.0.0.1:56799/order?type=15\&sign=0656837dd9c0cf8b7bdaba46af17f84f\&oid=280733

# 服务器切换配置要一致。
PortCfg = 56799
AuthCfg = 6101
FishCrontab = "crontab /opt/py/fish2.crontab"


def fish_server_cmd1():
    os.system("""
crontab -r
echo ****************************定时任务已关闭，请及时开启!!!!!!!!"""+FishCrontab+"""
date
curl -i http://127.0.0.1:"""+str(PortCfg)+"""/stopservice?sign=52a11abea3551c646001ae447329e74c
	""")


def fish_server_cmd2():
    cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/reloadMyCfg"
    print("cmd=", cmd)
    os.system(cmd)


def fish_server_cmd3():
    cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/reloadRoomConfig?type=3"
    print("cmd=", cmd)
    os.system(cmd)


def fish_server_cmd4():
    cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/getData"
    print("cmd=", cmd)
    os.system(cmd)


def fish_server_cmd5():
    print("cmd=", FishCrontab)
    os.system(FishCrontab)


def fish_server_cmd6():
    cmd = "/opt/soft/redis-5.0.3/src/redis-server /opt/soft/redis-5.0.3/redis.conf"
    print("cmd=", cmd)
    os.system(cmd)


def fish_server_cmd7():
    # 使用redis客户端查看服务器，并带上密码
    # /opt/soft/redis-5.0.3/src/redis-cli -a C9BE6E8D-F2CF-4154-BD34-922844BEAC11
    cmd = "/opt/soft/redis-5.0.3/src/redis-cli -a C9BE6E8D-F2CF-4154-BD34-922844BEAC11 shutdown"
    print("cmd=", cmd)
    os.system(cmd)


def fish_server_cmd8():
    cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/reloadUp"
    print("cmd=", cmd)
    os.system(cmd)
    # cmd = "curl -i http://127.0.0.1:56800/reloadUp"
    # print("cmd=",cmd)
    # os.system(cmd)


def fish_server_cmd9():
    cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/stat"
    print("cmd=", cmd)
    os.system(cmd)

#curl -i http://127.0.0.1:56799/snapshot?opt=1
#curl -i http://127.0.0.1:56799/snapshot?opt=1\&a=1 linux终端需要转义&
def fish_server_cmd10():
    cmd = "curl -i http://127.0.0.1:"+str(PortCfg)+"/snapshot"
    print("cmd=", cmd)
    os.system(cmd)

# curl -i http://127.0.0.1:6101/listProxy


def fish_server_cmd11():
    cmd = "curl -i http://127.0.0.1:"+str(AuthCfg)+"/listProxy"
    print("cmd=", cmd)
    os.system(cmd)


def fish_server_cmd12(port):
    if port == 56799:
        pass
    elif port == 56800:
        pass
    else:
        print("Port Error:", port)


def fish_server_cmd():
    strHelp = """
捕鱼命令行,选择号码并回车：
	0.退出
	1.停服
	2.更新MyConf配置信息 curl -i http://127.0.0.1:"""+str(PortCfg)+"""/reloadMyCfg
	3.更新房间配置 curl -i http://127.0.0.1:"""+str(PortCfg)+"""/reloadRoomConfig?type=3
	4.查看当前在线人数 curl -i http://127.0.0.1:"""+str(PortCfg)+"""/getData
	5.启用定时检查任务crontab
	6.开启redis
	7.关闭redis
	8.通知服务器充值配置变更
	9.查看当前服务器的STAT
	10.查看当前服务器的内存快照SNAPSHOT
	11.查看当前认证服务器的代理,curl -i http://127.0.0.1:"""+str(AuthCfg)+"""/listProxy
		curl -i http://127.0.0.1:"""+str(AuthCfg)+"""/removeProxy?ip=??
	12.服务器热切换，输入想要切换的端口地址(56799/56800)
"""
    print(strHelp)
    while(True):
        if "Windows" == platform.system():
            print("windows 不支持")
            break

        number = int(input("\n请输入："))
        print("number=", number)

        if number == 0:
            print("再见")
            break
        elif number == 1:
            number2 = int(input("\n确实要停止服务器吗?："))
            if number2 == 1:
                fish_server_cmd1()
            break
        elif number == 2:
            fish_server_cmd2()
        elif number == 3:
            fish_server_cmd3()
        elif number == 4:
            fish_server_cmd4()
        elif number == 5:
            fish_server_cmd5()
        elif number == 6:
            fish_server_cmd6()
        elif number == 7:
            fish_server_cmd7()
        elif number == 8:
            fish_server_cmd8()
        elif number == 9:
            fish_server_cmd9()
        elif number == 10:
            fish_server_cmd10()
        elif number == 11:
            fish_server_cmd11()
        elif number == 12:
            prot = int(input("\n切换的服务器端口地址(56799/56800)?："))
            fish_server_cmd12(prot)
        else:
            print(strHelp)


if __name__ == '__main__':
    fish_server_cmd()
