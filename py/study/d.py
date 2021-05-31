#!python3.4
# @ guliping

import time
import datetime
import sys
'''
python 数据类型详解

@注意：函数+变量引用的测试
'''


# 字符串
print("\n\n"+"*"*15+"字符串"+"*"*15)
s = "hello world"
s1 = 'hello world'  # go语言不能使用单引号表示字符串，单引号只能表示某个字符
s2 = """hello
    world"""
print(s, s1, s2)
print("repr=", repr(s2))
print("字符串拼接:" + str(123))
print("*"*30)

# python 对字符串的访问支持正负索引
s3 = s[:]  # 字符串拷贝出来的地址 python一样，go不一样
print(s3, id(s), id(s3), s == s3, id(s) == id(s3))
print(s[1:])  # python 的所有索引起点都是0 区别于lua的从1开始的索引
print(s[1:4])  # 前闭后开区间
print(s[3:2])  # 无输出
print(s[-5:-2])  # 前闭后开区间 ->Wor
print("长度=", len(s))  # 查看字符串长度
print("一个英文长度为1，utf8中文是1，长度=", len(s), len("中"), len("中文"))  # 查看字符串长度

print("字符串复制", "*"*30)
# python 3 不同于 python2的%表示法 ，都用大括号表示占位，并且支持索引和关键字，跟c的printf相比只是多了{:},不用写%了
print("字符串格式化", "the first code is {0} {1:02d} {jack}".format(
    s, 1, jack="jack son"))
print("字符串成员运算符in,Hello 是否存在", "Hello" in s)
print("字符串成员运算符not in,Hello 是否不存在", "Hello" not in s)
print("原始字符串", r"Hello\n", R"World\n")
print("字符串全部转为大写字母", s.upper())
print("字符串全部转为小写字母", s.lower())
print("首字母大写", s.capitalize())     # 把第一个字母转化为大写字母，其余小写
print("每个单词首字母大写", s.title())          # 把每个单词的第一个字母转化为大写，其余小写
print("字符串查找find=", s.find("l", 4))  # 4指定起始位置 返回在字符串中的开始位置 找不到返回-1
print("字符串查找find2=", s.find("l", 4,9))  # 4指定起始位置 6指定结束为止 前闭后开区间。返回在字符串中的开始位置 找不到返回-1
print("字符串查找rfind=", s.rfind("l", 4,6))  # 4指定起始位置 返回在字符串中的开始位置 找不到返回-1
#rfind 查找指定的位置跟find的用法保持一致
# 相比于find ，index方法找不到时会报错 还有从右边找的 rfind rindex
# print("字符串查找",s.index("lle"))
print("字符串查找替换", s.replace("l", "L", 2))  # 最后一个参数是要替换的次数，不填，默认全部替换
print("字符串查找替换2", s.replace("l", "L"))
print("Trim=" + " ss s1  ".strip(" "))  # 指定忽略字符
print("Trim=" + " ss s1  ".strip())  # 默认忽略空格
# 去除字符串左空格 lstrip ，右空格 rstrip,左右空格strip

ss = ["a", "b", "c"]
ss2 = ss[:]  # 数组拷贝出来的地址 python不一样，go不一样
print(ss2, " ", id(ss), " ", id(ss2), " ", id(ss) == id(ss2))
print("字符串以指定连接符连接", "_".join(ss))
print("字符串以指定字符串分隔", s.split("l"))
print("字符串以换行符分隔", s2.splitlines(True))  # True 保留换行符 ,False 去掉换行符
print("字符串检查指定字符串重复出现次数", s.count("l"))
print("字符串开头检查", s.startswith("Hell"))
print("字符串结束检查", s.endswith("world"))
print("字符串只含数字检查", s.isdigit())
print("字符串只含字母检查", s.isalpha())
print("字符串只含数字或字母", s.isalnum())


# 列表 list python索引从0开始
animal = ["cat", "dog", "fish", "bird"]
for i in range(len(animal)):
    print(animal[i], end=",")
else:
    print()
print("*"*30)
# 不能越界，-5就报错 相对于lua，python对列表也提供负索引访问
for i in range(-4, len(animal)):
    print(animal[i], end=",")
print()

