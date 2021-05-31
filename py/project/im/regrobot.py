import codecs
# Http 模块
import http.client
import urllib.parse
# json解析模块
import json

HEADERS = {"Content-Type": "application/json", "Accept": "text/plain"}


def regrobot(uid, avatar, name, level):
    robot = {"uid": uid, "user": {"uid": uid, "avatar": avatar,
                                  "nickname": name, "role_id": 0, "level": level}}
    print(robot)
    # return

    try:
        print("regrobot")
        # https 本地地址
        # conn = http.client.HTTPSConnection("192.168.0.120:9191")
        # 本地地址
        # conn = http.client.HTTPConnection("192.168.0.120:9191")
        # 正式服地址
        conn = http.client.HTTPConnection("34.199.120.59:9191")
        print(conn)

        tempHead = dict(HEADERS)

        json_params = json.dumps(robot)
        # print(json_params)
        conn.request("POST", "/add_user?debug=1&live_uid=1000&uuid=" +
                     str(robot["uid"]), json_params, tempHead)
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


def unregrobt(uid):
    try:
        print("unregrobt")
        # https 本地地址
        # conn = http.client.HTTPSConnection("192.168.0.120:9191")
        # 本地地址
        # conn = http.client.HTTPConnection("192.168.0.120:9191")
        # 正式服地址
        conn = http.client.HTTPConnection("34.199.120.59:9191")
        print(conn)

        tempHead = dict(HEADERS)

        # print(json_params)
        conn.request(
            "POST", "/del_user?debug=1&live_uid=1000&uuid="+str(uid), {}, tempHead)
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

# 读取带BOM的utf8文件


def regrobots(file, reg):
    with open(file, "r", encoding="utf-8-sig") as f:
        for line in f:
            # print(line)
            if line != "\n":
                items = line.split(" ")
                print(items)

                if reg:
                    regrobot(int(items[0]), items[1], items[2], int(items[3]))
                else:
                    unregrobt(int(items[0]))
            # break


if __name__ == '__main__':
    # regrobots("D:/glp/Github/PL/py/ztest/im/user.txt",True)
    regrobots("D:/glp/Github/PL/py/ztest/im/user.txt", False)

    # regrobot(1000000,"http://robot-1253351729.costj.myqcloud.com/1.jpg","Aaron",1)
