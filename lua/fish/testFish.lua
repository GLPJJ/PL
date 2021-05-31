function tableToStr(tab,i)
    i = i or 0

    if i == 3 then
        return "table more than 3"
    else
        i = i + 1
    end
    if tab and type(tab) == "table" then
        local ret = ""
        for k,v in pairs(tab) do
            if type(k) ~= "number" or i == 1 then
                ret = ret.."tab["..k.."]=["..tableToStr(v,i).."];"
            else
                ret = ret.."["..tableToStr(v,i).."]"
            end
        end
        return "\n"..ret.."\n"
    else 
        return ""..tab
    end
end

function ConvertVersion(strVer)
    local n = 0
    local ver = 0
    string.gsub(
        strVer,
        '[^.]+',
        function(w)
            n = n + 1
            ver = ver * 65536 + tonumber(w)
        end
    )
    for i = n + 1, 4 do
        ver = ver * 65536
    end

    return ver
end

--print(ConvertVersion("1.2.2.1"))

function Split(str, reps)
    local resultStrList = {}
    string.gsub(str,'[^'..reps..']+',function ( w )
        table.insert(resultStrList, w)
    end)
    return resultStrList
end

function CompileVersion(verA,verB)
    if verA == verB then return 0 end

    local verAs = Split(verA,".")
    local verBs = Split(verB,".")

    local isVerANew = 0;
    local i = 1;
    while(i<=#verAs and i<=#verBs) do
        print(verAs[i],verBs[i])
        if tonumber(verAs[i]) > tonumber(verBs[i]) then
            isVerANew = 1;
            break;
        elseif tonumber(verAs[i]) < tonumber(verBs[i]) then
            isVerANew = -1;
            break;
        end

        i = i+1
    end

    if(isVerANew == 0) then
        if #verAs > #verBs then
            return 1
        else
            return -1
        end
    else
        return isVerANew
    end
end

function getOrder()
    local order = { 1, 2, 3 }
    local AskRate = {10,30,60}
    local askOrder = {}
    for i = 1, 3 do
        sum = 0
        for i in ipairs(order) do
            sum = sum + AskRate[order[i]]
        end
        local rate = math.random(sum)
        -- print(rate)

        local start = 0
        local finish = 0
        for i in ipairs(order) do
            finish = start + AskRate[order[i]]
            if rate <= finish and rate > start then
                table.insert(askOrder, order[i]);
                table.remove(order, i)
                break
            end
            start = finish
        end
    end

    local str = ""
    for i,v in ipairs(askOrder) do str = str..","..v end
    print(str)
end

local __fish_rate_list = {
{1,2,3,4,5,6},
{1,2,3,4,5,6},
{1,2,3,4,5,6},
{1,2,3,4,5,6},
{1,2,3,4,5,6},
{1,2,3,4,5,6}}
function refresChair()
    for m = 1, #__fish_rate_list do
        local i, j, temp
        local l = #__fish_rate_list[m]
        for i = 1, l do
            j = math.random(l)
            temp = __fish_rate_list[m][i]
            __fish_rate_list[m][i] = __fish_rate_list[m][j]
            __fish_rate_list[m][j] = temp
        end
    end

    local str = ""
    for i,v in ipairs(__fish_rate_list) do 
        for j,v2 in ipairs(v) do
            str = str..","..v2
        end
        str = str .. "\n"
    end
    print(str)
end

math.randomseed(os.time())
-- for i=1,10 do
--     refresChair()
--     print(string.rep("*",100))
-- end

local DeskChairCnt = 4
function shuffle()
    local len, second = 6,10

    local desk_chair_rate_order = {}
    for i = 1, DeskChairCnt do --插入当前桌子的位置的一套鱼死亡轮询概率
        local rate_order = {}
        for i = 1, len do --先顺序插入位置
            table.insert(rate_order, i)
        end

        for i = 1, len * 2 do --随机调整位置
            local pos1 = math.random(len)
            local pos2 = math.random(len)
            rate_order[pos1], rate_order[pos2] = rate_order[pos2], rate_order[pos1]
        end
        table.insert(desk_chair_rate_order, rate_order)
    end

    print(tableToStr(desk_chair_rate_order))
    -- self.__fish_rate_total = len
    -- self.__fish_rate_per_sec = second
    -- self.__fish_rate_cur_index = 1
    -- self.__fish_rete_cur_sec = 0
    -- self.__fish_rate_list = desk_chair_rate_order
    -- for m = 1, #self.__fish_rate_list do
    --     local i, j
    --     local l = #self.__fish_rate_list[m]
    --     for i = 1, l do
    --         j = math.random(l)
    --         --交换位置
    --         self.__fish_rate_list[m][i],
    --             self.__fish_rate_list[m][j] = self.__fish_rate_list[m][j], self.__fish_rate_list[m][i]
    --     end
    -- end
end

shuffle()
shuffle()
shuffle()


function randOneList(list)
    local probs = list
    local total = 0
    for i = 1, #probs do
        total = total + probs[i]
        probs[i] = total
    end

    local r = math.random(total) --随机数
    for i = 1, #probs do
        if r <= probs[i] then
            return i
        end
    end
end

function randOne(...)
    local probs = table.pack(...)
    probs.n = nil
    return randOneList(probs)
end



-- print(randOne(100,200,300,400))
-- print(randOneList({100,200,300,400}))

--读取鱼ID配置的类型，提高效率
Cfg = {
    FishType = {
        {1, 2, 3, 4, 5, 6},
        {{8}, {7, 9, 10, 11, 12, 13, 14, 15, 16}},
        {17, 18, 19, 20, 21, 23, 25},
        {22, 24, 26, 27, 28},
        {},
        {31},
        {30},
        {29}
    }
}
Cfg.FishType2Category = {}
Cfg.FishType2Probability = {}
for i = 1, #Cfg.FishType do
    local curList = Cfg.FishType[i]
    if i == 2 then
        --有两种鱼
        local fishsProbabilityInSameType = {} --同类鱼的权重
        local total = 0
        for j = 1, #curList do
            local curListList = curList[j]
            for k = 1, #curListList do
                -- statements
                print(k)
                Cfg.FishType2Category[curListList[k]] = i
                fishsProbabilityInSameType[total+k] = j
            end
            total = total + #curListList
        end
        fishsProbabilityInSameType.total = total
        print(tableToStr(fishsProbabilityInSameType))
        Cfg.FishType2Probability[i] = fishsProbabilityInSameType
    else
        for j = 1, #curList do
            Cfg.FishType2Category[curList[j]] = i
        end
    end
end

print("FishType2Probability=",tableToStr(Cfg.FishType2Probability))

i = 2
t = Cfg.FishType2Probability[i].total
tempT = {}
tempS = string.sub(tostring({}),7)
print(tempS)
print(t,os.time(),tonumber(tempS,16))
math.randomseed(os.time())
local r = math.random(t)
print(r)
local mid_idx = 0--Cfg.FishType2Probability[i][r]
print(r,mid_idx,math.random(10),math.random(t))

local randomTab = {}
function randomInitEx(key, number)
    randomTab[key] = {}
    number = number or randomTab[key .. "len"] or 1000
    randomTab[key .. "len"] = number
    for i = 1, number do
        table.insert(randomTab[key], i)
    end

    for i = 1, number * 3 do
        local j = math.random(number)
        local k = math.random(number)
        randomTab[key][j], randomTab[key][k] = randomTab[key][k], randomTab[key][j]
    end
end

function randomEx(key)
    local r = table.remove(randomTab[key])
    if #(randomTab[key]) == 0 then
        randomInitEx(key) --我们已经把随机队列取完了。。那么我们开始新的一轮循环
    end
    return r
end

randomInitEx("glp",20)
for i=1,40 do
    print("glp",i,randomEx("glp"))
end
print("tab=",tableToStr(randomTab["glp"]))


-- local objsPool = {}
-- local mgr = {}
-- mgr.pool = objsPool
-- table.insert(mgr.pool,{})
-- table.insert(mgr.pool,{})
-- table.insert(mgr.pool,{})
-- table.insert(mgr.pool,{})
-- table.insert(mgr.pool,{})

-- print("#objsPool",#objsPool)
-- print("#mgr.pool",#mgr.pool)
-- local obj = table.remove(mgr.pool)
-- print("#objsPool",#objsPool)
-- print("#mgr.pool",#mgr.pool)
local t1 = {uid=165271,pay_type=15,oid=113}
local t2 = {order_15_113 = t1}
t2['order_15_113'] = nil
print(t2['order_15_113'],tableToStr(t2))

local function savePayOrderToLocal(order)
    local file = io.open("payOrder.json", "w")
    --覆盖文件
    if file ~= nil then
        file:write(order)
        file:flush()
        file:close()
    else
        tlog.error("savePayOrderToLocal order=%s", order)
    end
end

-- savePayOrderToLocal("2")

print(CompileVersion("1.0.62.1","1.2.0"))


function string2time(timeString)
    if type(timeString) ~= 'string' then
        error('string2time: timeString is not a string')
        return 0
    end
    local fun = string.gmatch(timeString, "%d+")
    local y = fun() or 0
    if y == 0 then
        error('timeString is a invalid time string')
        return 0
    end
    local m = fun() or 0
    if m == 0 then
        error('timeString is a invalid time string')
        return 0
    end
    local d = fun() or 0
    if d == 0 then
        error('timeString is a invalid time string')
        return 0
    end
    local H = fun() or 0
    if H == 0 then
        error('timeString is a invalid time string')
        return 0
    end
    local M = fun() or 0
    if M == 0 then
        error('timeString is a invalid time string')
        return 0
    end
    local S = fun() or 0
    if S == 0 then
        error('timeString is a invalid time string')
        return 0
    end
    return os.time({ year = y, month = m, day = d, hour = H, min = M, sec = S })
end

function todayBegin()
    local today = os.date("*t")
    return os.time({ year = today.year, month = today.month,
                     day = today.day, hour = 0, min = 0, sec = 0 })
end

local tmutc = string2time('2019-05-28 00:00:00')
local utc = todayBegin()
if math.abs(utc - tmutc) % (7 * 86400) == 0 then
    print("YES Clean")
else
    print("NO Clean")
end

local wealths = {}
table.insert(wealths,{uid=0,val=100})
table.insert(wealths,{uid=1,val=-20})
table.sort(wealths, function(a, b) return a.val < b.val end)
print("sort:",tableToStr(wealths))


print(CompileVersion("2.1.0.0","2.0.1.003"))
local a1 = "28598gc4ca4238a0b923820dcc509a6f75849b"
local a2 = string.find(a1,"g")
local a3 = string.sub(a1,1,a2-1)
print("tonumber()",a1,a2,a3,tonumber(a3,16))


function encodeToJsonBySortKeys(tab,nest)
    nest = nest or 3
    local keys = {}
    for k in pairs(tab) do
        table.insert(keys, k)
    end

    local ret = "{"
    table.sort(keys)
    for i, k in ipairs(keys) do
        local v = tab[k]
        local typeV = type(v)
        ret = ret .. "\"" .. k .. "\":"

        if typeV == "number" then
            ret = ret .. v .. ","
        elseif typeV == "string" then
            ret = ret .. "\"" .. v .. "\"" .. ","
        elseif typeV == "table" and nest > 0 then
            ret = ret .. encodeToJsonBySortKeys(v,nest-1)..","
        else
            ret = ret .. "\"unknown type("..typeV..")\","
        end
    end
    ret = string.sub(ret, 1, -2) .. "}"
    return ret
end

print(encodeToJsonBySortKeys({uid=160000,coin=1000,name="aa",b=encodeToJsonBySortKeys,c=wealths}))