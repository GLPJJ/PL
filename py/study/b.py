#!python3.6
# @ guliping

'''
python 变量
python 默认都是局部变量
python 默认都是局部变量

'''

a = 1         # 全局变量
b = 1         # 全局变量


def joke():
    c = 2     # 局部变量 python中函数体内部的是局部变量


joke()
# print(c)    # 报错，这里c是未定义

# 局部变量测试 nonlocal global


def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)


scope_test()
print("In global scope:", spam)

v = 1
while(v >= 1):
    a = 3     	# 全局变量
    b = 3       # 全局变量
    c = 3		# 全局变量
    print(a, b, c)
    v -= 1

print(a, b, c)
print("*"*30)


# 多重赋值
a = b = c = 10
print(a, b, c)
a, b, c = 1, "a", 2
print(a, b, c)

# 多重赋值机制跟lua一样,变量可以下面这样交换值

x = 1
y = 2
print("x=", x, ";y=", y)
x, y = y, x
print("x=", x, ";y=", y)

# python要求左右必须个数一致，不能像lua那样自动赋值nil，或者忽略，所以下面两个都会报错
# a,b,c = 1  报错
# a,b,c = 1,2,3,4  报错

'''
流程控制
'''
if True:
    print("is true")


a = 1
if a == 0:
    print("a=0")
elif a == 1:
    print("a=1")
else:
    print("a~=0")
print("*"*30)

# ? python 三目运算符
b = 5 if a != 1 else 6
print("? b =", b)
print("*"*30)


'''循环'''
n = 5
while(n > 0):  # 另外，在Python中没有do..while循环
    print("n=", n, end=",")
    n = n-1
else:  # 当while中的判断语句为false的时候执行这个语句
    print("while else n=", n)

print("*"*30)

fruits = ["apple", "pear", "orange"]
for fruit in fruits:
    print(fruit, end=",")
print()

for i in range(1, 10, 1):  # range参数 前闭后开 [起点，终点)，步长
    print(i, end=",")
print()

# range(start, stop[, step])
for i in range(len(fruits)):
    print("fruits[", i, "]=", fruits[i], end=",")
    continue  # 跳过后面的语句
    break  # 跳出循环 , 可以尝试把continue语句注释
else:
    print("水果结束了")  # 当有break 的时候我们这个else就不会执行
print("\n"+"*"*30)

for i, v in enumerate(fruits):  # enumerate 的用法等价于上面那个循环，只不过可以获得索引跟值
    print("fruits[", i, "]=", fruits[i], end=",")
print()

# pass 语句
if True:
    pass  # pass 语句本身不会做什么，它只是为了保持程序结构的完整性（缩进）
