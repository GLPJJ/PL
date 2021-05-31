#!python3.6
# @ guliping

# 多线程 python
import threading
import time
import random

# 卖票提供两个窗口
count = 10000

class AsyncWork(threading.Thread):
    count = 0
    lock = threading.RLock()  # 折返锁，同一线程可锁定多次

    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id
        self.lock1 = threading.Lock()

        print(self.lock, self.lock1)

    # 重载run函数
    def run(self):
        while True:
            # time.sleep(random.random()*2)

            global count
            with self.lock:
                if(count <= 0):
                    break

                count -= 1
                print("count=", count, "I'm thread ", self.id)


# 创建多线程实例
aw1 = AsyncWork(1)
aw2 = AsyncWork(2)

# 开启多线程
aw1.start()
aw2.start()
print('The main program continues to run in foreground.')

# 等待多线程结束
aw1.join()  # Wait for the background task to finish
aw2.join()
print('Main program waited until background was done.')

# 结束。。。
