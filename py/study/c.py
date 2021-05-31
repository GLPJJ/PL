#!python3.4
# @ guliping

''' 函数
http://blog.csdn.net/glp3329/article/details/52538511
'''


def none()->None:
    pass


print(none())  # 默认返回None


def sub(a, b):
    return a-b


print("3-1=", sub(3, 1))


def add(a:int, b:int):
    return a, "+", b, "=", a+b  # 返回一个元组


print(add(3, 4))

# add() #报错 python的必须参数必须数量一致
# add(1) #报错 python的必须参数必须数量一致
# add(1,2,3) #报错 python的必须参数必须数量一致
# 但是我们可以改造add函数


def addEx(a=0, b=1):  # 添加默认值
    return add(a, b)


print(addEx())
print(addEx(2))
print(addEx(b=2))  # 关键字参数，指定传给b参数

fAdd = add  # 函数类型的变量
print(fAdd(10, 11))  # 调用

# 可变长参数函数


def average(*vartuple):  # ‘*’ 接受所有超出参数列表的位置参数，
    result = 0
    for i in vartuple:
        result += i
    print("总共传入 " + str(len(vartuple)) + " 个数")
    return result/len(vartuple)


print("平均值为", average(10, 5, 3, 4, 5, 6))  # 位置参数调用


def testmap(*vartuple, **varmap):  # ‘**’ 接受所有的关键字参数
    for i in range(len(vartuple)):
        print("vartuple[", i, "] =", vartuple[i], end=",")
    else:
        print()

    keys = sorted(varmap.keys())
    for key in keys:
        print(key, ":", varmap[key], end=",")
    print()


testmap(4, 5, 5, a=1, b=2)  # 关键字参数调用,需要注意的是位置参数必须放在关键字参数前面

print("*"*30)
# * 也可以解包队列
testmap(*[4, 5, 5])
print("*"*30)
# ** 也可以解包字典
testmap(**{"a": 1, "b": 2})

# lambda 创建匿名函数
# 语法 lambda [arg1 [,arg2,.....argn]]:expression


def mul(arg1, arg2): return arg1*arg2


print("3*4 = ", mul(3, 4))

#
def test(a:int,b:str)->str:
    return str(a)+b
print("test(1,'a')=",test(1,'a'))