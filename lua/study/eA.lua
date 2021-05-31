#!lua 5.3.2
--@guliping
--[[
模块示例
]]

eA = {}

--定义模块变量
eA.a = 1

function eA.b()
	print("call dA.b()")
end

-- 模块私有函数
local function c()
	print("call c()")
end

--模块函数，调用模块私有函数
function eA.d()
	c()
end

--模块函数
eA.e = function()
	print("call e()")
end

return eA