# 多维列表
arras = []
nums = 3
for i in range(nums):
    temp = []
    for j in range(nums):
        vi = i+1
        vj = j+1
        temp.append(vi*vj)
        #print("arras[%d][%d]=%d" % (vi,vj,vi*vj))
    arras.append(temp)

for i in range(nums):
    for j in range(nums):
        print("arras[%d][%d]=%d" % (i, j, arras[i][j]))

print("*"*30)
print(arras[0])
print(arras[0:2])  # python支持列表片段访问

arras[0][0] = 2
print("修改 arras[0][0] = ", arras[0][0])

# 删除序列中的元素
line = 0
column = 0
del arras[line][column]
print("删除 arras[0][0] 后 arras[0]=", arras[line])

print("列表相加", [1, 2, 3]+[4, 5, 6])
print("列表相乘", ["Hi"]*4)

# 元组 tuple 跟列表类似，但是不能修改元组中的数据
print("元组", (1, 2, 3, "a", 'b'))
a, b, c = (1, 2, 3)
print("元组=", a, b, c)

# 字典
tab1 = {}  # 申明一个空的字典跟列表一致
print("字典是否含有 a", "a" in tab1)
key = "a"
tab1[key] = 3
print("字典是否含有 a", "a" in tab1)
print("插入字典 tab1[key] =", tab1[key])
tab2 = {"x": 1, "y": 2, "z": "a", 100: 100}  # -- 申明字典
print("字典 tab1=", tab1)
tab1.update(tab2)  # 一个字典插入另一个字典
print("字典 tab1=", tab1)
# print(tab1["x"]) # tab1 中没有x，所以会报错
print(tab2["x"], tab2["z"])  # 访问字典table，索引不再是数字
print("x in tab2 = ", "x" in tab2)  # 判断tab中是否拥有x的key
del tab2["x"]  # 删除元素
tab2[2] = 1
print(tab2)
print("x in tab2 = ", "x" in tab2)
# python中的键值必须是不可变的，可以是数字，字符串，元组

# 遍历字典的元素
for k, v in tab2.items():
    print("key=", k, "value=", v)

print(dir(dict))

# 迭代器
lst = [1, 2, 3]
itr = iter(lst)  # 创建迭代器对象
print(itr)
print("print(next(itr))=", next(itr))  # 访问第一个值
print("print(next(itr))=", next(itr))  # 访问第二个值
print("print(next(itr))=", next(itr))
try:
    print("print(next(itr))=", next(itr))
except StopIteration as e:
    print(e)

# python生成器 ，生成器只能用于迭代，否则没必要这样写


def fibonacci(n):  # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a  # 函数每次执行到这里,返回yield的值,下次调用next的时候直接这里继续运行
        a, b = b, a + b
        counter += 1


f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成

while True:
    try:
        print(next(f), end=" ")
    except StopIteration:  # 结束循环
        print()
        # sys.exit()
        break


# python特有的列表推导式
# 列表推导式提供了从序列创建列表的简单途径,看下面的例子
vec1 = [4, 2, 3]
print([x*x for x in vec1])
print([[x, x**2, x**3] for x in vec1])
print([x*y for x in vec1 for y in vec1])
print([x*y for x in vec1 for y in vec1 if x != y])

# 字典推导式 跟列表推导式差不多
print({x: x**2 for x in vec1})
vec2 = ["a", "b", "c"]
print({x: y for x in vec2 for y in vec1})  # 似乎字典并不能这么用
print({x: x**3 for x in vec1 if x != 1})

print("test sort")
print(sorted(vec1)) #排序后返回新列表
print(vec1)
print(vec1.sort()) #排序后,修改自身
print(vec1)

print('*'*100)
# 日期类型
today = datetime.date.today()  # 日期类
print('今天是', today, type(today))
today_time = datetime.datetime.today()  # 精确到毫秒
print('今天是', today_time, type(today_time))
print("格式化日期", today_time.strftime('%Y-%m-%d %H:%M:%S %f'))

t = time.time()  # utc
print("时间", t, type(t))


#函数+变量引用的测试
def deal(arra):
    arra.append(6)
testA = []
print("testA",testA)
deal(testA)
print("testA",testA)

