#!python3.6
# @ guliping

import selectors
import socket
import sys
import time
import threading

def test():
    try:
        sock = socket.socket()
        # sock.setblocking(False)
        # sel.register(sock, selectors.EVENT_READ, accept)
        print("connect..",id(sock))
        sock.connect(("127.0.0.1",9999))
        # print("send..")
        sock.send(b"ls\n")
        # print("sleep..")
        time.sleep(0.01)
        # print("close..")
        sock.close()
    except Exception as e:
        print(e)


class AsyncWork(threading.Thread):
    count = 0
    # lock = threading.RLock()  # 折返锁，同一线程可锁定多次

    def __init__(self,do,threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.do = do

    # 重载run函数
    def run(self):
        self.do(self.threadID)
    
if __name__ == '__main__':
    for i in range(200000):
        print(i)
        test()

    # def do(threadID):
    #     for i in range(1000):
    #         print(threadID,i)
    #         test()

    # limit = 1000
    # aws = []
    # for i in range(limit):
    #     aws.append(AsyncWork(do,i))

    # for i in range(limit):
    #     aws[i].start()

    # for i in range(limit):
    #     aws[i].join()
