#!lua 5.3.2
--@guliping
--[[

lua 变量
lua中的变量有三种类型，全局变量，局部变量，表域
lua 中的变量全是全局变量，那怕是语句块或是函数里，除非用 local 显示声明为局部变量
局部变量的作用域为从声明位置开始到所在语句块结束。
变量的默认值均为 nil

应该尽可能的使用局部变量，有两个好处：
1. 避免命名冲突。
2. 访问局部变量的速度比全局变量更快。
--]]

a = 1               -- 全局变量
local b = 1         -- 局部变量

function joke()
    c = 2           -- 全局变量
    local d = 2     -- 局部变量
end

joke()
print(c,d)

v = 1
while(v >= 1) do
    local a = 3     -- 局部变量
    b = 3           -- 全局变量
    c = 3			-- 全局变量
    print(a,b,c)
    v = v - 1    
end

print(a,b,c)
print("*********************************")

--[[ 
Lua可以对多个变量同时赋值，变量列表和值列表的各个元素用逗号分开
，赋值语句右边的值会依次赋给左边的变量。
--]]
-- a = b = c = 10 不允许连等
--print(a,b,c) -- 未定义的变量默认值是nil
a,b,c = 1,"a",2
print(a,b,c)


--遇到赋值语句Python会先计算右边所有的值然后再执行赋值操作，所以我们可以这样进行交换变量的值：

x = 1
y = 2
print("x=",x,";y=",y)
x,y = y,x
print("x=",x,";y=",y)

--[[
当变量个数和值的个数不一致时，Lua会一直以变量个数为基础采取以下策略：
a. 变量个数 > 值的个数             按变量个数补足nil
b. 变量个数 < 值的个数             多余的值会被忽略
--]]

--[[
流程控制
--]]
if true then
	print("is true")
end

a = 1
if a == 0 then
	print("a=0")
elseif a == 1 then
	print("a=1")
else
	print("a~=0")
end

--[[
循环
--]]
n = 5
while(n > 0) do
	print("n=",n)
	n = n-1
end

print("*********************************")

-- 数值for循环
n = 6
for i=1,n do -- for中的表达式在开始循环前只计算一次
	print("i=",i)
end
print("*********************************")
for i=6,0,-2 do -- 前后闭区间 [循环初始化，指定结束值]，指定步长
	print("i=",i)
end

-- 泛型for循环
for k,v in pairs(_G) do --查看当前lua环境中已经定义的function，table
	print(k,v)
end

tab = {10,9,8,7,6}
for i,v in ipairs(tab) do
	print(i,v)
end

r = 5
repeat
	print("r=",r)
	r = r+1 -- r++ r+=1 错误
	--continue lua中没有continue
	-- break -- 跳出循环 
until(r >= 9) --这里改成false永远执行
