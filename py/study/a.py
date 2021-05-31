#!python3.6
# @ guliping

'''
    python
    vscode 配置：
        {
            "name": "Python: Current File",
            "type": "python", //指定python配置，参见python的安装
            "request": "launch",
            "program": "${file}"//指定运行当前文件
        }
    sublime 配置   可以在python27中增加一个python3的快捷方式 或者配置 "path":C:/Python37
        {
            "cmd": ["python3", "-u","$file"],
        }

查询python环境
import builtins
dir(builtins)#跟lua一样，查看当前内建的变量和函数，模块
dir()#查看当前定义的变量,函数,模块
import sys
dir(sys)#查看该sys包下可用的变量，函数，模块

python 安装第三方包库 参见http://blog.csdn.net/glp3329/article/details/52664998
'''

'''
基础篇， 初识python
print 和 type都是 python内建的函数。
初识python类型和运算符
	
help函数可以给我们提供帮助文档

http://blog.csdn.net/glp3329/article/details/52511855
'''
'''
import keyword
keyword.kwlist

控制台输入，获取当前python的关键字

'''

# 单行注释
'''
多行注释 ， python讲究代码块的缩进保持一致
'''

# type(a)  不能使用未定义的变量

''' 输出
#Traceback (most recent call last): 
#  File "<stdin>", line 1, in <module> type(a) 
#NameError: name 'a' is not defined
'''

print("中文")

print(type(True)) #bool
a = "123"
print(type(a))  # 输出 <class 'str'>
print(id(a))  # 输出 35672112 - 每个人的结果不一样
print('isinstance(a,str)=',isinstance(a,str))
a = 12
print(type(a))  # 输出 <class 'int'>
print(id(a))  # 输出 1488898480 - 每个人的结果不一样
a = 12.3
print(type(a))  # 输出 <class 'float'>
print(id(a))  # 输出 5734688 - 每个人的结果不一样

print(bytes)  # 不可编辑的二进制
print(bytearray(10))  # 可编辑的二进制数组
print(type([]))
'''
Python3 中有六个标准的数据类型:

Number（数字） int、float、bool、complex 
	只有一种整数类型 int，表示为长整型，没有 python2 中的 Long
String（字符串） str
List（列表）
Tuple（元组）
Sets（集合）
Dictionary（字典）

申明的变量，可以使用del语句删除一些对象引用
del a, b
'''
print("class test")
print(type((1,)))
print(type([]))
print(type({}))

'''作死除法
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
'''
# 0/0

'''
python操作符

在交互模式下，python会把运算的结果保存在 '_' 里面
'''

# 1.算术运算符:
a = 10
b = 20

a, b = b, a
print("a=", a, "b=", b)

print("a+b=", a+b)  # 加
print("a-b=", a-b)  # 减
print("a*b=", a*b)  # 乘
print("b/a=", b/a)  # 除
print("b%a=", b % a)  # 模
print("b**a=", b**a)  # 指数
print("b//a=", b//a)  # 地板除 取整
print("-a=", -a)
print("*"*30)

# 2.比较操作符:
print("a==b", a == b)
print("a!=b", a != b)
print("a>b", a > b)
print("a<b", a < b)
print("a>=b", a >= b)
print("a<=b", a <= b)

# 3.赋值运算符：
c = 1
c += a
print("c+=a = ", c)
c -= a
print("c-=a = ", c)

# 类似的还有 *= /= %= **= //=
c *= 2
print(c)
c /= 2
print(c)
c %= 1
print(c)
c **= 2
print(c)
c //= 2
print(c)

# 4.位运算符：
a = 3  # 二进制的表示  0000 0011
b = 10  # 二进制的表示 0000 1010

print("a&b =", a & b)  # 按位与
print("a|b =", a | b)  # 按位或
print("a^b =", a ^ b)  # 按位异或
print("~b =", ~b)  # 按位取反
print("a<<2 =", a << 2)  # 按位左移
print("b>>2 =", b >> 2)  # 按位右移

# 5.逻辑运算符:
a = True  # 这里必须大写
b = False
print(a and b)  # 等价与 &&
print(a or b)  # 等价与 ||
print(not a)  # 等价与 !

# 6.成员运算符:
a = "a"
b = "abcdefg"
print("a in b =", a in b)  # 判断a是否在b的里面，可以是字符串，或者是元组，序列，字典
print("a not in b =", a not in b)

# 7.身份运算符
a = 1
b = 2
print("a is b =", a is b)  # 判断是否同一个对象
print("a is not b =", a is not b)
b = 1
print("a is b =", a is b)

"""

Python运算符优先级
以下表格列出了从最高到最低优先级的所有运算符：
运算符				描述
**					指数 (最高优先级)
~ + -				按位翻转, 一元加号和减号 (最后两个的方法名为 +@ 和 -@)
* / % //			乘，除，取模和取整除
+ -					加法减法
>> <<				右移，左移运算符
&					位 'AND'
^ |					位运算符
<= < > >=			比较运算符
<> == !=			等于运算符
= %= /= //= -= += *= **=	赋值运算符
is is not			身份运算符
in not in			成员运算符
not or and			逻辑运算符

"""

# 字符串连接符 +
print("123"+"abc")

'''
需要说明的是 python不支持字符串和数字相加，lua可以让是数字的字符串跟数字相加
'''
# print("1"+2) # 报错

# 字符串数字转换
print("字符串->数字", int("1"))
print("16进制字符串->数字", int("a",16))
print("数字->字符串", str(15))
print("数字->16进制字符串", "{0:02x}".format(15))
print("字节->数字", ord('A'))
print("数字->字节", str(1).encode())
print("字节->数字", b'11111'.decode('utf-8'))

print(not True)  # 不能使用 ‘!’

# 通过内建变量 __file__ 来获取当前脚本真实目录
print(__file__)

# chang 1

# chang 2

# chang 3

# 三目运算
print("1" if False else "2")
