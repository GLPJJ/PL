-- @ guliping
-- 名字取i.lua是为了和python对应
-- 协程 lua
-- 类似线程的概念

--看懂下面例子的输出就能理解lua的协程，lua的协程同一时刻只能运行一个
function foo (a)
	print("foo",coroutine.running())
	print("foo", a)
	return coroutine.yield(2*a)--这里挂起子线程，并将yield中的值当做coroutine.resume的返回值
end

--这里创建一个协程，指定需要传入两个参数
co = coroutine.create(function (a,b)
	print("co-body",coroutine.running())--当前不是主线程
	print("coroutine status",coroutine.status(co))
	print("co-body a,b=", a, b)
	local r = foo(a+1)--调用外部函数
	print("co-body r=", r)
	local r, s = coroutine.yield(a+b, a-b)--挂起子线程，并把算出来的两个值返回
	print("co-body r,s=", r, s)
	return b, "end"--函数执行结束，返回最后的值
end)

print("main 1",coroutine.running())--返回当前的线程对象，和一个是否是主线程的bool值
print("main 2 coroutinen status=",coroutine.status(co))--返回coroutine的当前状态
--"suspended" "running" "dead"

--1和10会传入coroutine.create创建的函数，主线程挂起
print("main 3", coroutine.resume(co, 1, 10))
--如果子线程没有报错，coroutine.resume默认第一参数是true 后面才是yield返回的参数

print("main 4",coroutine.running())
print("main 5 coroutine status=",coroutine.status(co))

--这里直接回到子线程刚才yield的位置继续执行，并且把"rrr"当做子线程中
--coroutine.yield的返回值，所以上面foo返回的其实是这里传入的值
print("main 6", coroutine.resume(co, "rrr"))
print("main 7", coroutine.resume(co, "x", "y"))--这里同样的道理传入"x","y"

print("main 8 coroutinen status=",coroutine.status(co))
print("main 9", coroutine.resume(co, "x", "y"))--已经死掉的线程无法再resume了


--[[最后总结
上面的例子有点过于复杂，使用好几次yield和resume，但是实际中我们只需要一次yield和resume：
举例子：
	用户登录过程，首先用户发上来账号和密码，这时候我们需要请求数据库，查询数据库是否有信息，再查询数据库
	的时候，我们先要把登录过程挂起，等到数据库返回再唤起登录过程。

	伪代码：
	function login(account,pwd)

		--查询数据库的密码
		local pwdInDB = coroutine.yeild(db:query(account))
		
		--检查密码是否一致
		if pwdInDB == pwd then
			print("登录成功")
		else
			print("登录错误")
		end

	end
	local co = coroutine.create(login);
	function dbBack(pwd)
		--数据库返回
		coroutine.resume(co,pwd)
	end

	上面的代码就是一个实际的应用。