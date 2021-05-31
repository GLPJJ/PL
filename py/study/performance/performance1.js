
function performance1(){
    var strs = []
    for(i=0;i<1000000;i++){
        strs.push(""+i)
    }

    // console.log(strs)

    var log = ""
    var sep = ""
    console.log(Date.now(), "普通循环拼接")
    for(i=0;i<strs.length;i++){
        log += sep + strs[i] //粗糙的字符串拼接。。
        sep = " "
    }
        
    console.log(Date.now(),log.slice(0,100))
    log = ""
    console.log(Date.now(), "strings.join拼接")
    log = strs.join(" ") //性能完胜啊。。
    console.log(Date.now(),log.slice(0,100))
}


performance1()

