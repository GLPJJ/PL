--#!lua 5.3.2
--@guliping

--[[ pcall 和 xpcall单独列一个文件演示
	pcall用于保护模式下执行代码，返回状态值和值,如果状态值为true，那么值就是执行结果，否则就是一个error
	xpcall类似于pcall不过提供了一个回调接口
]]

function doSomething(val)
	val()
end

print("\npcall")
local status,val = pcall(doSomething,50)
print(status,val,type(val))
print(debug.traceback()) --注意这里只是常规打印我们的调用堆栈

-- debug.debug()

print("\nxpcall")
xpcall(doSomething,function(e) 
	print("e=",e,type(e))
	print(debug.traceback())
	return e 
end, 50)


print(debug.traceback("11", 2))
-- pcall和xpcall的区别就是，xpcall能在回调的函数中打印错误堆栈，方便查问题，
-- pcall只能打印一行错误信息
