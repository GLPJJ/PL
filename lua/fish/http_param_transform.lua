-- lua 5.3.2
--@ guliping

function parse(s)
	local str = "map = "..s.." return map"

	local status,f = pcall(load,str);
	print(status,f)
	if status and f then
		print(str.rep("*",60))
		for k,v in pairs(f()) do
			print(k..":"..v)
		end
	else
		print(str.rep("*",60))
		print("load error = ")
	end
	print(str.rep("*",60))
end	

--调用的时候务必把参数中的中文改成英文或数字
parse("{gid=322724, uid=146953, lid=100004, os=1, ccode=86, play_mode=0}")
parse("{8D777F385D3DFEC8815D20F7496026DC=5b70d8f2baa23057f1d45b251cee8b97, 34D1C35063280164066ECC517050DA0B=2880, 07CC694B9B3FC636710FA08B6922C42B=1489486803, area=86, 04B29480233F4DEF5C875875B6BDC3B1=79c091ece0898a0ae6c699493cd8c7f049c5d1d3, my-app-ver=1.5.0}")

--URL = http://api.sociapoker.com/league/getSettlementInfo;
--Param={gid=248957, uid=110457, lid=100000, os=1, tid=7474412, ccode=86}

-- python 接口返回中文数据，转换成中文
function show_utf8(s)
	local temp = string.gsub(s,"\\u","0x")
	if(#temp % 6 ~= 0) then
		print("Error Str")
		return
	end

	local utf8s = ""
	local pos = 0
	while pos < #temp do
		local start = string.find(temp,"0x",pos)
		local ed = start + 6
		pos = ed
		local c = string.sub(temp,start,ed-1)
		-- print(c)
		local c_num = tonumber(string.sub(c,3),16)
		-- print(c_num)
		utf8s = utf8s..utf8.char(c_num)
		
	end
	print("接口返回utf8字符转中文:"..s.." ->"..utf8s)
	-- print(utf8.len(temp))
	-- print(utf8.char(0x7248))
end

show_utf8("\\u7248\\u672c\\u8fc7\\u4f4e\\uff0c\\u8bf7\\u5347\\u7ea7\\uff01")
