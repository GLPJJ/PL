

function LogTable(tab)
    if type(tab) == "table" then
        local out = string.rep("*",20).."\n"
        for k,v in pairs(tab) do out = out.."["..tostring(k).."] = "..LogTable(v)..";" end
        return "\n"..out.."\n"..string.rep("/",20)
    elseif type(tab) == "nil" then
        return "nil  "
    else
        return tostring(tab).."  "
    end
end


function Log(...)
    local out = ""
    local args = {...}
    print(#args)
    for _,v in pairs(args) do 
        print("in")
        out = out..LogTable(v)
    end
    print(out)
end

function LogE(...)
    Log("ERROR",...)
end

Log(11,nil)
print("123")
