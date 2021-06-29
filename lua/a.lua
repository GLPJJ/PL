--#!lua 5.3.2
--@guliping

--[[
查询lua环境
for k,v in pairs(_G) do print(k,v) end
--]]

--[[
基础篇， 初识lua
print 和 type都是 lua内建的函数。
初识lua类型和运算符

http://blog.csdn.net/glp3329/article/details/52511855

lua 关键字：
and			break	do		else
elseif		end		false	for
function	if		in		local
nil			not		or		repeat
return		then	true	until
while

一般约定，以下划线开头连接一串大写字母的名字（比如 _VERSION）被保留用于 Lua 内部全局变量
--]]

-- 单行注释

--[[
    lua多行注释
--]] --这里习惯在前面加上'--'

print(type(a)) -- 输出 nil ，访问未定义的变量，
-- 当我们不需要这个变量或者需要删除的时候我们可以给它赋值nil，
a = "123"
print(type(a)) -- 输出 string
a = 12
print(type(a)) -- 输出 number
a = 12.3
print(type(a)) -- 输出 number
print(0/0) -- 输出 nan  意思就是Not a Number 不是数字
print(type(0/0)) -- 输出 number , 意思就是nan都是number

--[[
lua 基础数据类型:

nil
boolean
number（双精度浮点实数）
string（使用两个方括号可表示一块字符串，就像注释一样；
	在对一个数字字符串上进行算术操作时，Lua 会尝试将这个数字字符串转成一个数字）
userdata（C\C++ struct数据或指针）
function、thread（其实是协同进程的概念，跟线程的区别是同一时刻，协程只有一个运行，线程是多个）
table
--]]


--[[
lua操作符
--]]

-- 1.算术运算符:
a = 10
b = 20
print("a+b=",a+b) --加
print("'11'+b","11"+b)--对字符串操作，优先将字符串化成number类型
print("a-b=",a-b) --减
print("a*b=",a*b) --乘
print("b/a=",b/a) --除
print("b%a=",b%a) --模
print("b^a=",b^a) --指数  lua使用这个当指数，意味着不能把它当按位异或运算了，我们有其他方法
print("b//a=",b//a) --地板除 取整
print("-a=",-a)
print("*********************************")

-- 2.比较操作符:
print("a==b",a==b)
print("a~=b",a~=b) -- 这个区别与别的 !=
print("a>b",a>b)
print("a<b",a<b)
print("a>=b",a>=b)
print("a<=b",a<=b)

--a += 2 lua中没有这样的赋值运算符，需要自己写成 a = a+2

-- 3.逻辑运算符:
a = true -- 这里必须小写
b = false
print(a and b) 	--等价与 &&
print(a or b) 	--等价与 ||
print(not a) 	--等价与 !

--[[
运算符优先级
从高到低的顺序：
^
not    - (unary)
*      /
+      -
..
<      >      <=     >=     ~=     ==
and
or
--]]

-- 4.其他运算符

--字符串连接符 ..
a = "123"
b = "abc"
print(a..b)

--长度计算符 #
print(#a) -- 计算字符串长度
b = {1,2}
print(#b) -- 计算table size

--table 访问有三个方法，使用[],或者点，或者内建函数
tab = {}
tab["n"] = 10 -- tab["n"] 等价于 tab.n
tab[1] = 9 -- 数字无法使用第二种表示方法 tab.1 会报错
print("tab.n=",tab.n,';tab[1]=',tab[1])
print("tab.n=",rawget(tab,"n"),';tab[1]=',tab[1])

-- lua可以计算 数字的字符串和数字的相加
print("1"+2)


--字符串数字转换
print("字符串->数字",tonumber("1"))
print("字符串->数字",tonumber("a",16))
print("数字->字符串",tostring(1))
print("数字->字符串",string.format("%x",10))
