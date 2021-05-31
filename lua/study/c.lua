#!lua 5.3.2
--@guliping
--[[ 函数 
http://blog.csdn.net/glp3329/article/details/52538511
]]
function none()
end
print(none() == nil) --返回空

function sub(a,b)
	return a-b
end
print("3-1=",sub(3,1))

function add(a,b)
	return a,"+",b,"=",a+b
end

print(add(3,4))
print(add(1,2,3)) -- 忽略了3
--add() 由于里面使用加法，所以会报错 ,为了避免这个错误，我们可以下面这样定义
function addEx(a,b)
	a = a or 0
	b = b or 1
	return add(a,b)
end
print(addEx()) -- 这里不传参数也不会报错

--可变长参数函数
function average(...)
   local result = 0
   local arg={...}
   for i,v in ipairs(arg) do
      result = result + v
   end
   print("总共传入 " .. #arg .. " 个数")
   return result/#arg
end

print("平均值为",average(10,5,3,4,5,6))
print("****************************")
-- lua 解包table
print("平均值为",average(table.unpack({10,5,3,4,5,6})))
