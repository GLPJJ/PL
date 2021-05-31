
local v = {betlst = {}}

local validBet1 = math.min(v.betlst[1], v.betlst[2], v.betlst[3], v.betlst[4])
local validBet2 = math.min(v.betlst[5], v.betlst[6], v.betlst[7], v.betlst[8])
if validBet1 > 0 and validBet2 > 0 then
    local validMin = math.min(validBet1, validBet2 / 4)
    validBetSum = v.betlst[1] + v.betlst[2] + v.betlst[3] + v.betlst[4] + v.betlst[5] + v.betlst[6] + v.betlst[7] + v.betlst[8] - validMin * 20
else
    validBetSum = v.betlst[1] + v.betlst[2] + v.betlst[3] + v.betlst[4] + v.betlst[5] + v.betlst[6] + v.betlst[7] + v.betlst[8]
end

