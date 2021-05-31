
console.log("abcdefghijklmnopqrstuvwxyz".toUpperCase(), Math.round(Math.random() * 10), Math.round(9.3));

var plainText = "abcdefghijklmnopqrstuvwxyz";
console.log(plainText.substring(0, plainText.length - 1));

console.log(new Date().getTime()/1000);

var http = "http://httpthirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epJbxlvia6KGZzOrlLoS2DISHZj9iaPpQUzGzsIULaQ7DgrSlPbOwL5Eib4PkNLADY5BQwwKrdtGTH4g/132";
console.log(http.indexOf("http"),http.indexOf("https"),http.replace("http","https"));

var state = 2
console.log((state >> 1) & 1 ? "True":"False")

var tips = [1,2,3];
var tips1 = tips.concat([4,6])
var tips2 = tips1.splice(0,0,7,8)
console.log(tips,tips1,tips2)
