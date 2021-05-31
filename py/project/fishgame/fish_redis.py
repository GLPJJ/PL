# pip install redis
import redis
import pymysql
import re
import threading
# import readline

class AsyncWorkSql(threading.Thread):
    count = 0
    # lock = threading.RLock()  # 折返锁，同一线程可锁定多次

    def __init__(self,id,host,port,pwd,path):
        threading.Thread.__init__(self)

        self.threadId = id
        self.pwd = pwd
        self.path = path
        self.host = host
        self.port = port
        # self.lock1 = threading.Lock()
        # print(self.lock, self.lock1)

    # 重载run函数
    def run(self):
        excuteSql(self.host,self.port,self.pwd,self.path,self.threadId)


def excuteSql(host,port,pwd,file,cnt):
    print("pwd=",pwd,"file=",file)
    connection = pymysql.connect(host=host,port=port,
                                     user="root",
                                     password=pwd,
                                     db="Buyu",
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
    # print(connection)

    # use cursor()
    cursor = connection.cursor()
    cur = 0
    with open(file,"rb") as sqls:
        for sql in sqls:
            sql = sql.decode("utf-8")
            cur = cur + 1
            if cur % cnt != 0:
                continue
            if sql != '':
                print("id="+str(cnt)+" sql="+sql)
                try:
                    cursor.execute(sql)
                    connection.commit() # 提交到数据库执行
                except Exception as e:
                    connection.rollback() # 回滚数据 这里不要回滚
                    print("e=",e)
                    pass

    # try:
    #     print(cursor.execute("""insert into Buyu.sub_act_cfg (activity_id, sub_id, level, total_cnt, sub_title, sub_content) VALUE (4, 1, 5, 6380, '', '');"""))

    #     connection.commit() # 提交到数据库执行
    #     result = cursor.fetchone()
    #     print("result=",result)
    # except Exception as e:
    #     connection.rollback() # 回滚数据
    #     print("e=",e)
    #     pass
    connection.close()
    

def resetUsrCard(uid):
    pass


def cleanUsers(pwd, pwd2, start=None, end=None):
    if not start or not end:
        connection = pymysql.connect(host='127.0.0.1',
                                     user="root",
                                     password=pwd,
                                     db="Buyu",
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        # print(connection)

        # use cursor()
        cursor = connection.cursor()

        if not start:
            cursor.execute("select min(uid) as uid from user;")
            vMin = cursor.fetchone()
            start = vMin["uid"]

        if not end:
            cursor.execute("select max(uid) as uid from user;")
            vMax = cursor.fetchone()
            end = vMax["uid"]
        connection.close()

    r = redis.Redis(host='127.0.0.1', port=6379, db=0, password=pwd2)
    # print(dir(r))
    for i in range(start, end):
        print("del usr_"+str(i), r.delete("usr_"+str(i)))
        r.delete("usrStat_"+str(i))


def cleanUsrByUids(uids, db, pwd, host=None):
    host = host or '127.0.0.1'
    r = redis.Redis(host=host, port=6379, db=db, password=pwd)
    # print(dir(r))

    for i in range(len(uids)):
        uid = uids[i]
        print("del usr_"+str(uid), r.delete("usr_"+str(uid)))


def cleanUsrAndStat(pwd, db, pattern=None, host=None):
    host = host or '127.0.0.1'
    r = redis.Redis(host=host, port=6379, db=db, password=pwd)
    # print(dir(r))

    keys = r.keys()
    for i in range(len(keys)):
        theKey = (keys[i]).decode("utf-8")  # byte -> str
        # print("key=", theKey)
        if not pattern:
            print("del "+theKey, r.delete(theKey))
        elif pattern.match(theKey):
            print("del "+theKey, r.delete(theKey))


def testRedis():
    r = redis.Redis(host='121.196.203.52', port=6379, db=0, password=redisPwd)
    token = "bfb38d68b426b5cb96cd5d8f44aed117"
    print(r.exists(token))
    print(r.get(token))
    print(r.get("token_188787"))
    print(r.keys())


if __name__ == '__main__':
    print("清理redis 测试服缓存...")
    # 启动redis
    # ./src/redis-server ../redis.conf

    mySqlPwd1 = ""
    mySqlPwd2 = ""
    redisPwd = ""
    with open("mysqlpwd.txt", "r") as f:
        mySqlPwd1 = f.readline()[:-1]
        mySqlPwd2 = f.readline()[:-1]
        redisPwd = f.readline()
    print(mySqlPwd1, mySqlPwd2, redisPwd)

    filePathFmt = 'D:\\work\\Github\\GoTest\\sql\\temp.sql'

    # D:\work\Github\fishing_server\sql_production\捕鱼3\Buyu_user_value_props_log.sql
    # excuteSql(mySqlPwd1,filePath)

    # excuteSql("121.196.203.52",3306,mySqlPwd2,filePathFmt,0)
    # workers = []
    # for i in range(1,10):
    #     worker = AsyncWorkSql(i,"121.196.203.52",3306,mySqlPwd2,filePathFmt)
    #     workers.append(worker)
    #     worker.start()

    # for i in range(1,10):
    #     workers[i-1].join()
    # testRedis()
    #废弃了。。。
    # cleanUsers(mySqlPwd1,redisPwd) #清除所有人的redis缓存，慎用 -这个方法最low，从数据获取到uid最大的

    # *匹配0次多次 +匹配一次多次 ?匹配0次1次(非贪婪)
    # \d 匹配所有数字 \D匹配任意非数字 ^匹配开头 $匹配末尾 \w匹配字母数字下划线 \W	匹配非字母数字及下划线
    pattern = None  # 这样会清理redis中所有的缓存信息
    # 下面两个很少会用
    # pattern = re.compile("^token_\\d+")#只匹配Token信息 ->建议还是用r比较方便，不然要写很多的\转义符
    # pattern = re.compile(r"^WX_\d+")#只匹配WX认证信息 ->建议还是用r比较方便，不然要写很多的\转义符

    # pattern = re.compile(r"^usr_checkin_\d+")#只匹配用户签到信息
    # pattern = re.compile(r"^usr_checkin7_\d+")#只匹配用户7日签到信息
    # pattern = re.compile(r"^usr_\d+")#只匹配用户信息
    # pattern = re.compile(r"^usr_today_\d+")#只匹配用户今日信息
    # pattern = re.compile(r"^usr_today_m_\d+")#只匹配用户今日更多信息

    # #\s 匹配所有空白字符=[\t\n\r\f]， \S 匹配所有非空白字符
    # pattern = re.compile(r"^usr_today_\S+")#匹配用户的所有今日信息，
    # pattern = re.compile(r"^usr_\S+")#匹配用户的所有信息，，在线列表的redis名字后面要换一下。。
    # pattern = re.compile(r"^usr_101\S+") #1014匹配 uid为1013打头的用户
    # pattern = re.compile(r"^usr_104\S+") #1014匹配 uid为1013打头的用户

    # if pattern:
    #   print("match=",pattern.match("usr_checkin7_165272"))
    # pattern = re.compile(r"usr_160027")
    # pattern = re.compile(r"usr_6303\S+")
    print("pattern=", pattern)
    number = 1#int(input("\n请确认pattern是否正确,输入(1执行|0退出)："))
    if number == 1:
        # host = "121.196.203.52" #测试1服
        host = "121.43.136.149" #测试极速
        # host = "127.0.0.1"
        #捕鱼使用0
        #修仙使用1
        cleanUsrAndStat(redisPwd, 0, pattern, host)  # 清除所有的redis缓存，慎用
