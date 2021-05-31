#!lua 5.3.2
--@guliping
--[[ IO 
]]

-- lua的字符串格式化同c的printf格式一致，这里不再赘述

-- lua 文件IO,这里只讲复杂模式，简单模式不表
f = io.open("zzz_io_test","w") -- r rb r+ rb+ w wb w+ wb+ a ab a+ ab+
f:write("Hello World \n\tfrom lua") 
f:flush()
f:close() -- 面向对象写法 等价于 下面
-- f.close(f)

-- 读取文件全部内容
f1 = io.open("zzz_io_test","r")
while true do
	local line = f1:read() --读取一行内容
	if(line == nil) then
		break
	end
	print(line)
end
f1:close()

f11 = io.open("zzz_io_test","r")
print("读取所有内容",f11:read('*a'))--读取所有内容
f11:close()

-- lua 不提供tell函数，但提供seek函数，不传参数，返回当前文件读取位置，强势可以理解
-- seek 第一参数就是位置，第二个参数才是偏移量
f2 = io.open("zzz_io_test","r")
print("当前文件位置",f2:seek())
f2:seek("set",5) -- "cur","end"
print("当前文件位置",f2:seek())
print(f2:read())
print("当前文件位置",f2:seek())
f2:close()
