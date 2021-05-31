#!python3.6
# @ guliping
# 模块事例

# 公开函数


def a():
    print("call function a")

# 私有函数


def __b():
    print("call function b")


# 公开变量
c = 10

# 私有变量
__d = 20

if __name__ == '__main__':
    print("自主运行")
else:
    print("包引入")
