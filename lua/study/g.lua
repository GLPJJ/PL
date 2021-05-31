--类 lua

-- 在学习类之前我们首先需要学会lua的元表，元方法，
-- https://www.jianshu.com/p/58050050b7cb

function tableToStr(tab)
	if tab and type(tab) == "table" then
		local ret = ""
		for k,v in pairs(tab) do
			-- if type(v) == "table" then
			-- 	v = tostring(v)
			-- elseif type(v) == "function" then
			-- 	v = tostring(v)
			-- end
			ret = ret.."tab["..k.."]="..tostring(v)..";"
		end
		return ret
	else 
		return ""..tab
	end
end

--元表 metatable
local a = {x=1;y=2}
local b = {z=3}
print("a =",tableToStr(a))
print("b =",tableToStr(b))

-- print("a+b =",tableToStr(a+b)) -- 报错

local mt = {}
--重载操作符 
mt.__add = function (v1,v2)
	local ret = {}
	setmetatable(ret,mt)
    for _,v in pairs(a) do 
        table.insert(ret,v)  
    end
    for _,v in pairs(b) do 
        table.insert(ret,v)  
    end

    return ret
end

setmetatable(a,mt)--设置a的元表
setmetatable(b,mt)--设置b的元表
print("a+b =",tableToStr(a+b)) -- 正常访问

--具体其他的重载操作可以参见我写的博客 https://www.jianshu.com/p/58050050b7cb

-- 两个特殊的元方法 __index 读取 ； __newindex 写入
mt.a = {a=10}
print(a.a)
mt.__index = mt
print(a.a,tableToStr(a.a))--由于我们指定了__index所以，我们在找a的时候如果没有"a"，那么就会去__index指定的table对象找，相当于在mt里面找
print(b.a)--与a一致

a.b = 20
print(tableToStr(a))
mt.__newindex = mt
a.c = 30 --这里的写入不在往a里面写，而是写入到设置的__newindex的mt中
print("a=",tableToStr(a))
print("mt=",tableToStr(mt))

rawset(a,"d",40)--不过可以以这样的方法直接写入到a
print("a=",tableToStr(a))
print('rawget(a,"c")=',rawget(a,"c"))

-- error (message [, level])
-- Level=1[默认]：为调用error位置(文件+行号)
-- Level=2：指出哪个调用error的函数的函数
-- Level=0:不添加错误位置信息
-- 函数参数：table，指定的key，指定的新value
mt.__newindex = function(tab,k,v)
	print("call __newindex",tab,k,v)
	--抛出异常
	error("table is read only")
end

-- 函数参数：table，指定的key
mt.__index = function(tab,k)
	print("call __index",tab,k)
	return mt[k]
end

print("a.e=",a.e)
--具体 pcall 和 xpcall 请看g1.lua演示
local status,val = pcall(function(v) a.e=v end,50)
print(status,val)

--还有一个特殊的 __call
-- This event happens when Lua tries to call a non-function value
mt.__call = function(inst,...)
	print("inst == a",inst == a)
	print("call mt",...)
end

a(1,2)--这里我们a不是函数，只是一个table，但是我们也可以像函数一样调用它

--根据上面的特性，我们就可以定制自己的简单class了,复杂一点的可以参见本目录的class.lua
function Class(base, _ctor)
	local c = {}    -- a new class instance
	if not _ctor and type(base) == 'function' then
        _ctor = base
        base = nil
    elseif type(base) == 'table' then
        -- our new class is a shallow copy of the base class!
		-- while at it also store our inherited members so we can get rid of them 
		-- while monkey patching for the hot reload
		-- if our class redefined a function peronally the function pointed to by our member is not the in in our inherited
		-- table
        for i,v in pairs(base) do
            c[i] = v
        end
        c._base = base
    end

	c.__index = c

	local mt = {}
    mt.__call = function(cls,...)
    	local obj = {}
		setmetatable(obj, c)
		if c._ctor then
		   c._ctor(obj, ...)
		end
		return obj
	end

	
    c._ctor = _ctor
    setmetatable(c, mt)
    return c
end

--定义类
local Animal = Class(function(self,name)
	print("Animal base =",self._base)
	self.name = name
end)

--定义成员方法 在lua中： Animal:call() 等价于 Animal.call(self)
function Animal:call()
	print(self.name,": ...")
end

--[[
	解析下面的调用过程
	1.调用Class中mt.__call，生成一个新的对象，把对象的元表设置为本类(即Animal)，
		调用构造函数，也就是上面定义的时候传入的function，经过构造函数之后返回这个实例对象，也就是我们获得的anima
	2.然后我们调用anima这个实例对象的call方法,在lua中 anima.call(anima,arg) 等价于 anim:call(arg)
]]
local anima = Animal("动物")
anima:call()

--继承
local Dog = Class(Animal,function(self,name)
	print("Dog base =",self._base)
	self._base._ctor(self,name)--调用父类构造函数

	--实现更多的方法
end)

--lua中没法实现重载，只有覆盖
function Dog:call()
	self._base.call(self)--调用父类的方法需要把自己的实例传入，否则父类的self参数将会没有定义
	print(self.name,": wang wang")
end

local dog = Dog("狗")
dog:call()
